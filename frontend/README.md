# US Power Grid Dashboard - Frontend

React 기반의 미국 전력망 모니터링 대시보드입니다.

## 기능

- 📊 실시간 전력 데이터 시각화
- 📈 발전원별 용량 분석 (Solar, Wind, Hydro, Fossil, Nuclear)
- 💰 지역별 전력 가격 비교
- 🌱 재생에너지 비율 및 분포
- 🔄 자동 데이터 새로고침 (1분 간격)
- 📱 반응형 디자인 (모바일/태블릿/데스크톱)

## 설치

### 1. 의존성 설치
```bash
cd frontend
npm install
```

### 2. 환경 변수 설정
```bash
cp .env.example .env
# .env 파일 편집 (필요한 경우 VITE_API_BASE_URL 수정)
```

## 실행

### 개발 서버 시작
```bash
npm run dev
```

서버는 `http://localhost:5173`에서 실행됩니다.

### 프로덕션 빌드
```bash
npm run build
npm run preview
```

## 테스트

### 테스트 실행
```bash
npm test
```

### 테스트 UI
```bash
npm run test:ui
```

### 커버리지 리포트
```bash
npm run test:coverage
```

## 구조

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── main.jsx              # 진입점
│   ├── App.jsx               # 메인 컴포넌트
│   ├── components/
│   │   ├── Dashboard.jsx     # 대시보드 레이아웃
│   │   ├── Header.jsx        # 헤더
│   │   ├── SummaryCard.jsx   # 요약 카드
│   │   ├── GenerationChart.jsx # 발전용량 차트
│   │   ├── PricingChart.jsx  # 가격 차트
│   │   ├── RenewableChart.jsx # 재생에너지 차트
│   │   └── __tests__/        # 컴포넌트 테스트
│   ├── services/
│   │   ├── api.js            # API 클라이언트
│   │   └── __tests__/        # API 테스트
│   ├── store/
│   │   ├── index.js          # Redux 스토어
│   │   ├── slices/
│   │   │   └── dataSlice.js  # 데이터 리듀서
│   │   └── __tests__/        # 스토어 테스트
│   ├── styles/
│   │   └── index.css         # 전역 스타일
│   └── test/
│       └── setup.js          # 테스트 설정
├── vite.config.js
├── vitest.config.js
├── tailwind.config.js
└── postcss.config.js
```

## 기술 스택

- **React 18** - UI 라이브러리
- **Redux Toolkit** - 상태 관리
- **Recharts** - 데이터 시각화
- **Tailwind CSS** - 스타일링
- **Axios** - HTTP 클라이언트
- **Vite** - 빌드 도구
- **Vitest** - 테스트 프레임워크

## API 통합

백엔드 API와 자동으로 통신합니다 (`http://localhost:8000/api`).

### 사용 가능한 엔드포인트
- `GET /generation` - 발전 용량 데이터
- `GET /pricing` - 전력 가격 데이터
- `GET /renewables` - 재생에너지 데이터
- `GET /summary` - 통합 요약

## 커스터마이제이션

### 색상 수정
`tailwind.config.js`의 `theme.extend.colors` 섹션을 수정하세요.

### API URL 변경
`.env` 파일에서 `VITE_API_BASE_URL` 수정하세요.

## 성능

- 코드 스플릿팅
- Lazy loading
- Redux 메모이제이션
- 효율적인 리렌더링

## 향후 계획

- [ ] 다국어 지원
- [ ] 사용자 맞춤 알림
- [ ] 데이터 내보내기 (CSV/PDF)
- [ ] 고급 필터링
- [ ] 모바일 앱 (React Native)
