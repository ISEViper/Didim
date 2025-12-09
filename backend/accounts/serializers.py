from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.db import transaction

class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    @transaction.atomic
    def save(self, request):
        # 기본 회원가입 로직 실행 (User 객체 생성됨)
        user = super().save(request)
        
        # 입력받은 이름 정보를 User 객체에 저장
        user.first_name = self.validated_data.get('first_name', '')
        user.last_name = self.validated_data.get('last_name', '')
        
        # 변경사항 DB에 반영
        user.save()
        
        return user