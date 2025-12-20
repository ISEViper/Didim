from django.db import models
from django.conf import settings


class Plan(models.Model):
    """구독 플랜"""
    name = models.CharField(max_length=50, verbose_name='플랜명')
    price = models.IntegerField(verbose_name='가격(원)')
    duration_days = models.IntegerField(default=30, verbose_name='기간(일)')
    description = models.TextField(blank=True, verbose_name='설명')
    is_active = models.BooleanField(default=True, verbose_name='활성화')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '구독 플랜'
        verbose_name_plural = '구독 플랜'

    def __str__(self):
        return f"{self.name} - {self.price:,}원"


class Subscription(models.Model):
    """사용자 구독 정보"""
    STATUS_CHOICES = [
        ('active', '구독중'),
        ('cancelled', '취소됨'),
        ('expired', '만료됨'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscription',
        verbose_name='사용자'
    )
    plan = models.ForeignKey(
        Plan,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='플랜'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name='상태'
    )
    billing_key = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='빌링키'
    )
    customer_key = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='고객키'
    )
    started_at = models.DateTimeField(verbose_name='구독 시작일')
    expires_at = models.DateTimeField(verbose_name='구독 만료일')
    cancelled_at = models.DateTimeField(null=True, blank=True, verbose_name='취소일')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '구독'
        verbose_name_plural = '구독'

    def __str__(self):
        return f"{self.user.email} - {self.plan.name if self.plan else 'N/A'}"

    @property
    def is_active(self):
        """구독이 활성 상태인지 확인"""
        from django.utils import timezone
        return self.status == 'active' and self.expires_at > timezone.now()


class Payment(models.Model):
    """결제 내역"""
    STATUS_CHOICES = [
        ('pending', '대기중'),
        ('completed', '완료'),
        ('failed', '실패'),
        ('refunded', '환불됨'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='사용자'
    )
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.SET_NULL,
        null=True,
        related_name='payments',
        verbose_name='구독'
    )
    amount = models.IntegerField(verbose_name='결제금액')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='상태'
    )
    payment_key = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='토스 결제키'
    )
    order_id = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='주문번호'
    )
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name='결제일시')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '결제'
        verbose_name_plural = '결제'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.amount:,}원 ({self.status})"