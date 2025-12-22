from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings


class DepositProduct(models.Model):
    """예금 상품"""
    PRODUCT_TYPE_CHOICES = [
        ('deposit', '정기예금'),
        ('saving', '적금'),
    ]

    fin_co_no = models.CharField(max_length=20, verbose_name='금융회사 코드')
    fin_prdt_cd = models.CharField(max_length=50, verbose_name='금융상품 코드')
    kor_co_nm = models.CharField(max_length=100, verbose_name='금융회사명')
    fin_prdt_nm = models.CharField(max_length=200, verbose_name='금융상품명')
    product_type = models.CharField(
        max_length=20,
        choices=PRODUCT_TYPE_CHOICES,
        default='deposit',
        verbose_name='상품유형'
    )
    join_way = models.TextField(blank=True, verbose_name='가입방법')
    mtrt_int = models.TextField(blank=True, verbose_name='만기 후 이자율')
    spcl_cnd = models.TextField(blank=True, verbose_name='우대조건')
    join_deny = models.CharField(max_length=10, blank=True, verbose_name='가입제한')
    join_member = models.TextField(blank=True, verbose_name='가입대상')
    etc_note = models.TextField(blank=True, verbose_name='기타 유의사항')
    max_limit = models.BigIntegerField(null=True, blank=True, verbose_name='최고한도')
    dcls_strt_day = models.CharField(max_length=10, blank=True, null=True, verbose_name='공시 시작일')
    dcls_end_day = models.CharField(max_length=10, blank=True, null=True, verbose_name='공시 종료일')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '예적금 상품'
        verbose_name_plural = '예적금 상품'
        unique_together = ['fin_co_no', 'fin_prdt_cd']

    def __str__(self):
        return f"[{self.kor_co_nm}] {self.fin_prdt_nm}"


class DepositOption(models.Model):
    """예적금 상품 옵션 (금리 정보)"""
    RATE_TYPE_CHOICES = [
        ('S', '단리'),
        ('M', '복리'),
    ]

    product = models.ForeignKey(
        DepositProduct,
        on_delete=models.CASCADE,
        related_name='options',
        verbose_name='상품'
    )
    intr_rate_type = models.CharField(
        max_length=10,
        choices=RATE_TYPE_CHOICES,
        verbose_name='저축금리 유형'
    )
    intr_rate_type_nm = models.CharField(max_length=20, verbose_name='저축금리 유형명')
    save_trm = models.IntegerField(verbose_name='저축기간(개월)')
    intr_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='기본금리'
    )
    intr_rate2 = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='최고금리'
    )

    class Meta:
        verbose_name = '예적금 옵션'
        verbose_name_plural = '예적금 옵션'

    def __str__(self):
        return f"{self.product.fin_prdt_nm} - {self.save_trm}개월"


class UserProduct(models.Model):
    """사용자 가입 상품"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='finance_products',
        verbose_name='사용자'
    )
    product = models.ForeignKey(
        DepositProduct,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='상품'
    )
    option = models.ForeignKey(
        DepositOption,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='선택 옵션'
    )
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name='가입일')
    memo = models.TextField(blank=True, verbose_name='메모')

    class Meta:
        verbose_name = '가입 상품'
        verbose_name_plural = '가입 상품'
        unique_together = ['user', 'product']

    def __str__(self):
        return f"{self.user.email} - {self.product.fin_prdt_nm}"


class GoldPrice(models.Model):
    """금 시세"""
    date = models.DateField(unique=True, verbose_name='날짜')
    close_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='종가')
    open_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='시가')
    high_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='고가')
    low_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='저가')
    volume = models.DecimalField(max_digits=15, decimal_places=3, verbose_name='거래량')

    class Meta:
        verbose_name = '금 시세'
        verbose_name_plural = '금 시세'
        ordering = ['-date']

    def __str__(self):
        return f"금 {self.date}: ${self.close_price}"


class SilverPrice(models.Model):
    """은 시세"""
    date = models.DateField(unique=True, verbose_name='날짜')
    close_price = models.DecimalField(max_digits=10, decimal_places=3, verbose_name='종가')
    open_price = models.DecimalField(max_digits=10, decimal_places=3, verbose_name='시가')
    high_price = models.DecimalField(max_digits=10, decimal_places=3, verbose_name='고가')
    low_price = models.DecimalField(max_digits=10, decimal_places=3, verbose_name='저가')
    volume = models.DecimalField(max_digits=15, decimal_places=3, verbose_name='거래량')

    class Meta:
        verbose_name = '은 시세'
        verbose_name_plural = '은 시세'
        ordering = ['-date']

    def __str__(self):
        return f"은 {self.date}: ${self.close_price}"