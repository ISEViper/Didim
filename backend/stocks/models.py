from django.db import models
from django.conf import settings

# 한국주식(KRX) 및 ETF 기본 정보 담는 모델
class Stock(models.Model):
    ASSET_CHOICES = (
        ('STOCK', '주식'),
        ('ETF', 'ETF'),
    )

    ticker = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    asset_type = models.CharField(max_length=10, choices=ASSET_CHOICES, default='STOCK')
    market_type = models.CharField(max_length=20)
    market_cap = models.BigIntegerField(null=True, blank=True)
    total_shares = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return f'[{self.asset_type}]: {self.name}({self.ticker})'

class DailyPrice(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='daily_price')

    date = models.DateField()

    open_price = models.BigIntegerField()
    high_price = models.BigIntegerField()
    low_price = models.BigIntegerField()
    close_price = models.BigIntegerField()
    fluctuation_rate = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    volume = models.BigIntegerField()
    trading_value = models.BigIntegerField(null=True, blank=True)
    change = models.BigIntegerField(null=True, blank=True)

    # ETF 전용: 순자산가치 (주식인 경우 NULL)
    nav = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ('stock', 'date')
        ordering = ['-date']

    def __str__(self):
        return f'{self.stock.name} - {self.date}'
    
class Watchlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='watchlist')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='watched_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'stock')
        ordering=['-created_at']