from rest_framework import serializers
from .models import Plan, Subscription, Payment

class PlanSerializer(serializers.ModelSerializer):
    """플랜 정보 시리얼라이저"""
    class Meta:
        model = Plan
        fields = ['id', 'name', 'price', 'duration_days', 'description']

    
class SubscriptionSerializer(serializers.ModelSerializer):
    """구독 정보 시리얼라이저"""
    plan = PlanSerializer(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = Subscription
        fields = [
            'id', 'plan', 'status', 'is_active',
            'started_at', 'expires_at', 'cancelled_at'
        ]

class PaymentSerializer(serializers.ModelSerializer):
    """결제 내역 시리얼라이저"""
    class Meta:
        model = Payment
        fields = [
            'id', 'amount', 'status', 'order_id', 'paid_at', 'created_at'
        ]