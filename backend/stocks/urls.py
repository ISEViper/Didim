from django.urls import path
from .views import StockSearchView, StockDetailView

app_name = 'stocks'

urlpatterns = [
    path('search/', StockSearchView.as_view(), name='stock-search'),
    path('<str:ticker>/', StockDetailView.as_view(), name='stock-detail'),
]