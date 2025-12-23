from google import genai
from django.conf import settings
import requests
import json
import re
from datetime import datetime
import pytz
from .constants import get_choice_text

def generate_stock_analysis(ticker, stock_name, asset_type="STOCK"):
    """
    ticker: 종목코드
    stock_name: 종목명
    asset_type: 'STOCK' (개별주) 또는 'ETF' (상장지수펀드)
    """
    url = "https://gms.ssafy.io/gmsapi/generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

    params = {
        'key': settings.GMS_API_KEY
    }

    headers = {
        'Content-Type': 'application/json'
    }

    korea_tz = pytz.timezone('Asia/Seoul')
    now = datetime.now(korea_tz).strftime("%Y년 %m월 %d일 %H시 기준")

    if asset_type == 'ETF':
        role_description = "당신은 ETF 상품 및 거시경제(Macro) 분석 전문가 '디딤 AI'입니다."
        
        search_instruction = f"""
        1. **Google Search 도구를 사용하여** ETF '{stock_name} ({ticker})'의 **기초지수(Underlying Index)**, **주요 구성 종목(Top Holdings)**, 그리고 **해당 섹터의 최신 시황**을 반드시 확인하세요.
        2. 개별 기업 이슈보다는 **산업 전반의 트렌드**, **금리/환율 등 거시경제 지표**가 이 ETF에 미치는 영향을 분석하세요.
        """

        task2_guide = """
        [Task 2: 3줄 ETF 요약]
        - summary_1: 이 ETF가 추종하는 기초지수 설명 및 주요 구성 종목(Top Holdings) 소개
        - summary_2: 해당 섹터/테마의 현재 시장 분위기 및 최근 이슈 (예: 반도체 업황 둔화, 금리 인하 수혜 등)
        - summary_3: 투자 매력도 및 향후 해당 섹터 전망
        """

        task3_guide = f"""
        [Task 3: 연관 ETF/종목 추천 4선]
        - 분석 대상 ETF와 유사한 테마의 **경쟁 ETF** 혹은 해당 ETF 내 **비중이 가장 높은 대장주**를 섞어서 4개 선정
        - 단, 입력된 ETF({stock_name})는 제외할 것
        - name: ETF/종목명
        - code: 종목코드 (6자리)
        - reason: 추천 이유 (예: "동일 테마의 경쟁 상품", "해당 ETF의 핵심 편입 종목")
        """
    
    else:
        role_description = "당신은 주식 종목 분석 및 투자 어드바이저 '디딤 AI'입니다."
        
        search_instruction = f"""
        1. **Google Search 도구를 사용하여** 기업 '{stock_name} ({ticker})'의 최신 뉴스, 실시간 주가 흐름, 최근 공시를 반드시 확인하세요.
        2. 기업의 **실적(매출, 영업이익)**, **신규 계약**, **경영진 이슈** 등을 중점적으로 검색하세요.
        """

        task2_guide = """
        [Task 2: 3줄 기업 요약]
        - summary_1: 기업 개요 및 주력 사업 모델 (무엇을 팔아 돈을 버는가)
        - summary_2: 현재 시장 업황 및 회사의 최근 핵심 이슈 (최신 뉴스 반영)
        - summary_3: 미래 성장 동력(신사업) 및 실적 전망
        """

        task3_guide = f"""
        [Task 3: 연관 테마 추천주 4선]
        - 분석 대상 기업과 섹터/테마가 유사하거나 경쟁 관계에 있는 **국내 상장주** 4개 선정
        - 단, 입력된 기업({stock_name})은 제외할 것
        - name: 기업명
        - code: 종목코드 (6자리)
        - reason: 추천 이유 요약
        """

    system_prompt = f"""
    {role_description}
    현재 시각은 **{now}** 입니다.

    [필수 지침 - 최신성 강제]
    {search_instruction}
    3. 당신의 학습 데이터가 아닌, **검색된 최신 정보(오늘 포함 최근 1주일 이내)**를 바탕으로 분석하세요.
    4. 최신 이슈(실적 발표, 계약 체결, 정책 변화 등)가 있다면 투자의견(reason)에 구체적으로 언급하세요.

    분석 후 반드시 아래 JSON 포맷으로만 응답하세요.

    [Task 1: 디딤 Comment (종합 투자의견)]
    - action: '매수', '관망', '매도' 중 하나를 선택 (최신 뉴스 호재/악재 반영 필수)
    - title: 투자의견을 한 줄로 요약 (ETF의 경우 섹터 전망 위주)
    - reason: 투자자를 위한 친절한 설명 (해요체, 2문장 이내)

    {task2_guide}

    {task3_guide}

    [JSON Output Schema]
    {{
      "opinion": {{
        "action": "매수",
        "title": "...",
        "reason": "..."
      }},
      "summary": {{
        "summary_1": "...",
        "summary_2": "...",
        "summary_3": "..."
      }},
      "related_stocks": [
        {{ "name": "...", "code": "...", "reason": "..." }},
        {{ "name": "...", "code": "...", "reason": "..." }},
        {{ "name": "...", "code": "...", "reason": "..." }},
        {{ "name": "...", "code": "..." }}
      ]
    }}
    """

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": system_prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.3,
            "responseMimeType": "application/json"
        }
    }

    try:
        response = requests.post(url, params=params, headers=headers, json=payload)

        if response.status_code == 200:
            result = response.json()
            
            if 'candidates' not in result or not result['candidates']:
                print("Gemini API Error: No candidates returned.")
                return None
            
            content_parts = result['candidates'][0]['content']['parts']
            raw_text = ""
            
            for part in content_parts:
                if 'text' in part:
                    raw_text += part['text']


            cleaned_text = re.sub(r"```json|```", "", raw_text).strip()

            parsed_data = json.loads(cleaned_text)

            return parsed_data
        
        else:
            print(f"API Request Failed: {response.status_code}, {response.text}")
            return None

    except json.JSONDecodeError:
        print("JSON Parsing Error: AI did not return valid JSON.")
        return None
    except Exception as e:
        print(f"Error calling SSAFY Gemini API: {e}")
        return None
    
    
def generate_finance_recommendation(user_survey, deposit_products, stocks):
    """
    금융 성향 설문 결과를 바탕으로 AI 추천 생성
    
    Args:
        user_survey: UserFinanceSurvey 인스턴스
        deposit_products: 예적금 상품 리스트 (dict)
        stocks: 주식 종목 리스트 (dict)
    
    Returns:
        dict: AI 추천 결과
    """
    url = "https://gms.ssafy.io/gmsapi/generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent"
    
    params = {
        'key': settings.GMS_API_KEY
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    korea_tz = pytz.timezone('Asia/Seoul')
    now = datetime.now(korea_tz).strftime("%Y년 %m월 %d일 %H시 기준")
    
    # 자산 정보
    total_assets = user_survey.savings + user_survey.investment
    savings_ratio = round(user_survey.savings / total_assets * 100, 1) if total_assets > 0 else 0
    investment_ratio = round(user_survey.investment / total_assets * 100, 1) if total_assets > 0 else 0
    
    # 설문 응답 텍스트 변환
    q2_text = get_choice_text('q2_goal', user_survey.q2_goal)
    q3_text = get_choice_text('q3_period', user_survey.q3_period)
    q4_text = get_choice_text('q4_knowledge', user_survey.q4_knowledge)
    q5_text = get_choice_text('q5_experience', user_survey.q5_experience)
    q6_text = get_choice_text('q6_expected_return', user_survey.q6_expected_return)
    q7_text = get_choice_text('q7_risk_tolerance', user_survey.q7_risk_tolerance)
    q8_text = get_choice_text('q8_monthly_saving', user_survey.q8_monthly_saving)
    q9_text = get_choice_text('q9_loss_reaction', user_survey.q9_loss_reaction)
    q10_text = get_choice_text('q10_interest', user_survey.q10_interest)
    
    # 예적금 상품 목록 문자열
    deposit_list_str = "\n".join([
        f"- ID:{p['id']}, {p['kor_co_nm']} {p['fin_prdt_nm']}, 최고금리: {p['max_rate']}%, 유형: {'예금' if p['product_type'] == 'deposit' else '적금'}"
        for p in deposit_products[:30]  # 상위 30개만
    ])
    
    # 주식 종목 목록 문자열
    stock_list_str = "\n".join([
        f"- TICKER:{s['ticker']}, {s['name']}, 유형: {s.get('asset_type', 'STOCK')}"
        for s in stocks[:50]
    ])
    
    system_prompt = f"""
당신은 개인 맞춤형 자산관리 어드바이저 '디딤 AI'입니다.
현재 시각은 **{now}** 입니다.

[사용자 자산 정보]
- 입출금/저축: {user_survey.savings:,}원 ({savings_ratio}%)
- 투자 자산: {user_survey.investment:,}원 ({investment_ratio}%)
- 총 자산: {total_assets:,}원
- 연봉: {user_survey.income:,}원

[설문 결과]
1. 금융 목표: {q2_text}
2. 투자 기간: {q3_text}
3. 금융 지식: {q4_text}
4. 투자 경험: {q5_text}
5. 기대 수익률: {q6_text}
6. 손실 감내: {q7_text}
7. 월 저축 여력: {q8_text}
8. 손실 시 반응: {q9_text}
9. 관심 분야: {q10_text}

[추천 가능한 예적금 상품 목록]
{deposit_list_str}

[추천 가능한 주식 종목 목록]
{stock_list_str}

[분석 및 추천 요청]
위 정보를 종합하여 사용자에게 맞춤형 금융 조언과 상품 추천을 제공하세요.

1. **투자자 유형 진단**: 5가지 유형(안정형, 안정추구형, 위험중립형, 적극투자형, 공격투자형) 중 하나로 분류
2. **자산 배분 제안**: 현재 자산 구성과 비교하여 추천 자산 배분 비율 제안
3. **핵심 조언**: 사용자의 금융 목표 달성을 위한 구체적 조언 3가지
4. **예적금 추천**: 위 목록에서 사용자에게 적합한 상품 3개 선택 (반드시 목록에 있는 ID 사용)
5. **주식 추천**: 위 목록에서 사용자에게 적합한 종목 3개 선택 (반드시 목록에 있는 ID 사용)

반드시 아래 JSON 포맷으로만 응답하세요. 다른 텍스트는 포함하지 마세요.

{{
  "investor_type": {{
    "type": "안정형/안정추구형/위험중립형/적극투자형/공격투자형 중 하나",
    "title": "투자 성향을 나타내는 한 줄 제목",
    "description": "사용자 성향에 대한 친근한 설명 (2~3문장, 해요체)"
  }},
  "asset_allocation": {{
    "current": {{
      "savings": {savings_ratio},
      "investment": {investment_ratio}
    }},
    "recommended": {{
      "savings": 추천_저축_비율(숫자),
      "investment": 추천_투자_비율(숫자),
      "other": 추천_기타_비율(숫자)
    }},
    "gap_analysis": "현재와 추천 배분의 차이에 대한 분석 (1~2문장)"
  }},
  "advice": {{
    "summary": "전체 조언 요약 (2~3문장, 해요체)",
    "details": [
      "구체적 조언 1",
      "구체적 조언 2",
      "구체적 조언 3"
    ]
  }},
  "recommended_deposits": {{
    "ids": [선택한_예적금_ID_1, 선택한_예적금_ID_2, 선택한_예적금_ID_3],
    "reason": "이 상품들을 추천하는 이유 (1~2문장)"
  }},
  "recommended_stocks": {{
    "tickers": ["선택한_주식_TICKER_1", "선택한_주식_TICKER_2", "선택한_주식_TICKER_3"],
    "reason": "이 종목들을 추천하는 이유 (1~2문장)"
}}
}}
"""

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": system_prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.3,
            "responseMimeType": "application/json"
        }
    }

    try:
        response = requests.post(url, params=params, headers=headers, json=payload)

        if response.status_code == 200:
            result = response.json()
            
            if 'candidates' not in result or not result['candidates']:
                print("Gemini API Error: No candidates returned.")
                return None
            
            content_parts = result['candidates'][0]['content']['parts']
            raw_text = ""
            
            for part in content_parts:
                if 'text' in part:
                    raw_text += part['text']

            cleaned_text = re.sub(r"```json|```", "", raw_text).strip()
            parsed_data = json.loads(cleaned_text)

            return parsed_data
        
        else:
            print(f"API Request Failed: {response.status_code}, {response.text}")
            return None

    except json.JSONDecodeError as e:
        print(f"JSON Parsing Error: {e}")
        return None
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return None