from celery.schedules import crontab
from sqlalchemy.orm import Session

from api.main import celery_app, event_handler
from constants.stock_symbols import symbol_representation
from db.models.model_base import SessionLocal
from resources.alert_rules.alert_rule_dal import AlertRuleRepository
from resources.alerts.alert_schema import CreateAlertCommand
from resources.market.market_service import get_market_data


@celery_app.task
async def validate_threshold_reach(price_decimal_places: int):
    prices = get_market_data(price_decimal_places)

    stock_symbols = symbol_representation.keys()
    db: Session = SessionLocal()
    alert_rules = AlertRuleRepository(db).find_by_symbols(stock_symbols)
    for rule in alert_rules:
        current_price = next((x for x in prices if x.symbol == rule.symbol), None)
        if current_price and current_price.price >= rule.threshold_price:
            await event_handler.publish(
                exchange_key="alert_threshold",
                router_key="alert_threshold_price_reached",
                exchange_type="topic",
                message=CreateAlertCommand(
                    symbol=rule.symbol,
                    original_threshold_price=rule.threshold_price,
                    new_price=current_price.price,
                    name=rule.name,
                ))


# Schedule the task to run every 5 minutes
@celery_app.periodic_task(run_every=crontab(minute='*/5'))
def fetch_market_data_every_five_minutes():
    return validate_threshold_reach(price_decimal_places=2)
