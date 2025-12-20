from django.shortcuts import render
import requests
import base64
import uuid
from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Plan, Subscription, Payment
from .serializers import PlanSerializer, SubscriptionSerializer, PaymentSerializer

# Create your views here.
class PlanListView(APIView):
    """구독 플랜 목록 조회"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        plans = Plan.objects.filter(is_active=True)
        serializer = PlanSerializer(plans, many=True)
        return Response(serializer.data)
    
class SubscriptionStatusView(APIView):
    """현재 구독 상태 조회"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            subscription = Subscription.objects.get(user=request.user)
            serializer = SubscriptionSerializer(subscription)
            return Response({
                'has_subcription': True,
                'subscription': serializer.data
            })
        except Subscription.DoesNotExist:
            return Response({
                'has_subscription': False,
                'subscription': None
            })
        
class BillingKeyIssueView(APIView):
    """
    빌링키 발급(카드 등록 완료 후 호출)
    토스 결제창에서 카드 등록 완료 -> authKey 발급 -> 이 API로 전송 -> 빌링키 발급
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        auth_key = request.data.get('authKey')
        customer_key = request.data.get('customerKey')

        if not auth_key or not customer_key:
            return Response({'error': 'authKey와 customerKey가 필요합니다.'}, status=400)
        
        # 토스페이먼츠 API 인증 헤더 생성
        secret_key = settings.TOSS_SECRET_KEY
        credentials = base64.b64encode(f"{secret_key}:".encode()).decode()

        # 빌링키 발급 API 호출
        response = requests.post(
            'https://api.tosspayments.com/v1/billing/authorizations/issue',
            headers={
                'Authorization': f'Basic {credentials}',
                'Content-Type': 'application/json'
            },
            json={
                'authKey': auth_key,
                'customerKey': customer_key
            }
        )

        if response.status_code != 200:
            # 토스가 보내주는 구체적인 에러 메시지를 확인하기 위해 print 추가
            print(f"Toss API Error: {response.status_code} - {response.text}")
            return Response({
                'error': '빌링키 발급 실패',
                'detail': response.json()
            }, status=400)

        data = response.json()
        billing_key = data.get('billingKey')

        # 빌링키 저장(구독 생성은 아직 안함, 결제 완료 후 생성)
        # 임시로 세션이나 응답으로 전달
        return Response({
            'success': True,
            'billingKey': billing_key,
            'customerKey': customer_key,
            'card': data.get('card', {})
        })
    
class SubscribeView(APIView):
    """
    구독 결제 실행
    빌링키로 실제 결제를 진행하고 구독을 생성
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        billing_key = request.data.get('billingKey')
        customer_key = request.data.get('customerKey')
        plan_id = request.data.get('planId')

        if not all([billing_key, customer_key, plan_id]):
            return Response({'error': '필수 정보가 누락되었습니다.'}, status=400)
        
        # 이미 구독 중인지 확인
        existing_sub = Subscription.objects.filter(
            user=request.user,
            status='active'
        ).first()

        if existing_sub and existing_sub.is_active:
            return Response({'error': '이미 구독 중입니다.'}, status=400)
        
        # 플랜 조회
        try:
            plan = Plan.objects.get(id=plan_id, is_active=True)
        except Plan.DoesNotExist:
            return Response({'error': '유효하지 않은 플랜입니다.'}, status=400)
        
        # 주문번호 생성
        order_id = f"DIDIM_{request.user.id}_{uuid.uuid4().hex[:8]}"

        # 토스페이먼츠 빌링 결제 API 호출
        secret_key = settings.TOSS_SECRET_KEY
        credentials = base64.b64encode(f"{secret_key}:".encode()).decode()

        response = requests.post(
            f'https://api.tosspayments.com/v1/billing/{billing_key}',
            headers={
                'Authorization': f'Basic {credentials}',
                'Content-Type': 'application/json'
            },
            json={
                'customerKey': customer_key,
                'amount': plan.price,
                'orderId': order_id,
                'orderName': f'DIDIM {plan.name} 구독',
                'customerEmail': request.user.email,
            }
        )

        if response.status_code != 200:
            # 결제 실패
            Payment.objects.create(
                user=request.user,
                amount=plan.price,
                status='failed',
                order_id=order_id
            )
            return Response({
                'error': '결제 실패',
                'detail': response.json()
            }, status=400)

        payment_data = response.json()

        # 결제 성공 - Payment 생성
        payment = Payment.objects.create(
            user=request.user,
            amount=plan.price,
            status='completed',
            payment_key=payment_data.get('paymentKey'),
            order_id=order_id,
            paid_at=timezone.now()
        )

        # 구독 생성 또는 갱신
        now = timezone.now()
        expires_at = now + timedelta(days=plan.duration_days)

        subscription, created = Subscription.objects.update_or_create(
            user=request.user,
            defaults={
                'plan': plan,
                'status': 'active',
                'billing_key': billing_key,
                'customer_key': customer_key,
                'started_at': now,
                'expires_at': expires_at,
                'cancelled_at': None
            }
        )

        payment.subscription = subscription
        payment.save()

        return Response({
            'success': True,
            'message': '구독이 완료되었습니다.',
            'subscription': SubscriptionSerializer(subscription).data
        })
    
class CancelSubscriptionView(APIView):
    """구독 취소"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            subscription = Subscription.objects.get(user=request.user)
        except Subscription.DoesNotExist:
            return Response({'error': '구독 정보가 없습니다.'}, status=404)

        if subscription.status == 'cancelled':
            return Response({'error': '이미 취소된 구독입니다.'}, status=400)

        # 구독 취소 (만료일까지는 사용 가능, 자동 갱신만 중지)
        subscription.status = 'cancelled'
        subscription.cancelled_at = timezone.now()
        subscription.save()

        return Response({
            'success': True,
            'message': '구독이 취소되었습니다. 만료일까지 서비스를 이용할 수 있습니다.',
            'expires_at': subscription.expires_at
        })
    
class PaymentHistoryView(APIView):
    """결제 내역 조회"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payments = Payment.objects.filter(user=request.user)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)