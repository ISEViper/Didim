import requests
import re
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Stock, Watchlist, Chartprice
from .serializers import StockSerializer, WatchlistSerializer

# 1. 주식 검색
@api_view(['GET'])
@permission_classes([AllowAny])
def stock_search(request):
    query = request.GET.get('q', '')
    
    if not query:
        return Response([])

    stocks = Stock.objects.filter(
        Q(name__icontains=query) | Q(ticker__icontains=query)
    )[:10] # 10개 제한

    serializer = StockSerializer(stocks, many=True)
    return Response(serializer.data)


# 2. 주식 상세 조회
@api_view(['GET'])
@permission_classes([AllowAny])
def stock_detail(request, ticker):
    stock = get_object_or_404(Stock, ticker=ticker)
    
    serializer = StockSerializer(stock)
    return Response(serializer.data)


# 3. 관심종목 목록 조회 및 추가
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def watchlist_list(request):
    if request.method == 'GET':
        watchlist = Watchlist.objects.filter(user=request.user)
        serializer = WatchlistSerializer(watchlist, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        ticker = request.data.get('ticker')

        if not ticker:
            return Response({'error': 'Ticker is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            stock = Stock.objects.get(ticker=ticker)
        except Stock.DoesNotExist:
            return Response({'error': 'Stock not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        obj, created = Watchlist.objects.get_or_create(user=request.user, stock=stock)

        if created:
            return Response({'status': 'added', 'message': f'{stock.name} 추가됨'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'already_exists', 'message': '이미 관심목록에 있습니다.'}, status=status.HTTP_200_OK)


# 4. 관심종목 삭제 (DELETE)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])    
def watchlist_detail(reqeust, ticker):
    if reqeust.method == 'DELETE':
        deleted_count, _ = Watchlist.objects.filter(user=reqeust.user, stock__ticker=ticker).delete()

        if deleted_count > 0:
            return Response({'status': 'deleted'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'Not found in watchlist'}, status=status.HTTP_404_NOT_FOUND)


# 5. 차트데이터용 주식 가격 불러오기        
@api_view(['GET'])
@permission_classes([AllowAny])
def stock_chart_data(request, ticker):
    period = request.GET.get('period', '1y') # 기본값 1년
    end_date = timezone.now().date()
    
    # 기간에 따른 시작일 계산
    if period == '1w':
        start_date = end_date - timedelta(weeks=1)
    elif period == '1m':
        start_date = end_date - relativedelta(months=1)
    elif period == '6m':
        start_date = end_date - relativedelta(months=6)
    elif period == '1y':
        start_date = end_date - relativedelta(years=1)
    elif period == '3y':
        start_date = end_date - relativedelta(years=3)
    elif period == '5y':
        start_date = end_date - relativedelta(years=5)
    else: # 전체
        start_date = end_date - relativedelta(years=10)

    # DB에서 해당 기간 데이터만 조회 (최적화)
    data = Chartprice.objects.filter(
        stock__ticker=ticker,
        date__gte=start_date,
        date__lte=end_date
    ).values('date', 'close_price').order_by('date')

    return Response(data)

# 6. 주식 관련 뉴스 불러오기
@api_view(['GET'])
@permission_classes([AllowAny])
def stock_news(request, ticker):
    try:
        stock = Stock.objects.get(ticker=ticker)
        query = stock.name
    except Stock.DoesNotExist:
        return Response({'error': 'Stock not found'}, status=404)
    
    client_id = settings.NAVER_CLIENT_ID
    client_secret = settings.NAVER_CLIENT_SECRET
    
    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
    }
    params = {
        "query": query,
        "display": 20,
        "sort":"date"
    }

    res = requests.get(url, headers=headers, params=params)

    if res.status_code != 200:
        return Response({'error': 'Naver API Error'}, status=500)
    
    items = res.json().get('items', [])
    news_list = []

    for item in items:
        title = re.sub('<[^<]+?>', '', item['title'])
        title = title.replace('&quot;', '"').replace('&amp;', '&')

        try:
            raw_date = item['pubDate']
            dt = datetime.striptime(raw_date, '%a, %d %b %Y %H:%M:%S +0900')
            formatted_date = dt.strfttime('%m.%d %H:%M')
        except:
            formatted_date = item['pubDate']

        news_list.append({
            'title': title,
            'link': item['link'],
            'date': formatted_date,
            'publisher': '네이버뉴스'
        })
    
    return Response(news_list)