from django.shortcuts import render

import requests
from decimal import Decimal
from django.conf import settings
from django.db.models import Max
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

from .models import DepositProduct, DepositOption, UserProduct, GoldPrice, SilverPrice
from .serializers import (
    DepositProductListSerializer,
    DepositProductDetailSerializer,
    UserProductSerializer,
    GoldPriceSerializer,
    SilverPriceSerializer
)


class DepositProductListView(APIView):
    """예적금 상품 목록 조회"""
    permission_classes = [AllowAny]  # 누구나 조회 가능

    def get(self, request):
        """상품 목록 조회"""
        product_type = request.query_params.get('type', 'deposit')
        search = request.query_params.get('search', '')
        bank = request.query_params.get('bank', '')

        products = DepositProduct.objects.filter(product_type=product_type)

        if search:
            products = products.filter(fin_prdt_nm__icontains=search)
        if bank:
            products = products.filter(kor_co_nm__icontains=bank)

        # 최고금리 순 정렬
        products = products.annotate(
            max_rate=Max('options__intr_rate2')
        ).order_by('-max_rate')

        serializer = DepositProductListSerializer(
            products, many=True, context={'request': request}
        )
        return Response(serializer.data)


class DepositProductDetailView(APIView):
    """예적금 상품 상세 조회"""
    permission_classes = [AllowAny]  # 누구나 조회 가능

    def get(self, request, pk):
        try:
            product = DepositProduct.objects.get(pk=pk)
        except DepositProduct.DoesNotExist:
            return Response({'error': '상품을 찾을 수 없습니다.'}, status=404)

        serializer = DepositProductDetailSerializer(product, context={'request': request})
        return Response(serializer.data)


class UserProductListView(APIView):
    """사용자 가입 상품 목록"""
    permission_classes = [IsAuthenticated]  # 로그인 필수

    def get(self, request):
        """가입 상품 목록 조회"""
        user_products = UserProduct.objects.filter(user=request.user)
        serializer = UserProductSerializer(user_products, many=True, context={'request': request})
        return Response(serializer.data)


class UserProductJoinView(APIView):
    """상품 가입/해지"""
    permission_classes = [IsAuthenticated]  # 로그인 필수

    def post(self, request, pk):
        """상품 가입"""
        try:
            product = DepositProduct.objects.get(pk=pk)
        except DepositProduct.DoesNotExist:
            return Response({'error': '상품을 찾을 수 없습니다.'}, status=404)

        option_id = request.data.get('option_id')
        memo = request.data.get('memo', '')

        option = None
        if option_id:
            try:
                option = DepositOption.objects.get(pk=option_id, product=product)
            except DepositOption.DoesNotExist:
                pass

        user_product, created = UserProduct.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'option': option, 'memo': memo}
        )

        if not created:
            return Response({'error': '이미 가입한 상품입니다.'}, status=400)

        return Response({
            'message': '상품에 가입했습니다.',
            'data': UserProductSerializer(user_product, context={'request': request}).data
        }, status=201)

    def delete(self, request, pk):
        """상품 해지"""
        try:
            user_product = UserProduct.objects.get(user=request.user, product_id=pk)
            user_product.delete()
            return Response({'message': '상품을 해지했습니다.'}, status=200)
        except UserProduct.DoesNotExist:
            return Response({'error': '가입한 상품이 아닙니다.'}, status=404)


class GoldPriceListView(APIView):
    """금 시세 조회"""
    permission_classes = [AllowAny]  # 누구나 조회 가능

    def get(self, request):
        limit = int(request.query_params.get('limit', 100))
        prices = GoldPrice.objects.all()[:limit]
        serializer = GoldPriceSerializer(prices, many=True)
        return Response(serializer.data)


class SilverPriceListView(APIView):
    """은 시세 조회"""
    permission_classes = [AllowAny]  # 누구나 조회 가능

    def get(self, request):
        limit = int(request.query_params.get('limit', 100))
        prices = SilverPrice.objects.all()[:limit]
        serializer = SilverPriceSerializer(prices, many=True)
        return Response(serializer.data)


class CommodityPriceView(APIView):
    """금/은 시세 통합 조회"""
    permission_classes = [AllowAny]  # 누구나 조회 가능

    def get(self, request):
        commodity_type = request.query_params.get('type', 'gold')
        limit = int(request.query_params.get('limit', 100))

        if commodity_type == 'gold':
            prices = GoldPrice.objects.all()[:limit]
            serializer = GoldPriceSerializer(prices, many=True)
        else:
            prices = SilverPrice.objects.all()[:limit]
            serializer = SilverPriceSerializer(prices, many=True)

        # 최신 가격 정보
        latest = prices.first() if prices else None
        previous = prices[1] if len(prices) > 1 else None

        change = None
        change_rate = None
        if latest and previous:
            change = float(latest.close_price) - float(previous.close_price)
            change_rate = (change / float(previous.close_price)) * 100

        return Response({
            'type': commodity_type,
            'latest': {
                'date': latest.date if latest else None,
                'price': latest.close_price if latest else None,
                'change': round(change, 2) if change else None,
                'change_rate': round(change_rate, 2) if change_rate else None,
            },
            'history': serializer.data
        })