from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta
from typing import List, Optional

from database.db import get_db
from models.mix_trend import GenerationMixTrend
from models.generation import GenerationData
from services.mix_trend_calculator import MixTrendCalculator

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

@router.get("/generation-mix-trend/{region}")
def get_generation_mix_trend(
    region: str,
    days: int = Query(7, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """발전원 MIX 트렌드 조회

    Args:
        region: 지역 (CAISO, ERCOT, PJM, MISO, SPP, WECC)
        days: 조회 기간 (기본값: 7일)
    """
    cutoff_date = datetime.now().date() - timedelta(days=days)

    records = db.query(GenerationMixTrend).filter(
        GenerationMixTrend.region == region,
        GenerationMixTrend.date >= cutoff_date
    ).order_by(GenerationMixTrend.date).all()

    if not records:
        raise HTTPException(status_code=404, detail="No trend data found")

    current = records[-1]  # 최신 데이터

    return {
        "region": region,
        "period": f"{days}_days",
        "current_mix": {
            "date": current.date,
            "solar": {
                "percentage": current.solar_pct,
                "trend": current.solar_trend
            },
            "wind": {
                "percentage": current.wind_pct,
                "trend": current.wind_trend
            },
            "hydro": {
                "percentage": current.hydro_pct,
                "trend": current.hydro_trend
            },
            "fossil": {
                "percentage": current.fossil_pct,
                "trend": current.fossil_trend
            },
            "nuclear": {
                "percentage": current.nuclear_pct,
                "trend": current.nuclear_trend
            },
            "renewable_total": {
                "percentage": current.renewable_total_pct,
                "trend": current.renewable_trend
            }
        },
        "trend_7_days": {
            "solar": {
                "change_pct": current.solar_pct_change_7d,
                "change_direction": current.solar_trend,
                "volatility": current.solar_volatility
            },
            "wind": {
                "change_pct": current.wind_pct_change_7d,
                "change_direction": current.wind_trend,
                "volatility": current.wind_volatility
            },
            "fossil": {
                "change_pct": current.fossil_pct_change_7d,
                "change_direction": current.fossil_trend
            },
            "renewable_total": {
                "change_pct": current.renewable_pct_change_7d,
                "change_direction": current.renewable_trend,
                "volatility": current.renewable_volatility
            }
        },
        "trend_30_days": {
            "solar": {
                "change_pct": current.solar_pct_change_30d,
                "trend": "increasing" if (current.solar_pct_change_30d or 0) > 0 else "decreasing"
            },
            "wind": {
                "change_pct": current.wind_pct_change_30d
            },
            "renewable_total": {
                "change_pct": current.renewable_pct_change_30d
            }
        },
        "trend_1_year": {
            "solar": {
                "change_pct": current.solar_pct_change_1y,
                "trend": "strongly_increasing" if (current.solar_pct_change_1y or 0) > 5 else "increasing"
            },
            "wind": {
                "change_pct": current.wind_pct_change_1y
            },
            "nuclear": {
                "change_pct": current.nuclear_pct_change_1y
            },
            "fossil": {
                "change_pct": current.fossil_pct_change_1y,
                "trend": "decreasing" if (current.fossil_pct_change_1y or 0) < 0 else "stable"
            },
            "renewable_total": {
                "change_pct": current.renewable_pct_change_1y
            }
        },
        "daily_breakdown": [
            {
                "date": r.date,
                "solar": r.solar_pct,
                "wind": r.wind_pct,
                "hydro": r.hydro_pct,
                "fossil": r.fossil_pct,
                "nuclear": r.nuclear_pct,
                "renewable": r.renewable_total_pct
            }
            for r in records
        ],
        "market_metrics": {
            "herfindahl_index": current.herfindahl_index,
            "energy_diversity_score": current.energy_diversity_score,
            "grid_stability": "healthy" if current.renewable_volatility < 2.0 else "volatile"
        }
    }

@router.get("/generation-mix-comparison")
def get_generation_mix_comparison(db: Session = Depends(get_db)):
    """지역 간 발전원 MIX 비교"""
    today = datetime.now().date()

    records = db.query(GenerationMixTrend).filter(
        GenerationMixTrend.date == today
    ).all()

    if not records:
        raise HTTPException(status_code=404, detail="No data for today")

    return {
        "comparison_date": today,
        "regions": [
            {
                "region": r.region,
                "renewable_percentage": r.renewable_total_pct,
                "solar": r.solar_pct,
                "wind": r.wind_pct,
                "fossil": r.fossil_pct,
                "renewable_change_7d": r.renewable_pct_change_7d,
                "energy_diversity_score": r.energy_diversity_score
            }
            for r in sorted(records, key=lambda x: x.renewable_total_pct, reverse=True)
        ],
        "summary": {
            "highest_renewable": max(records, key=lambda x: x.renewable_total_pct).region,
            "highest_fossil": max(records, key=lambda x: x.fossil_pct).region,
            "highest_diversity": max(records, key=lambda x: x.energy_diversity_score).region,
            "fastest_renewable_growth": max(
                records,
                key=lambda x: (x.renewable_pct_change_7d or 0)
            ).region
        }
    }

@router.get("/market-insights/{region}")
def get_market_insights(
    region: str,
    db: Session = Depends(get_db)
):
    """시장 분석가를 위한 종합 인사이트"""
    today = datetime.now().date()

    trend_record = db.query(GenerationMixTrend).filter(
        GenerationMixTrend.region == region,
        GenerationMixTrend.date == today
    ).first()

    if not trend_record:
        raise HTTPException(status_code=404, detail="No data found")

    # 인사이트 생성
    insights = {
        "positive_trends": [],
        "concerns": [],
        "recommendations": []
    }

    # 긍정적 트렌드
    if (trend_record.renewable_pct_change_7d or 0) > 0:
        insights["positive_trends"].append(
            f"재생에너지 비중 증가 ({trend_record.renewable_pct_change_7d:+.1f}% 7d)"
        )

    if (trend_record.solar_pct_change_7d or 0) > 0:
        insights["positive_trends"].append(
            f"태양광 비율 지속 증가 ({trend_record.solar_pct_change_7d:+.1f}% 7d)"
        )

    if (trend_record.fossil_pct_change_7d or 0) < 0:
        insights["positive_trends"].append(
            f"화석연료 비율 감소 ({trend_record.fossil_pct_change_7d:.1f}% 7d)"
        )

    # 우려사항
    if (trend_record.wind_volatility or 0) > 3.0:
        insights["concerns"].append(
            f"풍력 변동성 높음 (σ={trend_record.wind_volatility}%)"
        )

    if trend_record.renewable_total_pct > 40 and trend_record.solar_volatility > 2:
        insights["concerns"].append(
            "높은 재생에너지 의존도로 인한 일일 사이클 심화"
        )

    if (trend_record.renewable_pct_change_7d or 0) > 3:
        insights["concerns"].append(
            "급격한 재생에너지 비중 변화로 그리드 안정성 주의"
        )

    # 권장사항
    if (trend_record.renewable_total_pct or 0) < 50:
        insights["recommendations"].append(
            "재생에너지 확충을 통한 탄소 감축 지속 필요"
        )

    if (trend_record.renewable_volatility or 0) > 1.5:
        insights["recommendations"].append(
            "배터리 저장소 및 에너지 저장 시스템 확충 권장"
        )

    if (trend_record.energy_diversity_score or 0) < 6:
        insights["recommendations"].append(
            "발전원 다양성 증대를 통한 공급 안정성 강화"
        )

    insights["recommendations"].append(
        "수요 측면 관리(DSM) 및 스마트 그리드 기술 도입"
    )

    return {
        "region": region,
        "date": today,
        "current_state": {
            "renewable_percentage": trend_record.renewable_total_pct,
            "diversity_score": trend_record.energy_diversity_score,
            "volatility": trend_record.renewable_volatility
        },
        "insights": insights,
        "key_metrics": {
            "renewable_growth_7d": trend_record.renewable_pct_change_7d,
            "renewable_growth_30d": trend_record.renewable_pct_change_30d,
            "renewable_growth_1y": trend_record.renewable_pct_change_1y,
            "herfindahl_index": trend_record.herfindahl_index
        }
    }

@router.get("/volatility-analysis/{region}")
def get_volatility_analysis(
    region: str,
    days: int = Query(7, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """발전원별 변동성 분석"""
    cutoff_date = datetime.now().date() - timedelta(days=days)

    records = db.query(GenerationMixTrend).filter(
        GenerationMixTrend.region == region,
        GenerationMixTrend.date >= cutoff_date
    ).order_by(GenerationMixTrend.date).all()

    if not records:
        raise HTTPException(status_code=404, detail="No data found")

    latest = records[-1]

    return {
        "region": region,
        "period": f"{days}_days",
        "volatility_analysis": {
            "solar": {
                "current": latest.solar_pct,
                "volatility": latest.solar_volatility,
                "interpretation": "Low" if (latest.solar_volatility or 0) < 2 else "High",
                "primary_driver": "Daily cycle (weather)"
            },
            "wind": {
                "current": latest.wind_pct,
                "volatility": latest.wind_volatility,
                "interpretation": "High" if (latest.wind_volatility or 0) > 3 else "Moderate",
                "primary_driver": "Weather patterns"
            },
            "hydro": {
                "current": latest.hydro_pct,
                "volatility": latest.hydro_volatility,
                "interpretation": "Very Low",
                "primary_driver": "Reservoir management"
            },
            "renewable_total": {
                "current": latest.renewable_total_pct,
                "volatility": latest.renewable_volatility,
                "interpretation": "Moderate" if (latest.renewable_volatility or 0) < 2 else "High"
            }
        },
        "grid_stability": {
            "stability_score": max(0, 100 - (latest.renewable_volatility or 0) * 10),
            "status": "Healthy" if (latest.renewable_volatility or 0) < 2 else "Monitor"
        }
    }
