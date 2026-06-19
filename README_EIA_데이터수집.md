# EIA 미국 전력망 데이터 수집 가이드

## 📌 요청사항 요약
**목표**: EIA에서 미국의 전력망 발전원별 MIX와 발전 총 용량 데이터를 **2016년부터 2025년까지** 수집  
**형식**: 가공하지 않은 원본 데이터 상태  
**경로**: 어떤 경로로 들어가서 데이터를 수집했는지 명시

---

## 🌐 데이터 접근 경로

### 📍 메인 경로 (웹사이트)
```
EIA 전력 데이터 브라우저 (Electricity Data Browser)
https://www.eia.gov/electricity/data/browser/
```

### 📍 API 경로
```
EIA Open Data Portal
https://www.eia.gov/opendata/

API 엔드포인트: https://api.eia.gov/v2/electricity/...
API 키 발급: https://www.eia.gov/opendata/register.php (무료)
```

### 📍 직접 다운로드 경로
```
EIA 전력 데이터 페이지
https://www.eia.gov/electricity/

하위 링크들:
- https://www.eia.gov/electricity/data.php (발전 데이터)
- https://www.eia.gov/electricity/monthly/ (월간 데이터)
- https://www.eia.gov/electricity/annual/ (연간 데이터)
```

---

## 📊 수집할 데이터 종류

### 1️⃣ Net Generation by Source (발전원별 발전량)
- **단위**: MWh (메가와트시) 또는 GWh (기가와트시)
- **시간 범위**: 2016년 1월 ~ 2025년 12월
- **시간 단위**: Monthly (월간) 또는 Annual (연간)
- **발전원 분류**:
  - Coal (석탄)
  - Natural Gas (천연가스)
  - Nuclear (원자력)
  - Wind (풍력)
  - Solar (태양광)
  - Hydro (수력)
  - Biomass (바이오매스)
  - Geothermal (지열)
  - Other (기타 신재생에너지)

### 2️⃣ Capacity by Source (발전원별 발전 용량)
- **단위**: MW (메가와트) 또는 GW (기가와트)
- **시간 범위**: 2016년 ~ 2025년
- **시간 단위**: Annual (연간)
- **발전원 분류**: 위와 동일

---

## 🔍 상세 단계별 다운로드 방법

### 🥇 방법 1: 웹 인터페이스 (권장 - 가장 간단)

#### Step 1: 웹사이트 접속
```
https://www.eia.gov/electricity/data/browser/
```

#### Step 2: 좌측 메뉴에서 데이터 선택
```
발전량 선택:
- "Net Generation by Source" 또는
- "Electricity Net Generation from All Utility Power Plants" 또는
- 각 발전원별 상세 선택

용량 선택:
- "Capacity" 또는
- "Net Summer Capacity by Major Fuel" 또는
- "Capacity by Energy Source"
```

#### Step 3: 필터 설정
```
시간 범위 (Time Period):
  - 시작: 2016-01 (2016년 1월)
  - 종료: 2025-12 (2025년 12월)

주기 (Frequency):
  - Monthly (월간) 추천 - 더 상세한 데이터
  - Annual (연간) - 단순화된 데이터

부문 (Sector):
  - Electric power sector (전력 부문)
```

#### Step 4: 데이터 미리보기 및 다운로드
```
1. 설정 후 테이블 데이터 화면에 표시됨
2. 우측 상단 "Download" 또는 "Export" 버튼 클릭
3. 파일 형식 선택:
   - CSV (권장 - 개방형 포맷)
   - Excel (.xlsx)
   - JSON
4. 저장 위치: /home/user/Contests/data/
```

#### Step 5: 파일명 규칙
```
권장 파일명 (원본 그대로):
- eia_generation_2016_2025.csv
- eia_generation_monthly_2016_2025.csv
- eia_capacity_2016_2025.csv
- eia_capacity_annual_2016_2025.csv
```

---

### 🥈 방법 2: EIA API (자동화 필요시)

#### Prerequisites
```
1. API 키 발급: https://www.eia.gov/opendata/register.php
   - 이메일 입력
   - 등록
   - 이메일로 API 키 수신 (자동)
```

#### API 엔드포인트
```
신규 API (v2):
- 기본 URL: https://api.eia.gov/v2/
- 발전량: /electricity/rto/region-data/data/
- 용량: /electricity/rto/region-data/data/
```

#### 구식 API (Legacy) 시리즈 ID
```
발전량 (Net Generation) - 연간:
  ELEC.GEN.ALL-US.A    → 전체
  ELEC.GEN.COAL-US.A   → 석탄
  ELEC.GEN.NG-US.A     → 천연가스
  ELEC.GEN.NUC-US.A    → 원자력
  ELEC.GEN.WND-US.A    → 풍력
  ELEC.GEN.SOL-US.A    → 태양광
  ELEC.GEN.HPS-US.A    → 수력

용량 (Capacity) - 연간:
  ELEC.CAPAC.ALL-US.A  → 전체
  ELEC.CAPAC.COAL-US.A → 석탄
  ELEC.CAPAC.NG-US.A   → 천연가스
  ELEC.CAPAC.NUC-US.A  → 원자력
  ELEC.CAPAC.WND-US.A  → 풍력
  ELEC.CAPAC.SOL-US.A  → 태양광
```

#### Python 예제 (구식 API 사용)
```python
import requests

API_KEY = "your_api_key_from_eia"

# 발전량 데이터 요청
url = "https://api.eia.gov/series/data/ELEC.GEN.ALL-US.A"
params = {
    "api_key": API_KEY,
    "out": "json"
}

response = requests.get(url, params=params)
data = response.json()

# 원본 JSON 저장 (가공 없음)
import json
with open('eia_generation_raw.json', 'w') as f:
    json.dump(data, f, indent=2)
```

---

### 🥉 방법 3: 직접 다운로드 링크

```
EIA 주요 다운로드 페이지:

1. 발전 데이터 메인:
   https://www.eia.gov/electricity/

2. 발전 데이터 페이지:
   https://www.eia.gov/electricity/data.php

3. 월간 발전 데이터:
   https://www.eia.gov/electricity/monthly/

4. 연간 발전 데이터:
   https://www.eia.gov/electricity/annual/

각 페이지에서 xlsx/csv 파일 직접 다운로드 가능
```

---

## 💾 저장 구조

### 권장 디렉토리 구조
```
/home/user/Contests/
├── data/
│   ├── eia_generation_monthly_2016_2025.csv
│   ├── eia_generation_annual_2016_2025.csv
│   ├── eia_capacity_2016_2025.csv
│   ├── eia_generation_raw.json (API 사용시)
│   └── eia_capacity_raw.json (API 사용시)
│
├── download_eia_data.py
├── eia_api_downloader.py
├── EIA_DATA_DOWNLOAD_GUIDE.md
├── eia_download_instructions.json
└── README_EIA_데이터수집.md (이 파일)
```

### 파일명 규칙
```
✅ 권장 (원본 그대로):
- eia_generation_2016_2025.csv
- eia_capacity_2016_2025.csv

❌ 피할 것 (가공된 파일명):
- generation_processed.csv
- capacity_cleaned.csv
```

---

## ⚠️ 중요사항: 원본 데이터 유지

### 가공하면 안 되는 것들
```
❌ 단위 변경 금지
   예: MWh를 GWh로 변환하지 말 것

❌ 열/행 삭제 금지
   예: 특정 발전원 제거하지 말 것

❌ 누락값(N/A, -) 처리하지 말 것
   그대로 유지할 것

❌ 소수점 반올림 금지
   원본 정확도 유지할 것

❌ 정렬 변경 금지
   EIA 원본 순서 유지할 것
```

### 허용되는 작업
```
✅ CSV/JSON/Excel 형식 선택 (원본 데이터는 동일)

✅ 여러 발전원의 데이터를 합친 새 파일 생성
   (원본 파일은 따로 보관)

✅ 메타데이터 추가
   (데이터 출처, 다운로드 날짜, 단위 설명 등)

✅ 데이터 검증
   (행/열 수 확인, 시간 범위 확인 등)
```

---

## 📋 데이터 검증 체크리스트

다운로드 후 다음을 확인하세요:

```
□ 시간 범위: 2016-01 ~ 2025-12 (120개월 또는 10년)
□ 발전원: 9가지 모두 포함 (Coal, NG, Nuclear, Wind, Solar, Hydro, Biomass, Geo, Other)
□ 단위: MWh 또는 MW (EIA 원본 단위)
□ 형식: CSV, JSON, or Excel (그대로)
□ 파일 크기: 대략 100KB ~ 1MB (예상)
□ 누락값: N/A, -, 0 등이 섞여있을 수 있음 (정상)
```

---

## 🎯 실행 방법 요약

### 빠른 시작 (웹 브라우저)
```bash
1. https://www.eia.gov/electricity/data/browser/ 방문
2. "Net Generation by Source" 선택
3. 2016-01 ~ 2025-12 설정
4. CSV 다운로드
5. /home/user/Contests/data/ 에 저장
```

### Python 자동화
```bash
# 1단계: 가이드 확인
python3 download_eia_data.py

# 2단계: API 키 발급 (필요시)
# https://www.eia.gov/opendata/register.php

# 3단계: API 다운로더 실행
python3 eia_api_downloader.py
```

---

## 📞 문제 발생시

### 웹사이트에 접근 불가
```
→ VPN 또는 프록시 확인
→ 브라우저 캐시 삭제
→ 다른 브라우저 시도
```

### API 응답 오류
```
→ API 키 확인
→ 요청 매개변수 확인 (URL, 필터 등)
→ EIA 서버 상태 확인
```

### 파일 형식 문제
```
→ CSV 파일이 깨진 경우: Excel에서 열기 후 재저장
→ JSON 파일 구조 확인: Python json.load() 테스트
```

---

## 📚 참고 자료

### 공식 문서
- EIA 전력 데이터 브라우저: https://www.eia.gov/electricity/data/browser/
- EIA Open Data API: https://www.eia.gov/opendata/qb.php
- EIA 문의: https://www.eia.gov/about/contact.php

### 데이터 설명
- 발전원 분류 설명: https://www.eia.gov/electricity/monthly/
- 용량 정의: https://www.eia.gov/electricity/state/

### 라이센스
- EIA 데이터는 미국 정부 공개 도메인
- 상업적 사용 가능
- 출처 명시 권장: "Source: U.S. Energy Information Administration (EIA)"

---

## ✅ 최종 체크리스트

```
준비물:
  □ 웹 브라우저 (또는 curl/wget)
  □ CSV 파일 저장 공간 (최소 1GB 여유)
  □ 인터넷 연결

선택사항:
  □ Python 3.7+ (API 자동화용)
  □ API 키 (https://www.eia.gov/opendata/register.php)
  □ pandas 라이브러리 (데이터 분석용)

완료 후:
  □ 데이터 파일 저장 확인
  □ 파일 크기 및 내용 확인
  □ Git에 커밋 (선택사항)
```

---

**생성 날짜**: 2025-06-19  
**데이터 범위**: 2016-2025년  
**원본 유지**: ✓ 가공 없음  
**형식**: CSV, JSON, Excel 지원
