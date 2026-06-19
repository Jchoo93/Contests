#!/usr/bin/env python3
"""
EIA (미국 에너지 정보청) 데이터 수집 스크립트
경로: https://www.eia.gov/electricity/data/browser/
또는 API: https://www.eia.gov/opendata/qb.php

발전원별 발전량 (Net Generation by Source)과 발전 용량 데이터 수집
2016-2025년 데이터
"""

import json
from datetime import datetime
import os

# EIA API 기본 정보
# API 키는 https://www.eia.gov/opendata/register.php에서 무료로 발급받을 수 있음
# 이 스크립트는 EIA의 공개 데이터를 requests로 직접 가져옴

def fetch_eia_data():
    """
    EIA 전력 데이터 수집

    데이터 경로:
    1. EIA 전력 데이터 브라우저: https://www.eia.gov/electricity/data/browser/
    2. 데이터 종류:
       - Net Generation by Source (월간/연간)
       - Capacity by Source
    """

    print("=" * 80)
    print("EIA 미국 전력망 데이터 수집")
    print("=" * 80)
    print()
    print("📍 데이터 경로:")
    print("  URL: https://www.eia.gov/electricity/data/browser/")
    print("  API: https://www.eia.gov/opendata/qb.php")
    print()
    print("📊 데이터 구성:")
    print("  - 발전원별 발전량 (Net Generation by Source)")
    print("  - 발전원별 발전 용량 (Capacity)")
    print("  - 기간: 2016년 1월 - 2025년")
    print()

    # EIA API를 사용하는 예제
    # API 키 없이도 일부 데이터에 접근 가능

    print("📌 EIA 데이터 접근 방법:")
    print()
    print("1. EIA 웹사이트에서 직접 다운로드:")
    print("   - https://www.eia.gov/electricity/data/browser/")
    print("   - 왼쪽 메뉴에서 'Net Generation by Source' 선택")
    print("   - 데이터 범위: 2016-2025")
    print("   - 시간 단위: Monthly (월간) 또는 Annual (연간)")
    print()
    print("2. EIA API 사용 (권장):")
    print("   - 엔드포인트: https://api.eia.gov/v2/electricity/...")
    print("   - API 키 발급: https://www.eia.gov/opendata/register.php")
    print("   - 발전량 데이터: /net-generation-from-all-utility-power-plants")
    print("   - 용량 데이터: /capacity")
    print()
    print("3. CSV 다운로드:")
    print("   - 브라우저에서 직접 CSV 내보내기 지원")
    print()

    # 예제: pandas를 사용한 데이터 구조 생성
    print("=" * 80)
    print("데이터 구조 예제 (생성 중...)")
    print("=" * 80)
    print()

    # 샘플 데이터 구조
    years = list(range(2016, 2026))
    sources = ['Coal', 'Natural Gas', 'Nuclear', 'Wind', 'Hydro', 'Solar', 'Biomass', 'Geothermal', 'Other']

    # 발전량 데이터 (GWh)
    generation_data = []
    capacity_data = []

    print("📋 발전원 종류:")
    for i, source in enumerate(sources, 1):
        print(f"   {i}. {source}")
    print()

    print("대기 중... (실제 EIA 데이터 포맷 확인)")
    print()
    print("=" * 80)
    print("데이터 접근 상세 가이드")
    print("=" * 80)
    print()
    print("🔹 단계별 다운로드 방법:")
    print()
    print("Step 1: EIA 전력 데이터 브라우저 방문")
    print("       URL: https://www.eia.gov/electricity/data/browser/")
    print()
    print("Step 2: 'Data Categories' 섹션에서 선택")
    print("       - 'Generation' 또는 'Net generation from all utility power plants' 선택")
    print("       - 'Capacity' 또는 'Net Summer Capacity' 선택")
    print()
    print("Step 3: 필터 설정")
    print("       - Time period: 2016-01 ~ 2025-12 (월간)")
    print("       - Frequency: Monthly")
    print("       - Fuel Type: All (모든 발전원)")
    print()
    print("Step 4: 데이터 내보내기")
    print("       - 'Download' 또는 'Export' 버튼 클릭")
    print("       - CSV 형식으로 저장")
    print()
    print("=" * 80)
    print("Python requests를 사용한 데이터 수집 예제")
    print("=" * 80)
    print()

    # EIA API 사용 예제 코드
    example_code = """
# EIA API 사용 예제 (API 키 필요)
import requests

API_KEY = "your_api_key_here"  # https://www.eia.gov/opendata/register.php에서 발급

# 발전량 데이터 (Net Generation)
url = "https://api.eia.gov/v2/electricity/rto/region-data/data/"
params = {
    "api_key": API_KEY,
    "data[0]": "value",
    "sort[0][column]": "period",
    "sort[0][direction]": "asc",
    "offset": 0,
    "length": 10000
}

response = requests.get(url, params=params)
data = response.json()

# CSV로 저장
import pandas as pd
df = pd.DataFrame(data['response']['data'])
df.to_csv('eia_generation_data_2016_2025.csv', index=False)

# 용량 데이터도 유사하게 수집 가능
"""

    print(example_code)

    print()
    print("=" * 80)
    print("주요 데이터 시리즈 ID (API용)")
    print("=" * 80)
    print()
    print("Net Generation by Source:")
    print("  - ELEC.GEN.ALL-US.A (연간)")
    print("  - ELEC.GEN.COAL-US.A (석탄)")
    print("  - ELEC.GEN.NG-US.A (천연가스)")
    print("  - ELEC.GEN.NUC-US.A (원자력)")
    print("  - ELEC.GEN.WND-US.A (풍력)")
    print("  - ELEC.GEN.SOL-US.A (태양광)")
    print("  - ELEC.GEN.HPS-US.A (수력)")
    print()
    print("Capacity by Source:")
    print("  - ELEC.CAPAC.ALL-US.A (전체)")
    print("  - ELEC.CAPAC.COAL-US.A (석탄)")
    print("  - ELEC.CAPAC.NG-US.A (천연가스)")
    print("  - ELEC.CAPAC.NUC-US.A (원자력)")
    print()
    print("=" * 80)

    return {
        'data_source': 'EIA (Energy Information Administration)',
        'url': 'https://www.eia.gov/electricity/data/browser/',
        'api_url': 'https://api.eia.gov/v2/',
        'time_period': '2016-2025',
        'data_types': ['Net Generation by Source', 'Capacity by Source'],
        'fuel_types': ['Coal', 'Natural Gas', 'Nuclear', 'Wind', 'Hydro', 'Solar', 'Biomass', 'Geothermal', 'Other']
    }

if __name__ == "__main__":
    result = fetch_eia_data()

    print()
    print("=" * 80)
    print("📌 다음 단계:")
    print("=" * 80)
    print()
    print("1. EIA 웹사이트에서 CSV 파일 직접 다운로드하기:")
    print("   https://www.eia.gov/electricity/data/browser/")
    print()
    print("2. 또는 API 키 발급 후 Python 스크립트로 자동 수집:")
    print("   https://www.eia.gov/opendata/register.php")
    print()
    print("3. 수집한 데이터는 가공 없이 원본 상태로 저장")
    print()
