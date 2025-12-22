from rest_framework import serializers
from .models import DepositProduct, DepositOption, UserProduct, GoldPrice, SilverPrice


class DepositOptionSerializer(serializers.ModelSerializer):
    """예적금 옵션 시리얼라이저"""
    class Meta:
        model = DepositOption
        fields = [
            'id', 'intr_rate_type', 'intr_rate_type_nm',
            'save_trm', 'intr_rate', 'intr_rate2'
        ]


class DepositProductListSerializer(serializers.ModelSerializer):
    """예적금 상품 목록 시리얼라이저"""
    max_rate = serializers.SerializerMethodField()
    is_joined = serializers.SerializerMethodField()

    class Meta:
        model = DepositProduct
        fields = [
            'id', 'fin_co_no', 'fin_prdt_cd', 'kor_co_nm', 'fin_prdt_nm',
            'product_type', 'join_way', 'max_limit', 'max_rate', 'is_joined'
        ]

    def get_max_rate(self, obj):
        """최고 금리 반환"""
        options = obj.options.all()
        if options:
            max_option = max(options, key=lambda x: x.intr_rate2 or 0)
            return max_option.intr_rate2
        return None

    def get_is_joined(self, obj):
        """현재 사용자 가입 여부"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.subscribers.filter(user=request.user).exists()
        return False


class DepositProductDetailSerializer(serializers.ModelSerializer):
    """예적금 상품 상세 시리얼라이저"""
    options = DepositOptionSerializer(many=True, read_only=True)
    is_joined = serializers.SerializerMethodField()

    class Meta:
        model = DepositProduct
        fields = [
            'id', 'fin_co_no', 'fin_prdt_cd', 'kor_co_nm', 'fin_prdt_nm',
            'product_type', 'join_way', 'mtrt_int', 'spcl_cnd', 'join_deny',
            'join_member', 'etc_note', 'max_limit', 'dcls_strt_day',
            'dcls_end_day', 'options', 'is_joined'
        ]

    def get_is_joined(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.subscribers.filter(user=request.user).exists()
        return False


class UserProductSerializer(serializers.ModelSerializer):
    """사용자 가입 상품 시리얼라이저"""
    product = DepositProductListSerializer(read_only=True)
    option = DepositOptionSerializer(read_only=True)

    class Meta:
        model = UserProduct
        fields = ['id', 'product', 'option', 'joined_at', 'memo']


class GoldPriceSerializer(serializers.ModelSerializer):
    """금 시세 시리얼라이저"""
    class Meta:
        model = GoldPrice
        fields = ['date', 'close_price', 'open_price', 'high_price', 'low_price', 'volume']


class SilverPriceSerializer(serializers.ModelSerializer):
    """은 시세 시리얼라이저"""
    class Meta:
        model = SilverPrice
        fields = ['date', 'close_price', 'open_price', 'high_price', 'low_price', 'volume']