from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.models import get_db
from db.models import AlertRule
from resources.alert_rules.alert_rule_schema import AlertRuleCreate

router = APIRouter()


@router.get("/")
def get_alerts_rules(db: Session = Depends(get_db)):
    return db.query(AlertRule).all()


@router.post("/")
def create_alert_rule(body: AlertRuleCreate, db: Session = Depends(get_db)):
    alert_rule = AlertRule(name=body.name, symbol=body.symbol, threshold_price=body.threshold_price)
    db.add(alert_rule)
    db.commit()
    db.refresh(alert_rule)
    return {"message": "Alert Rule created successfully", "data": alert_rule, "status": True, "status_code": 201}
