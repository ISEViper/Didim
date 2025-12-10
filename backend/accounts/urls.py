from django.urls import path, include
from .views import NaverCallbackView

app_name = 'accounts'
urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('signup/', include('dj_rest_auth.registration.urls')),
    path('naver/callback/', NaverCallbackView.as_view(), name='naver_callback'),
]