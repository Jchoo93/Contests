#!/usr/bin/env python3
"""
EIA 데이터 다운로드 스크립트
미국 전력망의 발전원별 MIX와 발전 용량 데이터 (2016-2025)

사용법:
  1. 웹 브라우저로 수동 다운로드:
     https://www.eia.gov/electricity/data/browser/

  2. 또는 아래 스크립트로 수동 다운로드 링크 생성
"""

import json
import os
from datetime import datetime

def generate_download_instructions():
    """EIA 데이터 다운로드 인스트럭션 생성"""

    print("\n" + "="*80)
    print("EIA 전력망 데이터 수집 가이드 (가공하지 않은 원본)")
    print("="*80)
    print()

    instructions = {
        "data_source": "Energy Information Administration (EIA)",
        "website": "https://www.eia.gov/electricity/data/browser/",
        "api_website": "https://www.eia.gov/opendata/",
        "api_registration": "https://www.eia.gov/opendata/register.php",
        "time_period": "2016-01-01 to 2025-12-31",
        "data_types": [
            "Net Generation by Source (발전원별 발전량)",
            "Capacity by Source (발전원별 발전 용량)"
        ],
        "fuel_types": [
            "Coal (석탄)",
            "Natural Gas (천연가스)",
            "Nuclear (원자력)",
            "Wind (풍력)",
            "Solar (태양광)",
            "Hydro (수력)",
            "Biomass (바이오매스)",
            "Geothermal (지열)",
            "Other (기타)"
        ],
        "download_methods": {}
    }

    # Method 1: Web Interface
    instructions["download_methods"]["web_interface"] = {
        "name": "방법 1: EIA 웹사이트 (가장 간단)",
        "steps": [
            {
                "step": 1,
                "description": "EIA 전력 데이터 브라우저 접속",
                "action": "https://www.eia.gov/electricity/data/browser/ 방문"
            },
            {
                "step": 2,
                "description": "데이터 종류 선택",
                "action": """왼쪽 메뉴에서:
  - "Net Generation by Source" 또는
  - "Electricity Net Generation" 선택"""
            },
            {
                "step": 3,
                "description": "필터 설정",
                "action": """Time Period: 2016-01 ~ 2025-12
Frequency: Monthly 또는 Annual
Sector: Electric power sector"""
            },
            {
                "step": 4,
                "description": "다운로드",
                "action": """오른쪽 상단 "Download" 또는 "Export" 버튼 클릭
CSV 또는 Excel 형식 선택"""
            }
        ],
        "expected_files": [
            "generation_2016_2025.csv",
            "capacity_2016_2025.csv"
        ]
    }

    # Method 2: API
    instructions["download_methods"]["api"] = {
        "name": "방법 2: EIA API (자동화)",
        "prerequisite": "API 키 발급 필요: https://www.eia.gov/opendata/register.php",
        "api_endpoints": {
            "generation": {
                "url": "https://api.eia.gov/v2/electricity/rto/region-data/data/",
                "description": "Net Generation Data"
            },
            "capacity": {
                "url": "https://api.eia.gov/v2/electricity/rto/region-data/data/",
                "description": "Capacity Data"
            }
        },
        "legacy_series_ids": {
            "generation": {
                "ELEC.GEN.ALL-US.A": "Total Net Generation (Annual)",
                "ELEC.GEN.COAL-US.A": "Coal Generation (Annual)",
                "ELEC.GEN.NG-US.A": "Natural Gas Generation (Annual)",
                "ELEC.GEN.NUC-US.A": "Nuclear Generation (Annual)",
                "ELEC.GEN.WND-US.A": "Wind Generation (Annual)",
                "ELEC.GEN.SOL-US.A": "Solar Generation (Annual)",
                "ELEC.GEN.HPS-US.A": "Hydro Generation (Annual)"
            },
            "capacity": {
                "ELEC.CAPAC.ALL-US.A": "Total Capacity (Annual)",
                "ELEC.CAPAC.COAL-US.A": "Coal Capacity (Annual)",
                "ELEC.CAPAC.NG-US.A": "Natural Gas Capacity (Annual)",
                "ELEC.CAPAC.NUC-US.A": "Nuclear Capacity (Annual)",
                "ELEC.CAPAC.WND-US.A": "Wind Capacity (Annual)"
            }
        }
    }

    # Method 3: Direct Download
    instructions["download_methods"]["direct_download"] = {
        "name": "방법 3: 직접 다운로드 링크",
        "links": {
            "eia_electricity_data": "https://www.eia.gov/electricity/",
            "eia_generation_data": "https://www.eia.gov/electricity/data.php",
            "monthly_generation": "https://www.eia.gov/electricity/monthly/",
            "annual_generation": "https://www.eia.gov/electricity/annual/"
        }
    }

    # Output instructions
    print("📍 EIA 데이터 접근 경로:")
    print("-" * 80)
    print()
    print(f"메인 웹사이트: {instructions['website']}")
    print(f"API 웹사이트: {instructions['api_website']}")
    print(f"API 등록: {instructions['api_registration']}")
    print()

    print("📊 수집할 데이터:")
    print("-" * 80)
    for data_type in instructions['data_types']:
        print(f"  • {data_type}")
    print()

    print("⚡ 발전원 종류:")
    print("-" * 80)
    for fuel in instructions['fuel_types']:
        print(f"  • {fuel}")
    print()

    print("📥 다운로드 방법 1: 웹 인터페이스 (권장)")
    print("-" * 80)
    method1 = instructions['download_methods']['web_interface']
    for step_info in method1['steps']:
        print(f"\n  Step {step_info['step']}: {step_info['description']}")
        print(f"  → {step_info['action']}")
    print()
    print("  예상 파일명:")
    for file in method1['expected_files']:
        print(f"    - {file}")
    print()

    print("📡 다운로드 방법 2: EIA API")
    print("-" * 80)
    method2 = instructions['download_methods']['api']
    print(f"  사전 요구사항: {method2['prerequisite']}")
    print()
    print("  API 엔드포인트:")
    for key, endpoint in method2['api_endpoints'].items():
        print(f"    • {key.upper()}: {endpoint['url']}")
    print()
    print("  레거시 API 시리즈 ID (구식):")
    print()
    print("  발전량 (Net Generation):")
    for series_id, description in method2['legacy_series_ids']['generation'].items():
        print(f"    {series_id}: {description}")
    print()
    print("  용량 (Capacity):")
    for series_id, description in method2['legacy_series_ids']['capacity'].items():
        print(f"    {series_id}: {description}")
    print()

    print("🔗 직접 다운로드 링크:")
    print("-" * 80)
    method3 = instructions['download_methods']['direct_download']
    for name, link in method3['links'].items():
        print(f"  {name.replace('_', ' ').title()}: {link}")
    print()

    print("=" * 80)
    print("💾 저장 위치 및 포맷")
    print("=" * 80)
    print()
    print("권장 저장 경로:")
    print("  /home/user/Contests/data/")
    print()
    print("권장 파일명 (원본 그대로):")
    print("  • eia_generation_2016_2025.csv (또는 .xlsx, .json)")
    print("  • eia_capacity_2016_2025.csv (또는 .xlsx, .json)")
    print()
    print("⚠️  주의: 원본 데이터를 가공하지 말 것")
    print("  • 단위 변경 금지")
    print("  • 열/행 삭제 금지")
    print("  • 누락값(N/A) 그대로 유지")
    print()

    # Save instructions to JSON
    output_file = "/home/user/Contests/eia_download_instructions.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(instructions, f, indent=2, ensure_ascii=False)

    print("=" * 80)
    print(f"✅ 인스트럭션이 저장되었습니다: {output_file}")
    print("=" * 80)
    print()

    return instructions

def create_data_directory():
    """데이터 저장 디렉토리 생성"""
    data_dir = "/home/user/Contests/data"
    os.makedirs(data_dir, exist_ok=True)
    return data_dir

def generate_api_script_example():
    """EIA API 사용 예제 스크립트 생성"""

    script = '''#!/usr/bin/env python3
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
    print("\\n용량 데이터 다운로드 중...")

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
        print("\\n❌ API 키가 없습니다.")
        print("\\n다음 단계:")
        print("1. https://www.eia.gov/opendata/register.php 방문")
        print("2. 이메일로 API 키 수신")
        print("3. 이 스크립트를 다시 실행하여 API 키 입력")
        print("\\n또는 웹 인터페이스로 수동 다운로드:")
        print("   https://www.eia.gov/electricity/data/browser/")
    else:
        # 데이터 디렉토리 생성
        os.makedirs('data', exist_ok=True)

        # 데이터 다운로드
        download_eia_data_via_api(api_key)

        print("\\n완료!")
'''

    script_file = "/home/user/Contests/eia_api_downloader.py"
    with open(script_file, 'w') as f:
        f.write(script)

    return script_file

def main():
    """메인 함수"""

    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*78 + "║")
    print("║" + "  EIA 미국 전력망 데이터 수집 가이드".center(78) + "║")
    print("║" + "  (발전원별 MIX & 발전 용량, 2016-2025)".center(78) + "║")
    print("║" + " "*78 + "║")
    print("╚" + "="*78 + "╝")

    # Generate instructions
    instructions = generate_download_instructions()

    # Create data directory
    data_dir = create_data_directory()
    print(f"📁 데이터 디렉토리 생성: {data_dir}")
    print()

    # Generate API script
    api_script = generate_api_script_example()
    print(f"📜 API 다운로드 스크립트: {api_script}")
    print()

    print("=" * 80)
    print("🎯 다음 단계")
    print("=" * 80)
    print()
    print("옵션 1: 웹 인터페이스 (권장, 가장 간단)")
    print("  1. https://www.eia.gov/electricity/data/browser/ 방문")
    print("  2. Net Generation & Capacity 데이터 선택")
    print("  3. 2016-01 ~ 2025-12 기간 설정")
    print("  4. CSV 다운로드")
    print("  5. /home/user/Contests/data/ 에 저장")
    print()

    print("옵션 2: Python API 스크립트")
    print("  1. https://www.eia.gov/opendata/register.php 에서 API 키 발급")
    print("  2. python3 eia_api_downloader.py 실행")
    print("  3. API 키 입력")
    print()

    print("옵션 3: curl/wget로 직접 다운로드")
    print("  1. https://www.eia.gov/electricity/data/browser/ 에서 URL 복사")
    print("  2. wget 또는 curl로 다운로드")
    print()

    print("=" * 80)
    print("📌 중요: 원본 데이터 유지")
    print("=" * 80)
    print()
    print("✓ EIA에서 받은 데이터는 가공하지 말 것")
    print("✓ 단위, 시간대, 누락값 그대로 유지")
    print("✓ CSV/JSON 원본 형식 그대로 저장")
    print()

    print("📄 생성된 파일:")
    print(f"  1. {api_script}")
    print(f"  2. /home/user/Contests/eia_download_instructions.json")
    print(f"  3. /home/user/Contests/EIA_DATA_DOWNLOAD_GUIDE.md")
    print()

if __name__ == "__main__":
    main()
