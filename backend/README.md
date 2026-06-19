# US Power Grid Dashboard - Backend

미국 전역 전력망 모니터링 시스템의 Python 백엔드입니다.

## 기능

- 🔌 EIA API를 통한 전력 데이터 수집
- 📊 발전용량, 가격, 재생에너지 비율 데이터 관리
- ⏰ 일일 자동 데이터 업데이트
- 🔍 REST API를 통한 데이터 조회
- 📈 데이터 집계 및 요약

## 설치

### 1. 가상환경 생성
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate  # Windows
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정
```bash
cp .env.example .env
# .env 파일 편집하여 EIA_API_KEY 추가
```

EIA API 키는 https://www.eia.gov/opendata/ 에서 발급받을 수 있습니다.

## 실행

### 개발 서버 시작
```bash
python app.py
```

또는

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### API 문서
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 엔드포인트

### 발전 용량
```
GET /api/generation?days=1
GET /api/generation/{date}  # YYYY-MM-DD
```

### 전력 가격
```
GET /api/pricing?days=1
GET /api/pricing/{date}
```

### 재생에너지
```
GET /api/renewables?days=1
GET /api/renewables/{date}
```

### 통합 요약
```
GET /api/summary
```

### 헬스 체크
```
GET /api/health
```

## 데이터베이스

### 초기화
```bash
python -c "from database.db import Base, engine; from models.generation import GenerationData; from models.pricing import PricingData; from models.renewable import RenewableData; Base.metadata.create_all(bind=engine)"
```

### 지원 데이터베이스
- SQLite (기본, 개발용)
- PostgreSQL (프로덕션)

DATABASE_URL을 .env 파일에서 설정하세요.

## 테스트

```bash
pytest tests/ -v
pytest tests/ --cov=services --cov=api
```

## 구조

```
backend/
├── app.py                 # FastAPI 메인 애플리케이션
├── config.py              # 설정
├── requirements.txt       # 의존성
├── api/
│   ├── routes.py         # API 엔드포인트
│   └── schemas.py        # Pydantic 스키마
├── services/
│   ├── eia_service.py    # EIA API 클라이언트
│   ├── data_processor.py # 데이터 처리
│   └── scheduler_service.py # 스케줄러
├── models/
│   ├── generation.py     # 발전 데이터 모델
│   ├── pricing.py        # 가격 데이터 모델
│   └── renewable.py      # 재생에너지 데이터 모델
├── database/
│   └── db.py            # 데이터베이스 설정
├── utils/
│   └── logger.py        # 로깅 설정
└── tests/               # 테스트
```

## 로깅

로그는 `logs/app.log` 파일에 저장됩니다.

## 향후 계획

- [ ] WebSocket을 통한 실시간 데이터
- [ ] Redis 캐싱
- [ ] 데이터 예측 모델 (ML)
- [ ] 고급 필터링 및 분석
- [ ] Docker 컨테이너화
