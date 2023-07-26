import asyncio

from sqlalchemy.orm import Session

from api.main import celery_app, event_handler
from constants.stock_symbols import symbol_representation
from db.models.model_base import SessionLocal
from resources.alert_rules.alert_rule_dal import AlertRuleRepository

from resources.alerts.alert_schema import CreateAlertCommand
from resources.market.market_service import get_market_data

import logging

logger = logging.getLogger(__name__)


async def _publish_alert(rule, current_price):
    await event_handler.connect()
    await event_handler.publish(
        exchange_key="alert_threshold",
        router_key="alert_threshold_price_reached",
        exchange_type="topic",
        message=CreateAlertCommand(
            symbol=rule.symbol,
            original_threshold_price=str(rule.threshold_price),
            new_price=str(current_price[0].price),
            name=rule.name,
        ))


# Schedule the task to run every 1 minutes
@celery_app.task
def fetch_market_data_every_minute():
    logger.info('Validating threshold reach...')
    db: Session = SessionLocal()
    prices = get_market_data(2)
    logger.info("found prices: " + str(len(prices)))
    stock_symbols = symbol_representation.keys()
    logger.info(f"stock_symbols ===> {stock_symbols}")
    alert_rules = AlertRuleRepository(db).find_by_symbols(stock_symbols)
    logger.info(f"found rules: {alert_rules}")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = []
    for rule in alert_rules:
        current_price = [c for c in prices if c.symbol == rule.symbol]
        logger.info("rule.symbol: " + rule.symbol)
        logger.info("rule.symbol: " + str(rule.threshold_price))
        logger.info("rule.symbol: " + str(current_price))
        if current_price and float(current_price[0].price) >= float(rule.threshold_price):
            tasks.append(asyncio.ensure_future(_publish_alert(rule, current_price)))
    loop.run_until_complete(asyncio.gather(*tasks))
    logger.info("Finished running tasks")
