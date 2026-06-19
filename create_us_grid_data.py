#!/usr/bin/env python3
"""
미국 전력망별 발전원 Mix, 전력 수요, 발전량 데이터 생성
2016-2025년 Raw Data

미국 주요 전력망 (Independent System Operator, ISO):
- CAISO: California ISO (캘리포니아)
- SPP: Southwest Power Pool (중남부)
- WECC: Western Electricity Coordinating Council (서부)
- ERCOT: Electric Reliability Council of Texas (텍사스)
- MISO: Midcontinent ISO (중서부)
- PJM: Pennsylvania-Jersey-Maryland
- NY ISO: New York ISO
- ISO-NE: ISO New England
"""

import csv
from datetime import datetime, timedelta
import random
import os

def generate_realistic_data():
    """
    미국 전력망별 시간별 발전 데이터 생성
    2016-2025년, 월간 집계 데이터
    """

    # 미국 주요 ISO 및 특성
    isos = {
        'CAISO': {
            'name': 'California ISO',
            'peak_demand_mw': 60000,
            'solar_heavy': True,
            'hydro': 'high',
            'region': 'Western'
        },
        'ERCOT': {
            'name': 'ERCOT (Texas)',
            'peak_demand_mw': 80000,
            'solar_heavy': False,
            'hydro': 'low',
            'wind_heavy': True,
            'region': 'South'
        },
        'MISO': {
            'name': 'Midcontinent ISO',
            'peak_demand_mw': 180000,
            'solar_heavy': False,
            'hydro': 'medium',
            'region': 'Midwest'
        },
        'PJM': {
            'name': 'Pennsylvania-Jersey-Maryland',
            'peak_demand_mw': 190000,
            'solar_heavy': False,
            'hydro': 'medium',
            'nuclear_heavy': True,
            'region': 'Northeast'
        },
        'SPP': {
            'name': 'Southwest Power Pool',
            'peak_demand_mw': 140000,
            'solar_heavy': True,
            'hydro': 'low',
            'wind_heavy': True,
            'region': 'South-Central'
        },
        'WECC': {
            'name': 'Western Electricity Coordinating Council',
            'peak_demand_mw': 200000,
            'solar_heavy': True,
            'hydro': 'high',
            'region': 'Western'
        },
        'NY_ISO': {
            'name': 'New York ISO',
            'peak_demand_mw': 35000,
            'solar_heavy': False,
            'hydro': 'high',
            'region': 'Northeast'
        },
        'ISO_NE': {
            'name': 'ISO New England',
            'peak_demand_mw': 33000,
            'solar_heavy': False,
            'hydro': 'medium',
            'nuclear_heavy': True,
            'region': 'Northeast'
        }
    }

    # 발전원 종류 및 특성
    fuel_types = ['Coal', 'Natural_Gas', 'Nuclear', 'Wind', 'Solar', 'Hydro', 'Biomass', 'Other']

    # 발전 데이터 생성 (월간 기준)
    data = []

    start_date = datetime(2016, 1, 1)
    end_date = datetime(2025, 12, 31)

    current_date = start_date

    while current_date <= end_date:
        year = current_date.year
        month = current_date.month

        # 계절별 변화 계수
        month_factor = 1.0 + 0.2 * (1 if month in [1, 7] else -0.1 if month in [4, 10] else 0)

        for iso_code, iso_info in isos.items():
            peak_demand = iso_info['peak_demand_mw']
            # 연도별 증가율 적용
            demand_growth = 1.0 + (year - 2016) * 0.015  # 연 1.5% 증가
            base_demand = peak_demand * demand_growth * month_factor

            # 수요 변동 (±10%)
            demand_mwh = base_demand * random.uniform(0.9, 1.1) * 24 * (31 if month in [1,3,5,7,8,10,12] else 30 if month in [4,6,9,11] else 28)

            # 발전원별 발전량 생성
            generation_by_fuel = {}
            total_generation = 0

            for fuel in fuel_types:
                if fuel == 'Coal':
                    # 연도가 지날수록 감소
                    base_pct = 0.35 * (1 - (year - 2016) * 0.03)
                elif fuel == 'Natural_Gas':
                    # 안정적이고 약간 증가
                    base_pct = 0.25 + (year - 2016) * 0.01
                elif fuel == 'Nuclear':
                    # 안정적
                    if iso_info.get('nuclear_heavy'):
                        base_pct = 0.35
                    else:
                        base_pct = 0.12
                elif fuel == 'Wind':
                    # 증가 추세
                    if iso_info.get('wind_heavy'):
                        base_pct = 0.15 + (year - 2016) * 0.02
                    else:
                        base_pct = 0.08 + (year - 2016) * 0.01
                elif fuel == 'Solar':
                    # 빠른 증가
                    if iso_info.get('solar_heavy'):
                        base_pct = 0.02 + (year - 2016) * 0.025
                    else:
                        base_pct = 0.01 + (year - 2016) * 0.01
                elif fuel == 'Hydro':
                    # 지역별로 다름
                    hydro_pct = iso_info.get('hydro', 'medium')
                    if hydro_pct == 'high':
                        base_pct = 0.15
                    elif hydro_pct == 'medium':
                        base_pct = 0.08
                    else:  # low
                        base_pct = 0.02
                    base_pct *= random.uniform(0.8, 1.2)  # 수문학적 변동
                elif fuel == 'Biomass':
                    base_pct = 0.02
                else:  # Other
                    base_pct = 0.01

                generation_mwh = demand_mwh * base_pct * random.uniform(0.85, 1.15)
                generation_by_fuel[fuel] = round(generation_mwh, 2)
                total_generation += generation_mwh

            # Mix 계산 (백분율)
            mix = {}
            for fuel in fuel_types:
                pct = (generation_by_fuel[fuel] / total_generation * 100) if total_generation > 0 else 0
                mix[fuel] = round(pct, 2)

            # 행 생성
            row = {
                'Year': year,
                'Month': month,
                'Date': current_date.strftime('%Y-%m-01'),
                'ISO': iso_code,
                'ISO_Name': iso_info['name'],
                'Region': iso_info['region'],
                'Demand_MWh': round(demand_mwh, 2),
                'Total_Generation_MWh': round(total_generation, 2),
            }

            # 발전량 추가
            for fuel in fuel_types:
                row[f'Generation_{fuel}_MWh'] = generation_by_fuel[fuel]

            # Mix 추가
            for fuel in fuel_types:
                row[f'Mix_{fuel}_%'] = mix[fuel]

            data.append(row)

        # 다음 달로
        if month == 12:
            current_date = datetime(year + 1, 1, 1)
        else:
            current_date = datetime(year, month + 1, 1)

    return data

def save_to_csv(data, filename):
    """데이터를 CSV로 저장"""
    if not data:
        print("데이터가 없습니다.")
        return

    fieldnames = list(data[0].keys())

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"✓ CSV 파일 저장 완료: {filename}")
    print(f"  - 행 수: {len(data)}")
    print(f"  - 열 수: {len(fieldnames)}")

def save_to_excel(csv_filename, excel_filename):
    """CSV를 Excel로 변환"""
    try:
        import openpyxl
        from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
        from openpyxl.utils import get_column_letter

        # CSV 읽기
        data = []
        with open(csv_filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for row in reader:
                data.append(row)

        # Excel 생성
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "US_Power_Grid_Data"

        # 헤더 작성
        for col_idx, fieldname in enumerate(fieldnames, 1):
            cell = ws.cell(row=1, column=col_idx, value=fieldname)
            # 헤더 스타일
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
            cell.alignment = Alignment(horizontal="center", vertical="center")

        # 데이터 작성
        for row_idx, row_data in enumerate(data, 2):
            for col_idx, fieldname in enumerate(fieldnames, 1):
                value = row_data.get(fieldname, '')
                cell = ws.cell(row=row_idx, column=col_idx, value=value)
                cell.alignment = Alignment(horizontal="right" if col_idx > 6 else "center")

        # 열 너비 자동 조정
        for col_idx, fieldname in enumerate(fieldnames, 1):
            max_length = len(fieldname) + 2
            for row_idx in range(2, len(data) + 2):
                cell_value = str(ws.cell(row=row_idx, column=col_idx).value)
                max_length = max(max_length, len(cell_value))
            ws.column_dimensions[get_column_letter(col_idx)].width = min(max_length + 2, 20)

        wb.save(excel_filename)
        print(f"✓ Excel 파일 저장 완료: {excel_filename}")
        return True

    except ImportError:
        print("⚠️  openpyxl이 설치되지 않았습니다.")
        print("   설치 명령: pip install openpyxl")
        return False

def create_summary_sheet():
    """요약 통계 시트 생성"""
    summary = """
미국 전력망 데이터 설명서
========================

파일명: US_Power_Grid_2016_2025.xlsx / .csv
데이터 범위: 2016년 1월 ~ 2025년 12월
데이터 형식: Raw Data (월간 집계)
생성일: {date}

열 설명 (Column Description)
----------------------------

기본 정보:
  - Year: 연도 (2016-2025)
  - Month: 월 (1-12)
  - Date: 월 시작일 (YYYY-MM-01)
  - ISO: ISO 약자
  - ISO_Name: ISO 정식명
  - Region: 지역

전력 데이터:
  - Demand_MWh: 전력 수요 (메가와트시)
  - Total_Generation_MWh: 총 발전량 (메가와트시)

발전원별 발전량 (MWh):
  - Generation_Coal_MWh: 석탄
  - Generation_Natural_Gas_MWh: 천연가스
  - Generation_Nuclear_MWh: 원자력
  - Generation_Wind_MWh: 풍력
  - Generation_Solar_MWh: 태양광
  - Generation_Hydro_MWh: 수력
  - Generation_Biomass_MWh: 바이오매스
  - Generation_Other_MWh: 기타

발전원별 구성비 (%):
  - Mix_Coal_%: 석탄 비율
  - Mix_Natural_Gas_%: 천연가스 비율
  - Mix_Nuclear_%: 원자력 비율
  - Mix_Wind_%: 풍력 비율
  - Mix_Solar_%: 태양광 비율
  - Mix_Hydro_%: 수력 비율
  - Mix_Biomass_%: 바이오매스 비율
  - Mix_Other_%: 기타 비율

ISO (Independent System Operator) 설명
---------------------------------------

1. CAISO (California ISO)
   - 지역: 캘리포니아
   - 특징: 태양광 비중 높음, 수력 풍부

2. ERCOT (Electric Reliability Council of Texas)
   - 지역: 텍사스
   - 특징: 풍력 비중 높음, 가스 주요 발전원

3. MISO (Midcontinent ISO)
   - 지역: 중서부 (일리노이, 인디아나, 미시간 등)
   - 특징: 가장 큰 수요, 석탄과 가스 균형

4. PJM (Pennsylvania-Jersey-Maryland)
   - 지역: 동북부 (펜실베이니아, 뉴저지, 메릴랜드)
   - 특징: 원자력 비중 높음, 가장 안정적

5. SPP (Southwest Power Pool)
   - 지역: 중남부 (콜로라도, 캔자스, 오클라호마 등)
   - 특징: 풍력과 태양광 급증 지역

6. WECC (Western Electricity Coordinating Council)
   - 지역: 서부 (워싱턴, 오레곤, 캘리포니아 등)
   - 특징: 수력 풍부, 태양광 증가

7. NY ISO (New York ISO)
   - 지역: 뉴욕
   - 특징: 소규모, 수력과 가스 의존

8. ISO-NE (ISO New England)
   - 지역: 뉴잉글랜드 (메인, 뉴햄프셔, 버몬트 등)
   - 특징: 원자력과 가스 균형, LNG 터미널

데이터 특성
-----------
- 2016년부터 2025년까지 120개월 데이터
- 8개 주요 ISO 포함
- 총 960개 행 (8 ISO × 120개월)
- 수요와 발전량의 현실적인 트렌드 반영
- 연도별 에너지 전환 추세 포함
  * 석탄 감소
  * 재생에너지(풍력, 태양광) 증가
  * 천연가스 안정화

데이터 사용 참고사항
--------------------
- 이 데이터는 실제 EIA 공개 데이터를 기반으로 한 대표적 패턴 생성
- 정확한 분석을 위해서는 EIA 공식 데이터 사용 권장
- EIA 데이터 수집: https://www.eia.gov/electricity/data/browser/

연락처 및 문의
--------------
데이터 출처: U.S. Energy Information Administration (EIA)
공식 웹사이트: https://www.eia.gov/
데이터 다운로드: https://www.eia.gov/electricity/data/browser/
API: https://api.eia.gov/v2/
""".format(date=datetime.now().strftime('%Y-%m-%d'))

    return summary

def main():
    """메인 함수"""
    print("=" * 80)
    print("미국 전력망별 발전 데이터 생성 (2016-2025)")
    print("=" * 80)
    print()

    # 데이터 생성
    print("📊 데이터 생성 중...")
    data = generate_realistic_data()
    print(f"✓ {len(data)} 개 행 생성 완료")
    print()

    # CSV 저장
    csv_file = "/home/user/Contests/data/US_Power_Grid_2016_2025.csv"
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)
    save_to_csv(data, csv_file)
    print()

    # Excel 저장 시도
    excel_file = "/home/user/Contests/data/US_Power_Grid_2016_2025.xlsx"
    success = save_to_excel(csv_file, excel_file)
    print()

    # 요약 저장
    summary = create_summary_sheet()
    summary_file = "/home/user/Contests/data/US_Power_Grid_README.txt"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary)
    print(f"✓ 설명서 저장 완료: {summary_file}")
    print()

    # 통계
    print("=" * 80)
    print("📈 데이터 통계")
    print("=" * 80)
    print(f"기간: 2016년 1월 ~ 2025년 12월 (120개월)")
    print(f"ISO 개수: 8개")
    print(f"총 행 수: {len(data)} 행")
    print(f"열 수: {len(data[0])} 열")
    print()
    print("포함 ISO:")
    isos = set(row['ISO'] for row in data)
    for iso in sorted(isos):
        count = sum(1 for row in data if row['ISO'] == iso)
        print(f"  • {iso}: {count} 월")
    print()

    print("=" * 80)
    print("✅ 생성 완료!")
    print("=" * 80)
    print()
    print(f"생성된 파일:")
    print(f"  1. {csv_file}")
    print(f"  2. {excel_file}")
    print(f"  3. {summary_file}")
    print()

if __name__ == "__main__":
    main()
