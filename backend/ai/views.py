from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from django.db.models import Max

from stocks.models import Stock 
from finance.models import DepositProduct, DepositOption
from .models import StockAiAnalysis, UserFinanceSurvey, UserAiRecommendation
from .serializers import SurveySubmitSerializer, UserFinanceSurveySerializer, UserAiRecommendationSerializer
from .utils import generate_stock_analysis, generate_finance_recommendation
from .constants import SURVEY_CHOICES


@api_view(['GET'])
@permission_classes([AllowAny])
def get_ai_analysis(request, ticker):
    try:
        recent_time = timezone.now() - timedelta(hours=24)
        cached_data = StockAiAnalysis.objects.filter(
            ticker=ticker, 
            created_at__gte=recent_time
        ).last()

        if cached_data:
            return Response(cached_data.data)

        stock_obj = Stock.objects.filter(ticker=ticker).first()
        stock_name = stock_obj.name if stock_obj else ticker

        result_data = generate_stock_analysis(ticker, stock_name, asset_type=stock_obj.asset_type if stock_obj else 'STOCK')

        if not result_data:
            return Response({"error": "AI 분석 생성 실패"}, status=500)

        StockAiAnalysis.objects.create(ticker=ticker, data=result_data)

        return Response(result_data)

    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_survey_choices(request):
    """설문 선택지 목록 반환"""
    return Response(SURVEY_CHOICES)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_recommendation(request):
    """사용자의 AI 추천 결과 조회"""
    try:
        recommendation = UserAiRecommendation.objects.get(user=request.user)
        survey = UserFinanceSurvey.objects.get(user=request.user)
        
        # 추천된 예적금 상품 정보 조회
        deposit_ids = recommendation.recommended_deposit_ids
        deposits = DepositProduct.objects.filter(id__in=deposit_ids).annotate(
            max_rate=Max('options__intr_rate2')
        ).values('id', 'kor_co_nm', 'fin_prdt_nm', 'product_type', 'max_rate', 'join_way')
        
        # 추천된 주식 종목 정보 조회 (ticker 기준)
        stock_tickers = recommendation.recommended_stock_ids
        stocks = Stock.objects.filter(ticker__in=stock_tickers).values('ticker', 'name', 'asset_type')
        
        return Response({
            'has_result': True,
            'survey': UserFinanceSurveySerializer(survey).data,
            'recommendation': {
                'investor_type': recommendation.investor_type,
                'asset_allocation': recommendation.asset_allocation,
                'advice': recommendation.advice,
                'deposit_recommendation': recommendation.deposit_recommendation,
                'stock_recommendation': recommendation.stock_recommendation,
            },
            'recommended_deposits': list(deposits),
            'recommended_stocks': list(stocks),
            'updated_at': recommendation.updated_at
        })
        
    except (UserAiRecommendation.DoesNotExist, UserFinanceSurvey.DoesNotExist):
        return Response({
            'has_result': False,
            'message': '아직 금융 성향 진단을 완료하지 않았습니다.'
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_survey(request):
    """설문 제출 및 AI 추천 생성"""
    serializer = SurveySubmitSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    
    # 설문 결과 저장 (있으면 업데이트, 없으면 생성)
    survey, _ = UserFinanceSurvey.objects.update_or_create(
        user=request.user,
        defaults={
            'savings': data['savings'],
            'investment': data['investment'],
            'income': data['income'],
            'q2_goal': data['q2_goal'],
            'q3_period': data['q3_period'],
            'q4_knowledge': data['q4_knowledge'],
            'q5_experience': data['q5_experience'],
            'q6_expected_return': data['q6_expected_return'],
            'q7_risk_tolerance': data['q7_risk_tolerance'],
            'q8_monthly_saving': data['q8_monthly_saving'],
            'q9_loss_reaction': data['q9_loss_reaction'],
            'q10_interest': data['q10_interest'],
        }
    )
    
    # 예적금 상품 목록 조회 (최고금리 순)
    deposit_products = DepositProduct.objects.annotate(
        max_rate=Max('options__intr_rate2')
    ).order_by('-max_rate').values(
        'id', 'kor_co_nm', 'fin_prdt_nm', 'product_type', 'max_rate'
    )[:30]
    
    # 주식 종목 목록 조회 (ticker가 primary key)
    stocks = Stock.objects.all().values('ticker', 'name', 'asset_type')[:50]
    
    # AI 추천 생성
    ai_result = generate_finance_recommendation(
        survey,
        list(deposit_products),
        list(stocks)
    )
    
    if not ai_result:
        return Response(
            {'error': 'AI 추천 생성에 실패했습니다. 잠시 후 다시 시도해주세요.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # AI 추천 결과 저장 (덮어쓰기)
    recommendation, _ = UserAiRecommendation.objects.update_or_create(
        user=request.user,
        defaults={
            'investor_type': ai_result.get('investor_type', {}),
            'asset_allocation': ai_result.get('asset_allocation', {}),
            'advice': ai_result.get('advice', {}),
            'recommended_deposit_ids': ai_result.get('recommended_deposits', {}).get('ids', []),
            'recommended_stock_ids': ai_result.get('recommended_stocks', {}).get('tickers', []),
            'deposit_recommendation': ai_result.get('recommended_deposits', {}),
            'stock_recommendation': ai_result.get('recommended_stocks', {}),
        }
    )
    
    # 추천된 상품 정보 조회
    deposit_ids = recommendation.recommended_deposit_ids
    deposits = DepositProduct.objects.filter(id__in=deposit_ids).annotate(
        max_rate=Max('options__intr_rate2')
    ).values('id', 'kor_co_nm', 'fin_prdt_nm', 'product_type', 'max_rate', 'join_way')
    
    stock_tickers = recommendation.recommended_stock_ids
    stocks_result = Stock.objects.filter(ticker__in=stock_tickers).values('ticker', 'name', 'asset_type')
    
    return Response({
        'success': True,
        'survey': UserFinanceSurveySerializer(survey).data,
        'recommendation': {
            'investor_type': recommendation.investor_type,
            'asset_allocation': recommendation.asset_allocation,
            'advice': recommendation.advice,
            'deposit_recommendation': recommendation.deposit_recommendation,
            'stock_recommendation': recommendation.stock_recommendation,
        },
        'recommended_deposits': list(deposits),
        'recommended_stocks': list(stocks_result),
    })