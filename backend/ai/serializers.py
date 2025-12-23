from rest_framework import serializers
from .models import UserFinanceSurvey, UserAiRecommendation


class SurveySubmitSerializer(serializers.Serializer):
    """설문 제출용 시리얼라이저"""
    # 자산 정보
    savings = serializers.IntegerField(min_value=0)
    investment = serializers.IntegerField(min_value=0)
    income = serializers.IntegerField(min_value=0)
    
    # 설문 응답
    q2_goal = serializers.IntegerField(min_value=0, max_value=4)
    q3_period = serializers.IntegerField(min_value=0, max_value=4)
    q4_knowledge = serializers.IntegerField(min_value=0, max_value=3)
    q5_experience = serializers.IntegerField(min_value=0, max_value=4)
    q6_expected_return = serializers.IntegerField(min_value=0, max_value=4)
    q7_risk_tolerance = serializers.IntegerField(min_value=0, max_value=4)
    q8_monthly_saving = serializers.IntegerField(min_value=0, max_value=4)
    q9_loss_reaction = serializers.IntegerField(min_value=0, max_value=3)
    q10_interest = serializers.IntegerField(min_value=0, max_value=4)


class UserFinanceSurveySerializer(serializers.ModelSerializer):
    """설문 결과 조회용"""
    class Meta:
        model = UserFinanceSurvey
        exclude = ['user']


class UserAiRecommendationSerializer(serializers.ModelSerializer):
    """AI 추천 결과 조회용"""
    class Meta:
        model = UserAiRecommendation
        exclude = ['user']