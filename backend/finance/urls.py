from django.urls import path
from .views import (
    DepositProductListView,
    DepositProductDetailView,
    UserProductListView,
    UserProductJoinView,
    GoldPriceListView,
    SilverPriceListView,
    CommodityPriceView
)

app_name = 'finance'

urlpatterns = [
    # 예적금 상품
    path('deposits/', DepositProductListView.as_view(), name='deposit-list'),
    path('deposits/<int:pk>/', DepositProductDetailView.as_view(), name='deposit-detail'),
    
    # 사용자 가입 상품
    path('my-products/', UserProductListView.as_view(), name='my-products'),
    path('products/<int:pk>/join/', UserProductJoinView.as_view(), name='product-join'),
    
    # 현물 시세
    path('commodities/', CommodityPriceView.as_view(), name='commodity-price'),
    path('gold/', GoldPriceListView.as_view(), name='gold-price'),
    path('silver/', SilverPriceListView.as_view(), name='silver-price'),
]