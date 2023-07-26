""" Alert DAL"""
from abc import ABC
from typing import List, Type

from sqlalchemy.orm import Session

from mixins.repository import Repository
from resources.alerts.alert_schema import CreateAlertCommand
from db.models import Alert

"""_summary_
this file is to right any ORM logic for the Alert model
"""


class AlertRepository(Repository, ABC):
    """
       AlertRuleRepository
       used as abstraction to access data layer and return objects
       requires: sqlalchemy.orm.Session
       """

    def __init__(self, db: Session):
        self.db = db

    def create(self, command: CreateAlertCommand):
        alert = Alert(
            name=command.name,
            symbol=command.symbol,
            original_threshold_price=command.original_threshold_price,
            reached_threshold_price=command.reached_threshold_price)
        self.db.add(alert)
        return alert

    def find_all(self) -> List[Type[Alert]]:
        return self.db.query(Alert).all()
