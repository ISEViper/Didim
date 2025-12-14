from django.urls import path
from . import views

app_name = 'stocks'

urlpatterns = [
    path('search/', views.stock_search, name='stock-search'),
    path('watchlist/', views.watchlist_list, name='watchlist-list'), 
    path('watchlist/<str:ticker>/', views.watchlist_detail, name='watchlist-delete'),
    path('<str:ticker>/chart/', views.stock_chart_data, name='stock-chart'),
    path('<str:ticker>/', views.stock_detail, name='stock-detail'),
]