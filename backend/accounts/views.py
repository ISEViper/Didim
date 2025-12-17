# accounts/views.py
import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import UserProfileSerializer, UserProfileUpdateSerializer

User = get_user_model()

class NaverCallbackView(APIView):
    """프론트에서 받은 네이버 code로 로그인 처리"""
    permission_classes = [AllowAny]

    def generate_unique_nickname(self, base_nickname):
        """닉네임 중복 제한 설정"""
        nickname = base_nickname
        counter = 1

        while User.objects.filter(nickname=nickname).exists():
            nickname = f"{base_nickname}_{counter}"
            counter += 1

        return nickname
    
    def post(self, request):
        code = request.data.get('code')
        state = request.data.get('state')
        
        if not code:
            return Response({'error': 'code가 필요합니다.'}, status=400)
        
        # 1. 네이버에서 access_token 발급
        token_url = 'https://nid.naver.com/oauth2.0/token'
        token_data = {
            'grant_type': 'authorization_code',
            'client_id': settings.NAVER_CLIENT_ID,
            'client_secret': settings.NAVER_CLIENT_SECRET,
            'code': code,
            'state': state,
        }
        
        token_response = requests.post(token_url, data=token_data)
        token_json = token_response.json()
        
        if 'access_token' not in token_json:
            return Response({'error': '네이버 토큰 발급 실패'}, status=400)
        
        access_token = token_json['access_token']
        
        # 2. 네이버 사용자 정보 조회
        profile_url = 'https://openapi.naver.com/v1/nid/me'
        headers = {'Authorization': f'Bearer {access_token}'}
        profile_response = requests.get(profile_url, headers=headers)
        profile_json = profile_response.json()
        
        if profile_json.get('resultcode') != '00':
            return Response({'error': '네이버 프로필 조회 실패'}, status=400)
        
        naver_data = profile_json.get('response', {})
        naver_id = naver_data.get('id')
        email = naver_data.get('email')
        name = naver_data.get('name', '')
        profile_image = naver_data.get('profile_image', '')
        
        # 3. 기존 소셜 계정 확인 또는 신규 생성
        try:
            social_account = SocialAccount.objects.get(
                provider='naver',
                uid=naver_id
            )
            user = social_account.user
        except SocialAccount.DoesNotExist:
            # 이메일로 기존 유저 확인
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # 신규 유저 생성
                unique_nickname = self.generate_unique_nickname(name) if name else f"user_{naver_id[:8]}"
                user = User.objects.create_user(
                    username=f'naver_{naver_id}',
                    email=email,
                    first_name=name,
                    nickname=unique_nickname,
                )
            
            # 소셜 계정 연결
            SocialAccount.objects.create(
                user=user,
                provider='naver',
                uid=naver_id,
                extra_data=naver_data
            )
        
        # 4. JWT 토큰 발급
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'pk': user.pk,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'nickname': user.nickname,
                'profile_image_url': user.get_profile_image_url(),
                'display_initial': user.get_display_initial(),
            }
        })
    
class ProfileView(APIView):
    """프로필 조회 및 수정 API"""
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        """프로필 조회"""
        serializer = UserProfileSerializer(request.user, context={'request': request})
        return Response(serializer.data)
    
    def patch(self, request):
        """프로필 수정(닉네임, 프로필 이미지)"""
        serializer = UserProfileUpdateSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            profile_serializer = UserProfileSerializer(request.user, context={'request': request})
            return Response(profile_serializer.data)
        return Response(serializer.errors, status=400)
        
    def delete(self, request):
        """프로필 이미지 삭제"""
        user = request.user
        if user.profile_image:
            user.profile_image.delete()
            user.profile_image = None
            user.save()
        return Response({'message': '프로필 이미지가 삭제되었습니다.'})
    
class PasswordVerifyView(APIView):
    """비밀번호 확인 API (정보 수정 전 본인 확인용)"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        password = request.data.get('password')
        
        if not password:
            return Response({'error': '비밀번호를 입력해주세요.'}, status=400)
        
        # 비밀번호 확인
        if request.user.check_password(password):
            return Response({'message': '비밀번호가 확인되었습니다.'})
        else:
            return Response({'error': '비밀번호가 올바르지 않습니다.'}, status=400)