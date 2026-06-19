import statistics
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models.generation import GenerationData
from models.mix_trend import GenerationMixTrend

class MixTrendCalculator:
    """발전원 MIX 트렌드 계산 엔진"""

    @staticmethod
    def calculate_percentages(capacity_dict: Dict[str, float]) -> Dict[str, float]:
        """발전원별 점유율 계산"""
        total = sum(capacity_dict.values())
        if total == 0:
            return {k: 0.0 for k in capacity_dict.keys()}
        return {k: (v / total) * 100 for k, v in capacity_dict.items()}

    @staticmethod
    def calculate_renewable_percentage(percentages: Dict[str, float]) -> float:
        """재생에너지 총 점유율 계산"""
        renewable_sources = ["solar", "wind", "hydro"]
        return sum(percentages.get(source, 0) for source in renewable_sources)

    @staticmethod
    def determine_trend_direction(change_pct: float) -> str:
        """트렌드 방향 결정"""
        if change_pct > 0.5:
            return "↑"
        elif change_pct < -0.5:
            return "↓"
        else:
            return "→"

    @staticmethod
    def calculate_volatility(values_list: List[float]) -> float:
        """표준편차 계산 (변동성)"""
        if len(values_list) < 2:
            return 0.0
        try:
            return round(statistics.stdev(values_list), 2)
        except:
            return 0.0

    @staticmethod
    def calculate_herfindahl_index(percentages: Dict[str, float]) -> float:
        """허핀달 지수 계산 (시장 집중도)

        HHI = Σ(percentage_i)²
        0 = 완벽하게 다양함
        10000 = 완벽한 독점

        전력 분야 일반적 범위: 1500-3000
        """
        hhi = sum((p ** 2) for p in percentages.values())
        return round(hhi / 100, 2)  # 0-100 스케일로 정규화

    @staticmethod
    def calculate_energy_diversity_score(herfindahl: float) -> float:
        """에너지 다양성 점수 (0-10)

        HHI 낮을수록 다양함 (높은 점수)
        """
        # HHI: 0-100 범위
        # 점수: 10-0 범위 (반비례)
        score = max(0, 10 - (herfindahl / 10))
        return round(score, 1)

    @staticmethod
    def get_historical_percentages(
        db: Session,
        region: str,
        days: int
    ) -> List[Dict[str, float]]:
        """과거 발전원별 점유율 데이터 조회"""
        cutoff_date = datetime.now().date() - timedelta(days=days)

        records = db.query(GenerationData).filter(
            GenerationData.region == region,
            GenerationData.date >= cutoff_date
        ).order_by(GenerationData.date).all()

        percentages_list = []
        for record in records:
            capacity_dict = {
                "solar": record.solar_capacity_mw or 0,
                "wind": record.wind_capacity_mw or 0,
                "hydro": record.hydro_capacity_mw or 0,
                "fossil": record.fossil_capacity_mw or 0,
                "nuclear": record.nuclear_capacity_mw or 0,
            }
            pct = MixTrendCalculator.calculate_percentages(capacity_dict)
            pct["renewable"] = MixTrendCalculator.calculate_renewable_percentage(pct)
            pct["date"] = record.date
            percentages_list.append(pct)

        return percentages_list

    @staticmethod
    def calculate_trend_change(
        current: Dict[str, float],
        previous: Dict[str, float]
    ) -> Dict[str, float]:
        """변화율 계산"""
        return {
            k: round(current.get(k, 0) - previous.get(k, 0), 2)
            for k in current.keys()
        }

    @staticmethod
    def calculate_volatility_for_period(
        db: Session,
        region: str,
        source: str,
        days: int
    ) -> float:
        """특정 발전원의 기간별 변동성 계산"""
        percentages = MixTrendCalculator.get_historical_percentages(db, region, days)
        values = [p.get(source, 0) for p in percentages]
        return MixTrendCalculator.calculate_volatility(values)

    @staticmethod
    def create_mix_trend_record(
        db: Session,
        region: str,
        date: datetime.date,
        generation_data: GenerationData
    ) -> GenerationMixTrend:
        """발전원 MIX 트렌드 레코드 생성"""

        # 현재 발전원 구성 계산
        capacity_dict = {
            "solar": generation_data.solar_capacity_mw or 0,
            "wind": generation_data.wind_capacity_mw or 0,
            "hydro": generation_data.hydro_capacity_mw or 0,
            "fossil": generation_data.fossil_capacity_mw or 0,
            "nuclear": generation_data.nuclear_capacity_mw or 0,
        }
        current_pct = MixTrendCalculator.calculate_percentages(capacity_dict)
        renewable_pct = MixTrendCalculator.calculate_renewable_percentage(current_pct)

        # 과거 데이터 조회
        historical_7d = MixTrendCalculator.get_historical_percentages(db, region, 7)
        historical_30d = MixTrendCalculator.get_historical_percentages(db, region, 30)
        historical_1y = MixTrendCalculator.get_historical_percentages(db, region, 365)

        # 변화율 계산
        change_7d = {}
        change_30d = {}
        change_1y = {}

        if len(historical_7d) > 0:
            oldest_7d = historical_7d[0]
            change_7d = MixTrendCalculator.calculate_trend_change(current_pct, oldest_7d)

        if len(historical_30d) > 0:
            oldest_30d = historical_30d[0]
            change_30d = MixTrendCalculator.calculate_trend_change(current_pct, oldest_30d)

        if len(historical_1y) > 0:
            oldest_1y = historical_1y[0]
            change_1y = MixTrendCalculator.calculate_trend_change(current_pct, oldest_1y)

        # 변동성 계산
        solar_volatility = MixTrendCalculator.calculate_volatility_for_period(
            db, region, "solar", 7
        )
        wind_volatility = MixTrendCalculator.calculate_volatility_for_period(
            db, region, "wind", 7
        )
        hydro_volatility = MixTrendCalculator.calculate_volatility_for_period(
            db, region, "hydro", 7
        )
        renewable_volatility = MixTrendCalculator.calculate_volatility_for_period(
            db, region, "renewable", 7
        )

        # 헤르핀달 지수 및 다양성 점수 계산
        herfindahl = MixTrendCalculator.calculate_herfindahl_index(current_pct)
        diversity_score = MixTrendCalculator.calculate_energy_diversity_score(herfindahl)

        # 트렌드 방향 결정
        trend_record = GenerationMixTrend(
            date=date,
            region=region,

            # 현재 구성
            solar_pct=round(current_pct.get("solar", 0), 1),
            wind_pct=round(current_pct.get("wind", 0), 1),
            hydro_pct=round(current_pct.get("hydro", 0), 1),
            fossil_pct=round(current_pct.get("fossil", 0), 1),
            nuclear_pct=round(current_pct.get("nuclear", 0), 1),
            renewable_total_pct=round(renewable_pct, 1),

            # 7일 변화
            solar_pct_change_7d=change_7d.get("solar", 0),
            wind_pct_change_7d=change_7d.get("wind", 0),
            hydro_pct_change_7d=change_7d.get("hydro", 0),
            fossil_pct_change_7d=change_7d.get("fossil", 0),
            nuclear_pct_change_7d=change_7d.get("nuclear", 0),
            renewable_pct_change_7d=change_7d.get("renewable", 0),

            # 30일 변화
            solar_pct_change_30d=change_30d.get("solar", 0),
            wind_pct_change_30d=change_30d.get("wind", 0),
            renewable_pct_change_30d=change_30d.get("renewable", 0),

            # 1년 변화
            solar_pct_change_1y=change_1y.get("solar", 0),
            wind_pct_change_1y=change_1y.get("wind", 0),
            renewable_pct_change_1y=change_1y.get("renewable", 0),

            # 트렌드 방향
            solar_trend=MixTrendCalculator.determine_trend_direction(change_7d.get("solar", 0)),
            wind_trend=MixTrendCalculator.determine_trend_direction(change_7d.get("wind", 0)),
            hydro_trend=MixTrendCalculator.determine_trend_direction(change_7d.get("hydro", 0)),
            fossil_trend=MixTrendCalculator.determine_trend_direction(change_7d.get("fossil", 0)),
            nuclear_trend=MixTrendCalculator.determine_trend_direction(change_7d.get("nuclear", 0)),
            renewable_trend=MixTrendCalculator.determine_trend_direction(change_7d.get("renewable", 0)),

            # 변동성
            solar_volatility=solar_volatility,
            wind_volatility=wind_volatility,
            hydro_volatility=hydro_volatility,
            renewable_volatility=renewable_volatility,

            # 시장 지표
            herfindahl_index=herfindahl,
            energy_diversity_score=diversity_score,
        )

        return trend_record
