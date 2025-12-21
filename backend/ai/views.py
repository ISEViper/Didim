from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from stocks.models import Stock 
from .models import StockAiAnalysis
from .utils import generate_stock_analysis

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

        result_data = generate_stock_analysis(ticker, stock_name, asset_type=stock_obj.asset_type)

        if not result_data:
            return Response({"error": "AI 분석 생성 실패"}, status=500)

        StockAiAnalysis.objects.create(ticker=ticker, data=result_data)

        return Response(result_data)

    except Exception as e:
        return Response({"error": str(e)}, status=500)