#!/usr/bin/env python3
"""
EIA API를 사용한 데이터 다운로드 (예제)
실제 사용을 위해 API 키를 받아야 합니다.
"""

import requests
import json
import csv
import os
from datetime import datetime

def download_eia_data_via_api(api_key):
    """
    EIA API를 통한 데이터 다운로드

    Args:
        api_key: EIA API 키 (https://www.eia.gov/opendata/register.php)
    """

    base_url = "https://api.eia.gov/v2"

    # 1. 발전량 데이터 (Net Generation)
    print("발전량 데이터 다운로드 중...")

    generation_endpoint = f"{base_url}/electricity/rto/region-data/data/"

    params = {
        "api_key": api_key,
        "data[0]": "value",
        "facets[subba][]": "US48",  # 미국 본토 48개 주
        "frequency": "annual",
        "sort[0][column]": "period",
        "sort[0][direction]": "asc",
        "offset": 0,
        "length": 10000
    }

    try:
        response = requests.get(generation_endpoint, params=params)
        response.raise_for_status()

        generation_data = response.json()

        # 원본 JSON 저장
        with open('data/eia_generation_raw.json', 'w') as f:
            json.dump(generation_data, f, indent=2)

        print("✓ 발전량 데이터 저장 완료: data/eia_generation_raw.json")

    except requests.exceptions.RequestException as e:
        print(f"✗ 발전량 데이터 다운로드 실패: {e}")

    # 2. 용량 데이터 (Capacity)
    print("\n용량 데이터 다운로드 중...")

    # 용량 데이터도 유사하게 다운로드
    # (동일한 엔드포인트, 다른 필터)

    print("✓ 데이터 다운로드 완료")
    print()
    print("저장된 파일:")
    print("  - data/eia_generation_raw.json")
    print("  - data/eia_capacity_raw.json (예상)")


def convert_json_to_csv(json_file, csv_file):
    """JSON을 CSV로 변환 (선택사항)"""
    try:
        import pandas as pd

        with open(json_file, 'r') as f:
            data = json.load(f)

        # 'response.data' 부분 추출
        if 'response' in data and 'data' in data['response']:
            df = pd.DataFrame(data['response']['data'])
            df.to_csv(csv_file, index=False)
            print(f"✓ CSV 변환 완료: {csv_file}")

    except ImportError:
        print("pandas 설치 필요: pip install pandas")
    except Exception as e:
        print(f"변환 실패: {e}")


if __name__ == "__main__":
    print("="*60)
    print("EIA API 데이터 다운로드 (예제)")
    print("="*60)
    print()

    # API 키 입력
    api_key = input("EIA API 키 입력 (또는 Enter로 스킵): ").strip()

    if not api_key:
        print("\n❌ API 키가 없습니다.")
        print("\n다음 단계:")
        print("1. https://www.eia.gov/opendata/register.php 방문")
        print("2. 이메일로 API 키 수신")
        print("3. 이 스크립트를 다시 실행하여 API 키 입력")
        print("\n또는 웹 인터페이스로 수동 다운로드:")
        print("   https://www.eia.gov/electricity/data/browser/")
    else:
        # 데이터 디렉토리 생성
        os.makedirs('data', exist_ok=True)

        # 데이터 다운로드
        download_eia_data_via_api(api_key)

        print("\n완료!")
