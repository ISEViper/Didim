from django.db import models
from django.conf import settings

# Create your models here.
class StockAiAnalysis(models.Model):
    ticker = models.CharField(max_length=10, db_index=True)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AI Analysis: {self.ticker} ({self.created_at})"
    
class UserFinanceSurvey(models.Model):
    """사용자 금융 성향 설문 결과"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='finance_survey'
    )
    
    # 자산 정보
    savings = models.BigIntegerField(default=0, verbose_name='입출금/저축')
    investment = models.BigIntegerField(default=0, verbose_name='투자 자산')
    income = models.BigIntegerField(default=0, verbose_name='연봉')
    
    # 설문 응답 (1~5 또는 선택지 인덱스)
    q2_goal = models.IntegerField(default=0, verbose_name='금융 목표')
    q3_period = models.IntegerField(default=0, verbose_name='투자 기간')
    q4_knowledge = models.IntegerField(default=0, verbose_name='금융 지식')
    q5_experience = models.IntegerField(default=0, verbose_name='투자 경험')
    q6_expected_return = models.IntegerField(default=0, verbose_name='기대 수익률')
    q7_risk_tolerance = models.IntegerField(default=0, verbose_name='손실 감내')
    q8_monthly_saving = models.IntegerField(default=0, verbose_name='월 저축 여력')
    q9_loss_reaction = models.IntegerField(default=0, verbose_name='손실 시 반응')
    q10_interest = models.IntegerField(default=0, verbose_name='관심 분야')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '금융 성향 설문'
        verbose_name_plural = '금융 성향 설문'

    def __str__(self):
        return f"{self.user.username}의 금융 설문"


class UserAiRecommendation(models.Model):
    """AI 추천 결과 저장"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ai_recommendation'
    )
    
    # AI 분석 결과 (JSON)
    investor_type = models.JSONField(default=dict, verbose_name='투자자 유형')
    asset_allocation = models.JSONField(default=dict, verbose_name='자산 배분')
    advice = models.JSONField(default=dict, verbose_name='조언')
    
    # 추천 상품 (ID 리스트)
    recommended_deposit_ids = models.JSONField(default=list, verbose_name='추천 예적금 ID')
    recommended_stock_ids = models.JSONField(default=list, verbose_name='추천 주식 ID')
    
    # 추천 이유
    deposit_recommendation = models.JSONField(default=dict, verbose_name='예적금 추천 정보')
    stock_recommendation = models.JSONField(default=dict, verbose_name='주식 추천 정보')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'AI 추천 결과'
        verbose_name_plural = 'AI 추천 결과'

    def __str__(self):
        return f"{self.user.username}의 AI 추천"