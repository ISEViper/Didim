from google import genai
from django.conf import settings
import requests
import json
import re


def generate_stock_analysis(ticker, stock_name):
    url = "https://gms.ssafy.io/gmsapi/generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

    params = {
        'key': settings.GMS_API_KEY
    }

    headers = {
        'Content-Type': 'application/json'
    }

    system_prompt = f"""
    당신은 주식 투자 어드바이저 '디딤 AI'입니다.
    기업 '{stock_name} ({ticker})'를 분석하여 반드시 아래 JSON 포맷으로만 응답하세요.

    [Task 1: 디딤 Comment (종합 투자의견)]
    - action: '매수', '관망', '매도' 중 하나를 선택 (엄격 준수)
    - title: 투자의견을 한 줄로 요약 (예: "성장 잠재력이 높아요.")
    - reason: 투자자를 위한 친절한 설명 (해요체, 2문장 이내)

    [Task 2: 3줄 기업 요약]
    - summary_1: 기업 개용 및 주력 사업 모델
    - summary_2: 현재 시장 업황 및 주요 이슈
    - summary_3: 미래 성장 동력 및 전망

    [Task 3: 연관 테마 추천주 4선]
    - 분석 대상 기업과 섹터/테마가 유사한 국내 상장주 (KOSPI) 4개 선정
    - 단, 입력된 기업({stock_name})은 제외할 것
    - name: 기업명
    - code: 종목코드 (6자리)
    - reason: 추천 이유 요약

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

            raw_text = result['candidates'][0]['content']['parts'][0]['text']

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
    