""" Alert Rule  DAL"""
from typing import List, Type

from sqlalchemy.orm import Session
from decimal import Decimal
from mixins.repository import Repository
from resources.alert_rules.alert_rule_schema import CreateAlertRuleCommand, UpdateAlertRuleCommand
from db.models import AlertRule

"""_summary_
this file is to right any ORM logic for the Alert Rule model
"""


class AlertRuleRepository(Repository):
    """
    AlertRuleRepository
    used as abstraction to access data layer and return objects
    requires: sqlalchemy.orm.Session
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, command: CreateAlertRuleCommand):
        alert_rule = AlertRule(name=command.name, symbol=command.symbol, threshold_price=command.threshold_price)
        self.db.add(alert_rule)
        return alert_rule

    def find_all(self) -> List[Type[AlertRule]]:
        return self.db.query(AlertRule).all()

    def find_by_id(self, id: str):
        return self.db.query(AlertRule).filter(AlertRule.id == id).first()

    def update_by_id(self, id: str, command: UpdateAlertRuleCommand):
        alert_rule = self.find_by_id(id)
        for k, v in command.items():
            setattr(alert_rule, k, v)
        return alert_rule

    def delete_by_id(self, id: str) -> Type[AlertRule]:
        alert_rule = self.find_by_id(id)
        return alert_rule

    def is_alert_rule_already_exist(self, symbol: str, threshold_price: Decimal) -> bool:
        is_already_exist_rule = self.db.query(AlertRule).filter(
            (AlertRule.symbol == symbol), (AlertRule.threshold_price == threshold_price)).first()
        return is_already_exist_rule is not None

    def find_by_symbols(self, symbols: list[str]) -> Type[AlertRule]:
        return self.db.query(AlertRule).filter(AlertRule.symbol in symbols).first()
