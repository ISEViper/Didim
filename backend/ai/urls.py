from django.urls import path, include
from . import views

app_name = 'ai'
urlpatterns = [
    path('analyze/<str:ticker>/', views.get_ai_analysis, name='get-ai-analysis'),
]