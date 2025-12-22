import requests
from decimal import Decimal
from django.conf import settings
from .models import DepositProduct, DepositOption, GoldPrice, SilverPrice


def fetch_deposit_products():
    """
    금융감독원 API에서 정기예금 상품 가져오기
    
    사용법:
        from finance.utils import fetch_deposit_products
        fetch_deposit_products()
    """
    api_key = settings.FSS_API_KEY
    
    if not api_key:
        print("❌ API 키가 없습니다. .env 파일에 FSS_API_KEY를 설정하세요.")
        return 0
    
    url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1'
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
    except Exception as e:
        print(f"❌ API 호출 실패: {e}")
        return 0
    
    result = data.get('result', {})
    base_list = result.get('baseList', [])
    option_list = result.get('optionList', [])
    
    if not base_list:
        print("❌ 데이터가 없습니다. API 키를 확인하세요.")
        print(f"응답: {data}")
        return 0
    
    print(f"📦 정기예금 {len(base_list)}개 발견")
    
    count = 0
    for item in base_list:
        product, created = DepositProduct.objects.update_or_create(
            fin_co_no=item.get('fin_co_no'),
            fin_prdt_cd=item.get('fin_prdt_cd'),
            defaults={
                'kor_co_nm': item.get('kor_co_nm', ''),
                'fin_prdt_nm': item.get('fin_prdt_nm', ''),
                'product_type': 'deposit',
                'join_way': item.get('join_way', ''),
                'mtrt_int': item.get('mtrt_int', ''),
                'spcl_cnd': item.get('spcl_cnd', ''),
                'join_deny': item.get('join_deny', ''),
                'join_member': item.get('join_member', ''),
                'etc_note': item.get('etc_note', ''),
                'max_limit': item.get('max_limit'),
                'dcls_strt_day': item.get('dcls_strt_day', ''),
                'dcls_end_day': item.get('dcls_end_day', ''),
            }
        )
        
        # 옵션(금리) 저장
        for opt in option_list:
            if opt.get('fin_prdt_cd') == item.get('fin_prdt_cd'):
                DepositOption.objects.update_or_create(
                    product=product,
                    save_trm=opt.get('save_trm', 0),
                    intr_rate_type=opt.get('intr_rate_type', 'S'),
                    defaults={
                        'intr_rate_type_nm': opt.get('intr_rate_type_nm', ''),
                        'intr_rate': opt.get('intr_rate'),
                        'intr_rate2': opt.get('intr_rate2'),
                    }
                )
        count += 1
    
    print(f"✅ 정기예금 {count}개 저장 완료!")
    return count


def fetch_saving_products():
    """
    금융감독원 API에서 적금 상품 가져오기
    
    사용법:
        from finance.utils import fetch_saving_products
        fetch_saving_products()
    """
    api_key = settings.FSS_API_KEY
    
    if not api_key:
        print("❌ API 키가 없습니다. .env 파일에 FSS_API_KEY를 설정하세요.")
        return 0
    
    url = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1'
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
    except Exception as e:
        print(f"❌ API 호출 실패: {e}")
        return 0
    
    result = data.get('result', {})
    base_list = result.get('baseList', [])
    option_list = result.get('optionList', [])
    
    if not base_list:
        print("❌ 데이터가 없습니다. API 키를 확인하세요.")
        print(f"응답: {data}")
        return 0
    
    print(f"📦 적금 {len(base_list)}개 발견")
    
    count = 0
    for item in base_list:
        product, created = DepositProduct.objects.update_or_create(
            fin_co_no=item.get('fin_co_no'),
            fin_prdt_cd=item.get('fin_prdt_cd'),
            defaults={
                'kor_co_nm': item.get('kor_co_nm', ''),
                'fin_prdt_nm': item.get('fin_prdt_nm', ''),
                'product_type': 'saving',
                'join_way': item.get('join_way', ''),
                'mtrt_int': item.get('mtrt_int', ''),
                'spcl_cnd': item.get('spcl_cnd', ''),
                'join_deny': item.get('join_deny', ''),
                'join_member': item.get('join_member', ''),
                'etc_note': item.get('etc_note', ''),
                'max_limit': item.get('max_limit'),
                'dcls_strt_day': item.get('dcls_strt_day', ''),
                'dcls_end_day': item.get('dcls_end_day', ''),
            }
        )
        
        # 옵션(금리) 저장
        for opt in option_list:
            if opt.get('fin_prdt_cd') == item.get('fin_prdt_cd'):
                DepositOption.objects.update_or_create(
                    product=product,
                    save_trm=opt.get('save_trm', 0),
                    intr_rate_type=opt.get('intr_rate_type', 'S'),
                    defaults={
                        'intr_rate_type_nm': opt.get('intr_rate_type_nm', ''),
                        'intr_rate': opt.get('intr_rate'),
                        'intr_rate2': opt.get('intr_rate2'),
                    }
                )
        count += 1
    
    print(f"✅ 적금 {count}개 저장 완료!")
    return count


def fetch_all_products():
    """
    정기예금 + 적금 모두 가져오기
    
    사용법:
        from finance.utils import fetch_all_products
        fetch_all_products()
    """
    print("=" * 50)
    print("🏦 금융상품 데이터 동기화 시작")
    print("=" * 50)
    
    deposit_count = fetch_deposit_products()
    saving_count = fetch_saving_products()
    
    print("=" * 50)
    print(f"📊 총 결과: 정기예금 {deposit_count}개, 적금 {saving_count}개")
    print(f"📊 DB 총 상품 수: {DepositProduct.objects.count()}개")
    print(f"📊 DB 총 옵션 수: {DepositOption.objects.count()}개")
    print("=" * 50)
    
    return {'deposit': deposit_count, 'saving': saving_count}


def get_product_summary():
    """
    현재 DB에 저장된 상품 요약 정보
    
    사용법:
        from finance.utils import get_product_summary
        get_product_summary()
    """
    deposit_count = DepositProduct.objects.filter(product_type='deposit').count()
    saving_count = DepositProduct.objects.filter(product_type='saving').count()
    option_count = DepositOption.objects.count()
    
    print("=" * 50)
    print("📊 현재 DB 상품 현황")
    print("=" * 50)
    print(f"정기예금: {deposit_count}개")
    print(f"적금: {saving_count}개")
    print(f"금리 옵션: {option_count}개")
    print("=" * 50)
    
    # 은행별 상품 수
    print("\n🏦 은행별 상품 수:")
    banks = DepositProduct.objects.values_list('kor_co_nm', flat=True).distinct()
    for bank in banks:
        count = DepositProduct.objects.filter(kor_co_nm=bank).count()
        print(f"  - {bank}: {count}개")
    
    return {
        'deposit': deposit_count,
        'saving': saving_count,
        'options': option_count
    }