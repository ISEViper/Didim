from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Stock, Watchlist
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
