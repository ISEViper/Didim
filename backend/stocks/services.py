import requests
import pandas as pd
import FinanceDataReader as fdr
from datetime import datetime, timedelta
from django.conf import settings
from .models import Stock, DailyPrice, Chartprice

# 1. API URL 정의 (문서 기반 수정)
STOCK_API_URL = "https://data-dbg.krx.co.kr/svc/apis/sto/stk_bydd_trd"  
KOSDAQ_API_URL = "https://data-dbg.krx.co.kr/svc/apis/sto/ksq_bydd_trd" 
ETF_API_URL = "https://data-dbg.krx.co.kr/svc/apis/etp/etf_bydd_trd"    

# 2. 인증키
AUTH_KEY = settings.KRX_API_KEY

def clean_int(value):
    if not value or value == '-': return 0
    return int(str(value).replace(",", ""))

def clean_float(value):
    if not value or value == '-': return 0.0
    return float(str(value).replace(",", ""))

def save_data(items, date_obj, asset_type, explicit_market_type=None):
    count = 0
    for item in items:
        try:
            # 1. Stock 정보 파싱 
            ticker = item.get("ISU_CD") 
            name = item.get("ISU_NM")   
            total_shares = clean_int(item.get("LIST_SHRS")) 
            mkt_cap = clean_int(item.get("MKTCAP"))        
            
            if asset_type == 'ETF':
                mkt_nm = "ETF"
            else:
                mkt_nm = item.get("MKT_NM", explicit_market_type) 

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
            trading_value = clean_int(item.get("ACC_TRDVAL")) # [cite: 11]
            change = clean_int(item.get("CMPPREVDD_PRC"))     # [cite: 11]
            fluctuation_rate = clean_float(item.get("FLUC_RT")) # [cite: 11]
            nav = clean_float(item.get("NAV")) if asset_type == 'ETF' else None

            # DB 저장 (DailyPrice)
            DailyPrice.objects.update_or_create(
                stock=stock,
                date=date_obj,
                defaults={
                    'close_price': clean_int(item.get("TDD_CLSPRC")), # [cite: 11]
                    'open_price': clean_int(item.get("TDD_OPNPRC")),  # [cite: 11]
                    'high_price': clean_int(item.get("TDD_HGPRC")),   # [cite: 11]
                    'low_price': clean_int(item.get("TDD_LWPRC")),    # [cite: 11]
                    'volume': clean_int(item.get("ACC_TRDVOL")),      # [cite: 11]
                    'fluctuation_rate': fluctuation_rate,
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
    db_date = datetime.strptime(date_str, "%Y%m%d").date()
    
    headers = {"AUTH_KEY": AUTH_KEY}
    params = {"basDd": date_str} # 

    print(f"=== {date_str} 데이터 수집 시작 ===")

    # 해당 날짜 데이터 초기화
    deleted_count, _ = DailyPrice.objects.filter(date=db_date).delete()
    print(f"🔄 기존 데이터 초기화: {db_date} 날짜의 데이터 {deleted_count}건 삭제됨.")

    # 1. KOSPI 수집
    try:
        res = requests.get(STOCK_API_URL, headers=headers, params=params)
        if res.status_code == 200:
            data = res.json().get("OutBlock_1", [])
            cnt = save_data(data, db_date, "STOCK", explicit_market_type="KOSPI")
            print(f"[KOSPI] {cnt}개 저장 완료")
        else:
            print(f"[KOSPI] API 요청 실패: {res.status_code}")
    except Exception as e:
        print(f"[KOSPI] 에러: {e}")

    # 2. KOSDAQ 수집
    try:
        res = requests.get(KOSDAQ_API_URL, headers=headers, params=params) # 
        if res.status_code == 200:
            data = res.json().get("OutBlock_1", [])
            cnt = save_data(data, db_date, "STOCK", explicit_market_type="KOSDAQ")
            print(f"[KOSDAQ] {cnt}개 저장 완료")
        else:
            print(f"[KOSDAQ] API 요청 실패: {res.status_code}")
    except Exception as e:
        print(f"[KOSDAQ] 에러: {e}")

    # 3. ETF 수집
    try:
        res = requests.get(ETF_API_URL, headers=headers, params=params)
        if res.status_code == 200:
            data = res.json().get("OutBlock_1", [])
            cnt = save_data(data, db_date, "ETF")
            print(f"[ETF] {cnt}개 저장 완료")
    except Exception as e:
        print(f"[ETF] 에러: {e}")
        
    print("=== 수집 종료 ===")

def update_chart_data(ticker, period_year=5):
    try:
        stock = Stock.objects.get(ticker=ticker)
    except Stock.DoesNotExist:
        return

    Chartprice.objects.filter(stock=stock).delete()

    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=365 * period_year)

    try:
        df = fdr.DataReader(f'NAVER:{ticker}', start_date)
        
    except Exception as e:
        print(f"{stock.name}({ticker}) FDR 호출 실패: {e}")
        return

    if df is None or df.empty:
        print(f"{stock.name}({ticker}) 데이터 없음 (Empty DataFrame)")
        return

    df = df.dropna(subset=['Close']) 

    chart_prices = []
    
    try:
        for date, row in df.iterrows():
            close_val = row['Close']
            if pd.isna(close_val) or close_val == 0:
                continue

            chart_prices.append(Chartprice(
                stock=stock,
                date=date.date(),
                close_price=int(float(close_val))
            ))

        if chart_prices:
            Chartprice.objects.bulk_create(chart_prices)
            print(f"{stock.name}({ticker}) 차트 업데이트 완료 ({len(chart_prices)}건)")
        else:
            print(f"{stock.name}({ticker}) 유효한 차트 데이터가 없습니다.")
        
    except Exception as e:
        print(f"{stock.name}({ticker}) DB 저장 실패: {e}")