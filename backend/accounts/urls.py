from django.urls import path, include
from .views import NaverCallbackView, ProfileView, PasswordVerifyView

app_name = 'accounts'
urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('signup/', include('dj_rest_auth.registration.urls')),
    path('naver/callback/', NaverCallbackView.as_view(), name='naver_callback'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password/verify/', PasswordVerifyView.as_view(), name='password_verify'),
]