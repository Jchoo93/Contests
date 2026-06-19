# US Power Grid Dashboard

미국 전역 전력망을 실시간으로 모니터링하는 풀스택 대시보드 애플리케이션입니다.

![Dashboard](https://img.shields.io/badge/Status-In%20Development-blue)
![Python](https://img.shields.io/badge/Backend-Python%203.9%2B-blue)
![React](https://img.shields.io/badge/Frontend-React%2018-61dafb)

## 🎯 프로젝트 개요

이 프로젝트는 미국 에너지정보청(EIA)의 공개 데이터를 활용하여:
- **발전용량** - 발전원별(태양광, 풍력, 수력, 화석, 원자력) 용량 분석
- **전력 가격** - 지역별 평균 전력 가격 비교
- **재생에너지 비율** - 녹색 에너지 사용 현황 추적
- 일일 자동 업데이트를 통한 **정확하고 최신의 데이터** 제공

## 🚀 빠른 시작

### 1. 백엔드 설정 및 실행

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python3 app.py
```

백엔드는 `http://localhost:8000`에서 실행됩니다.

### 2. 프론트엔드 설정 및 실행

```bash
cd frontend
npm install
npm run dev
```

프론트엔드는 `http://localhost:5173`에서 실행됩니다.

## 🧪 테스트

### 통합 테스트 실행
```bash
python3 test_integration.py
```

### 백엔드 테스트
```bash
cd backend
pytest tests/ -v
```

### 프론트엔드 테스트
```bash
cd frontend
npm test
```

## 📁 프로젝트 구조

```
power-grid-dashboard/
├── backend/          # Python FastAPI 백엔드
├── frontend/         # React 프론트엔드
└── test_integration.py
```

## 📊 주요 기능

### 백엔드
- ✅ FastAPI REST API
- ✅ EIA API 데이터 수집
- ✅ SQLAlchemy ORM
- ✅ 일일 자동 업데이트 (APScheduler)
- ✅ 에러 핸들링 및 로깅

### 프론트엔드
- ✅ React 18 + Vite
- ✅ Redux Toolkit 상태 관리
- ✅ Recharts 데이터 시각화
- ✅ Tailwind CSS 반응형 디자인
- ✅ 자동 데이터 새로고침

## 📝 상세 문서

- [Backend README](backend/README.md)
- [Frontend README](frontend/README.md)

## 🔧 환경 변수

### 백엔드 (.env)
```
EIA_API_KEY=your_api_key_here
DATABASE_URL=sqlite:///./power_grid.db
ENVIRONMENT=development
HOST=0.0.0.0
PORT=8000
DEBUG=True
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
LOG_LEVEL=INFO
```

### 프론트엔드 (.env)
```
VITE_API_BASE_URL=http://localhost:8000/api
```

## API 엔드포인트

- `GET /api/generation` - 발전용량 데이터
- `GET /api/pricing` - 전력 가격 데이터
- `GET /api/renewables` - 재생에너지 데이터
- `GET /api/summary` - 통합 요약
- `GET /api/health` - 헬스 체크
- `GET /docs` - Swagger API 문서

## 🌟 데이터 흐름

1. 매일 자정 UTC 기준 EIA API에서 데이터 수집
2. 데이터 검증 및 정규화
3. SQLite/PostgreSQL에 저장
4. REST API를 통해 프론트엔드에 제공
5. React 대시보드에서 시각화

## 📞 문의

자세한 정보는 각 디렉토리의 README.md를 참조하세요.

---

**US Power Grid Monitoring Dashboard**
