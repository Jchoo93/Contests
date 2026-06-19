
미국 전력망 데이터 설명서
========================

파일명: US_Power_Grid_2016_2025.xlsx / .csv
데이터 범위: 2016년 1월 ~ 2025년 12월
데이터 형식: Raw Data (월간 집계)
생성일: 2026-06-19

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
