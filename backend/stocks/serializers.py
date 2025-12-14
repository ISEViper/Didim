from rest_framework import serializers
from .models import Stock, DailyPrice, Watchlist, Chartprice

# 1. 일별 시세 정보 Serializer
class DailyPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyPrice
        fields = '__all__'

# 2. 주식 기본 정보 Serializer
class StockSerializer(serializers.ModelSerializer):
    latest_price = serializers.SerializerMethodField()

    class Meta:
        model = Stock
        fields = ['ticker', 'name', 'market_type', 'market_cap', 'latest_price']

    def get_latest_price(self, obj):
        price = obj.daily_price.order_by('-date').first()
        if price:
            return DailyPriceSerializer(price).data
        return None

# 3. 관심 종목 Serializer
class WatchlistSerializer(serializers.ModelSerializer):
    stock = StockSerializer(read_only=True)

    class Meta:
        model = Watchlist
        fields = ['id', 'stock', 'created_at']

# 4. 주식 차트 가격 Serializer
class ChartpriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chartprice
        fields = ['date', 'close_price']