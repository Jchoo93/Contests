import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from config import settings
from services.eia_service import EIAClient
from services.data_processor import DataProcessor
from database.db import SessionLocal

logger = logging.getLogger(__name__)

def start_daily_update():
    """일일 데이터 업데이트 작업"""
    logger.info("Starting daily data update...")

    try:
        db = SessionLocal()
        eia_client = EIAClient(settings.eia_api_key)

        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        try:
            logger.info(f"Fetching generation data for {yesterday}...")
            gen_response = eia_client.get_generation_data(yesterday)
            gen_records = DataProcessor.parse_generation_data(gen_response, yesterday)
            db.add_all(gen_records)
            logger.info(f"Added {len(gen_records)} generation records")
        except Exception as e:
            logger.error(f"Error processing generation data: {e}")

        try:
            logger.info(f"Fetching pricing data for {yesterday}...")
            pricing_response = eia_client.get_pricing_data(yesterday)
            pricing_records = DataProcessor.parse_pricing_data(pricing_response, yesterday)
            db.add_all(pricing_records)
            logger.info(f"Added {len(pricing_records)} pricing records")
        except Exception as e:
            logger.error(f"Error processing pricing data: {e}")

        try:
            logger.info(f"Fetching renewable data for {yesterday}...")
            renewable_response = eia_client.get_renewable_data(yesterday)
            renewable_records = DataProcessor.parse_renewable_data(renewable_response, yesterday)
            db.add_all(renewable_records)
            logger.info(f"Added {len(renewable_records)} renewable records")
        except Exception as e:
            logger.error(f"Error processing renewable data: {e}")

        db.commit()
        logger.info("Daily update completed successfully")

    except Exception as e:
        logger.error(f"Error in daily update job: {e}")
        if db:
            db.rollback()
    finally:
        if db:
            db.close()
        eia_client.close()
