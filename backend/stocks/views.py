from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Q
from .models import Stock
from .serializers import StockSerializer

# 1. 주식 검색 API (GET stocks/search/?q=삼성)
class StockSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.GET.get('q', '')
        if not query:
            return Response([])

        # 종목명(name) 또는 종목코드(ticker)에 검색어가 포함된 것 찾기
        stocks = Stock.objects.filter(
            Q(name__icontains=query) | Q(ticker__icontains=query)
        )[:10] # 너무 많으면 느리니까 10개만 제한

        serializer = StockSerializer(stocks, many=True)
        return Response(serializer.data)

# 2. 주식 상세 조회 API (GET stocks/<ticker>/)
class StockDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]

    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    lookup_field = 'ticker' # URL에서 ticker로 종목을 찾음
