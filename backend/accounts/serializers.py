from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.db import transaction
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    nickname = serializers.CharField(required=True, max_length=30)
    profile_image = serializers.ImageField(required=False, allow_null=True, default=None)

    def validate_nickname(self, value):
        """닉네임 중복 체크"""
        if User.objects.filter(nickname=value).exists():
            raise serializers.ValidationError("이미 사용 중인 닉네임입니다.")
        return value

    @transaction.atomic
    def save(self, request):
        # 기본 회원가입 로직 실행 (User 객체 생성됨)
        user = super().save(request)
        
        # 입력받은 이름 정보를 User 객체에 저장
        user.first_name = self.validated_data.get('first_name', '')
        user.last_name = self.validated_data.get('last_name', '')
        user.nickname = self.validated_data.get('nickname', '')
        
        profile_image = self.validated_data.get('profile_image')
        if profile_image:
            user.profile_image = profile_image

        # 변경사항 DB에 반영
        user.save()
        
        return user
    def get_cleaned_data(self):
        """dj-rest-auth가 사용하는 메서드 오버라이드"""
        data = super().get_cleaned_data()
        data['first_name'] = self.validated_data.get('first_name', '')
        data['last_name'] = self.validated_data.get('last_name', '')
        data['nickname'] = self.validated_data.get('nickname', '')
        data['profile_image'] = self.validated_data.get('profile_image', None)
        return data
    
class UserProfileSerializer(serializers.ModelSerializer):
    """프로필 조회용 시리얼라이저"""
    has_password = serializers.SerializerMethodField()
    profile_image_url = serializers.SerializerMethodField()
    display_initial = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'pk',
            'email',
            'first_name',
            'last_name',
            'nickname',
            'profile_image',
            'profile_image_url',
            'display_initial',
            'has_password',
        ]
        read_only_fields = ['pk', 'email', 'first_name', 'last_name']

    def get_profile_image_url(self, obj):
        if obj.profile_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.profile_image.url)
            return obj.profile_image.url
        return None

    def get_display_initial(self, obj):
        return obj.get_display_initial()
    
    def get_has_password(self, obj):
        return obj.has_usable_password()


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """프로필 수정용 시리얼라이저 - 닉네임, 프로필 이미지만 수정 가능"""
    
    class Meta:
        model = User
        fields = ['nickname', 'profile_image']

    def validate_nickname(self, value):
        """닉네임 중복 체크 (본인 제외)"""
        user = self.context['request'].user
        if User.objects.filter(nickname=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("이미 사용 중인 닉네임입니다.")
        return value