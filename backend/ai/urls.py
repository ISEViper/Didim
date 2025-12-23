from django.urls import path, include
from . import views

app_name = 'ai'
urlpatterns = [
    path('analyze/<str:ticker>/', views.get_ai_analysis, name='get-ai-analysis'),
    path('survey/choices/', views.get_survey_choices, name='survey-choices'),
    path('survey/submit/', views.submit_survey, name='survey-submit'),
    path('recommendation/', views.get_user_recommendation, name='user-recommendation'),
]