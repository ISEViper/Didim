from django.urls import path
from .views import (
    PlanListView,
    SubscriptionStatusView,
    BillingKeyIssueView,
    SubscribeView,
    CancelSubscriptionView,
    PaymentHistoryView
)

app_name = 'subscriptions'

urlpatterns = [
    path('plans/', PlanListView.as_view(), name='plan-list'),
    path('status/', SubscriptionStatusView.as_view(), name='subscription-status'),
    path('billing-key/', BillingKeyIssueView.as_view(), name='billing-key'),
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
    path('cancel/', CancelSubscriptionView.as_view(), name='cancel'),
    path('payments/', PaymentHistoryView.as_view(), name='payment-history'),
]