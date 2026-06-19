# EIA 미국 전력망 데이터 수집 가이드

## 📌 요약
**목표**: EIA(미국 에너지 정보청)에서 2016-2025년 미국 전력망의 발전원별 MIX와 발전 총 용량 데이터를 가공하지 않은 원본 상태로 수집

---

## 🌐 데이터 경로

### 주요 접근 방법 3가지

#### 1️⃣ **EIA 전력 데이터 브라우저 (가장 간단)**
- **웹사이트**: https://www.eia.gov/electricity/data/browser/
- **특징**: 웹 인터페이스로 쉽게 데이터 조회 및 다운로드 가능
- **지원 포맷**: CSV, JSON, XML

#### 2️⃣ **EIA Open Data API (자동화)**
- **API 기본 URL**: https://api.eia.gov/v2/
- **API 등록**: https://www.eia.gov/opendata/register.php (무료)
- **특징**: 프로그래맍으로 자동 수집 가능

#### 3️⃣ **EIA 데이터 다운로드 센터**
- **웹사이트**: https://www.eia.gov/electricity/
- **카테고리**: Generation Data, Capacity Data

---

## 📊 수집할 데이터 종류

### 1. 발전원별 발전량 (Net Generation by Source)
- **단위**: MWh (메가와트시) 또는 GWh (기가와트시)
- **시간 단위**: Monthly (월간) 또는 Annual (연간)
- **발전원**:
  - Coal (석탄)
  - Natural Gas (천연가스)
  - Nuclear (원자력)
  - Wind (풍력)
  - Solar (태양광)
  - Hydro (수력)
  - Biomass (바이오매스)
  - Geothermal (지열)
  - Other (기타)

### 2. 발전 총 용량 (Net Summer Capacity 또는 Capacity by Source)
- **단위**: MW (메가와트) 또는 GW (기가와트)
- **시간 단위**: Annual (연간)
- **같은 발전원 분류**

---

## 🔍 상세 단계별 다운로드 방법

### **방법 A: 웹 인터페이스를 통한 다운로드 (권장)**

#### Step 1: EIA 전력 데이터 브라우저 접속
```
https://www.eia.gov/electricity/data/browser/
```

#### Step 2: 데이터 선택
왼쪽 메뉴에서 다음 중 선택:

**발전량 데이터 선택**
- "Net generation from all utility power plants" 또는
- "Net generation from utility-scale electric generation"
- 또는 각 발전원별 항목 (예: "Electricity Net Generation from Coal")

**용량 데이터 선택**
- "Capacity" 또는
- "Net Summer Capacity by Major Fuel" 또는
- "Capacity by Energy Source"

#### Step 3: 필터 설정
```
Time Period: 2016-01 ~ 2025-12
Frequency: Monthly (월간) 또는 Annual (연간)
Sector: Electric power sector
```

#### Step 4: 데이터 미리보기
- 화면에 데이터 테이블이 표시됨
- 표에서 데이터 구조 확인 가능

#### Step 5: 다운로드/내보내기
1. 페이지 우상단의 **"Download"** 또는 **"More Options"** 버튼 클릭
2. 파일 형식 선택: **CSV** 또는 **Excel**
3. 저장 위치 선택 (권장: `/home/user/Contests/data/`)

**기대 파일명 예**:
- `generation_2016_2025.csv`
- `capacity_2016_2025.csv`
- `net_generation_utility.csv`

---

### **방법 B: EIA API를 통한 자동 수집**

#### Step 1: API 키 발급
1. https://www.eia.gov/opendata/register.php 방문
2. 이메일 입력 및 등록
3. API 키 수신 (이메일)

#### Step 2: Python 스크립트로 데이터 수집

**발전량 데이터 (Net Generation)**
```python
import requests
import json

API_KEY = "your_api_key_here"
BASE_URL = "https://api.eia.gov/v2"

# 발전량 API 엔드포인트 (연간 데이터)
endpoint = f"{BASE_URL}/electricity/rto/region-data/data/"

params = {
    "api_key": API_KEY,
    "data[0]": "value",
    "facets[subba][]": "US48",  # 미국 본토 48개 주
    "frequency": "annual",
    "sort[0][column]": "period",
    "sort[0][direction]": "asc",
    "offset": 0,
    "length": 10000
}

response = requests.get(endpoint, params=params)
data = response.json()

# 원본 데이터를 JSON으로 저장 (가공 없음)
with open('generation_raw.json', 'w') as f:
    json.dump(data, f, indent=2)

# 또는 CSV로 변환 (pandas 필요)
# import pandas as pd
# df = pd.DataFrame(data['response']['data'])
# df.to_csv('generation_2016_2025.csv', index=False)
```

**용량 데이터 (Capacity)**
```python
endpoint = f"{BASE_URL}/electricity/rto/region-data/data/"

params = {
    "api_key": API_KEY,
    "data[0]": "value",
    "facets[subba][]": "US48",
    "frequency": "annual",
    "sort[0][column]": "period",
    "sort[0][direction]": "asc",
    "offset": 0,
    "length": 10000
}

response = requests.get(endpoint, params=params)
data = response.json()

with open('capacity_raw.json', 'w') as f:
    json.dump(data, f, indent=2)
```

---

## 📋 EIA API 주요 시리즈 ID (구식 API)

만약 구식 API를 사용할 경우:

### Net Generation by Source
```
ELEC.GEN.ALL-US.A      : 전체 (연간)
ELEC.GEN.ALL-US.M      : 전체 (월간)
ELEC.GEN.COAL-US.A     : 석탄 (연간)
ELEC.GEN.NG-US.A       : 천연가스 (연간)
ELEC.GEN.NUC-US.A      : 원자력 (연간)
ELEC.GEN.WND-US.A      : 풍력 (연간)
ELEC.GEN.SOL-US.A      : 태양광 (연간)
ELEC.GEN.HPS-US.A      : 수력 (연간)
ELEC.GEN.BIO-US.A      : 바이오매스 (연간)
ELEC.GEN.GEO-US.A      : 지열 (연간)
```

### Capacity by Source
```
ELEC.CAPAC.ALL-US.A    : 전체 (연간)
ELEC.CAPAC.COAL-US.A   : 석탄 (연간)
ELEC.CAPAC.NG-US.A     : 천연가스 (연간)
ELEC.CAPAC.NUC-US.A    : 원자력 (연간)
ELEC.CAPAC.WND-US.A    : 풍력 (연간)
ELEC.CAPAC.SOL-US.A    : 태양광 (연간)
```

---

## 💾 데이터 저장 및 형식

### 원본 상태 보존
- **CSV 포맷 권장**: 가공 없는 원본 데이터
- **JSON 포맷**: API 응답 그대로 저장
- **Excel 포맷**: 필요시 EIA 웹사이트에서 직접 다운로드

### 저장 경로 추천
```
/home/user/Contests/
├── data/
│   ├── eia_generation_2016_2025.csv
│   ├── eia_capacity_2016_2025.csv
│   ├── eia_generation_raw.json
│   └── eia_capacity_raw.json
└── EIA_DATA_DOWNLOAD_GUIDE.md
```

---

## 📌 중요 사항

### ✅ 원본 데이터 유지
- EIA에서 제공하는 데이터를 그대로 저장
- 단위, 포맷, 시간대 변경 금지
- 누락된 값(N/A, -) 그대로 유지

### 🔐 라이센스
- EIA 데이터는 공개 도메인
- 상업적 사용 가능
- 출처 명시 권장: "Source: U.S. Energy Information Administration (EIA)"

### 📞 기술 지원
- EIA 문의: https://www.eia.gov/about/contact.php
- API 문서: https://www.eia.gov/opendata/qb.php

---

## 🎯 다음 단계

1. **웹 인터페이스로 데이터 다운로드** (빠름, 권장)
   - https://www.eia.gov/electricity/data/browser/ 접속
   - CSV 파일로 저장

2. **또는 API로 자동 수집** (정기적 업데이트 필요시)
   - API 키 발급
   - Python 스크립트 실행

3. **데이터 검증**
   - 행과 열 수 확인
   - 시간 범위 확인 (2016-01 ~ 2025-12)
   - 발전원 분류 확인

4. **Git에 커밋** (원본 데이터 관리)
   ```bash
   git add data/eia_*.csv
   git commit -m "Add raw EIA generation and capacity data (2016-2025)"
   git push
   ```

---

**마지막 업데이트**: 2025년
**데이터 범위**: 2016-2025년
**원본 유지**: ✓ 가공 없음
