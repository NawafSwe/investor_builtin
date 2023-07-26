""" Rule Service"""

from sqlalchemy.orm import Session

from db.models.model_base import SessionLocal
from resources.alerts.alert_schema import CreateAlertCommand
from resources.alerts.alert_dal import AlertRepository

"""_summary_
this file to write any business logic for the Rules
"""


async def notify_threshold_reached(command: CreateAlertCommand):
    """
    log alert for the threshold reached
    :param command: to create alert
    :return:None
    """
    db: Session = SessionLocal()
    alert = AlertRepository(db).create(command)
    db.add(alert)
    db.commit()
    return None
