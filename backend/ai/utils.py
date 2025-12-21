from google import genai
from django.conf import settings
import requests
import json
import re
from datetime import datetime
import pytz

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