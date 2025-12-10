import requests
from datetime import datetime
from django.conf import settings
from .models import Stock, DailyPrice

# 1. KRX API URL
STOCK_API_URL = "https://data-dbg.krx.co.kr/svc/apis/sto/stk_bydd_trd"
ETF_API_URL = "https://data-dbg.krx.co.kr/svc/apis/etp/etf_bydd_trd"

# 2. 인증키
AUTH_KEY = settings.KRX_API_KEY

def clean_int(value):
    if not value or value == '-': return 0
    return int(str(value).replace(",", ""))

def clean_float(value):
    if not value or value == '-': return 0.0
    return float(str(value).replace(",", ""))

def save_data(items, date_obj, asset_type):
    count = 0
    for item in items:
        try:
            # 1. Stock 정보 파싱 
            ticker = item.get("ISU_CD")
            name = item.get("ISU_NM")
            total_shares = clean_int(item.get("LIST_SHRS"))
            mkt_cap = clean_int(item.get("MKTCAP"))
            mkt_nm = item.get("MKT_NM", "ETF" if asset_type == 'ETF' else "KOSPI")

            # DB 저장 (Stock)
            stock, created = Stock.objects.update_or_create(
                ticker=ticker,
                defaults={
                    'name': name,
                    'asset_type': asset_type,
                    'market_type': mkt_nm,
                    'market_cap': mkt_cap,
                    'total_shares': total_shares,             
                }
            )

            # 2. DailyPrice 정보 파싱 
            trading_value = clean_int(item.get("ACC_TRDVAL"))
            change = clean_int(item.get("CMPPREVDD_PRC"))
            nav = clean_float(item.get("NAV")) if asset_type == 'ETF' else None

            # DB 저장 (DailyPrice)
            DailyPrice.objects.update_or_create(
                stock=stock,
                date=date_obj,
                defaults={
                    'close_price': clean_int(item.get("TDD_CLSPRC")),
                    'open_price': clean_int(item.get("TDD_OPNPRC")),
                    'high_price': clean_int(item.get("TDD_HGPRC")),
                    'low_price': clean_int(item.get("TDD_LWPRC")),
                    'volume': clean_int(item.get("ACC_TRDVOL")),
                    'trading_value': trading_value, 
                    'change': change,               
                    'nav': nav
                }
            )
            count += 1
        except Exception as e:
            print(f"Error saving {ticker}: {e}")
            continue
    return count


def fetch_krx_data(date_str):
    # 1. 날짜 포맷 변환
    db_date = datetime.strptime(date_str, "%Y%m%d").date()
    
    headers = {"AUTH_KEY": AUTH_KEY}
    params = {"basDd": date_str}

    print(f"=== {date_str} 데이터 수집 시작 ===")

    # 기존 시세 데이터 삭제 (초기화)
    deleted_count, _ = DailyPrice.objects.all().delete()
    print(f"🔄 기존 데이터 초기화: {db_date} 날짜의 데이터 {deleted_count}건 삭제됨.")

    # 2. 주식 데이터 요청
    try:
        res = requests.get(STOCK_API_URL, headers=headers, params=params)
        if res.status_code == 200:
            data = res.json().get("OutBlock_1", [])
            cnt = save_data(data, db_date, "STOCK")
            print(f"[주식] {cnt}개 저장 완료")
        else:
            print(f"[주식] API 요청 실패: {res.status_code}")
    except Exception as e:
        print(f"[주식] 에러: {e}")

    # 3. ETF 데이터 요청
    try:
        res = requests.get(ETF_API_URL, headers=headers, params=params)
        if res.status_code == 200:
            data = res.json().get("OutBlock_1", [])
            cnt = save_data(data, db_date, "ETF")
            print(f"[ETF] {cnt}개 저장 완료")
    except Exception as e:
        print(f"[ETF] 에러: {e}")
        
    print("=== 수집 종료 ===")