from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.models import get_db
from db.models import AlertRule
from resources.alert_rules.alert_rule_schema import CreateAlertRuleCommand, UpdateAlertRuleCommand
from resources.alert_rules.alert_rule_service import create_new_rule, get_all_alert_rules, find_alert_rule_by_id, \
    update_alert_rule_by_id, find_and_delete_alert_rule_by_id
from resources.alert_rules.exceptions import AlertRuleAlreadyExist

router = APIRouter()


@router.get("/")
def get(db: Session = Depends(get_db)):
    return {"data": get_all_alert_rules(db), "message": "Successfully Retrieved", "status": True, "status_code": 200}


@router.post("/", status_code=201)
def post(command: CreateAlertRuleCommand, db: Session = Depends(get_db)):
    try:
        alert_rule: AlertRule = create_new_rule(command, db)
    except AlertRuleAlreadyExist as _:
        return {"message": "Alert already exist", "status": False, "status_code": 400}

    return {"message": "Alert Rule created successfully", "data": alert_rule, "status": True, "status_code": 201}


@router.get("/{alert_rule_id}")
def get_by_id(alert_rule_id: str, db: Session = Depends(get_db)):
    alert_rule = find_alert_rule_by_id(alert_rule_id, db)
    if alert_rule is None:
        return {"message": "Alert Rule not found", "status": False, "status_code": 404}

    return {"data": alert_rule, "message": "Successfully Retrieved", "status": True, "status_code": 200}


@router.patch("/{alert_rule_id}", status_code=200)
def patch(alert_rule_id: str, body: UpdateAlertRuleCommand, db: Session = Depends(get_db)):
    alert_rule = find_alert_rule_by_id(rule_id=alert_rule_id, db=db)
    if alert_rule is None:
        return {"message": "Alert Rule not found", "status": False, "status_code": 404}
    try:
        alert_rule = update_alert_rule_by_id(rule_id=alert_rule_id, command=body, db=db)
        return {"data": alert_rule, "message": "Updated Successfully", "status": True, "status_code": 200}
    except AlertRuleAlreadyExist as _:
        return {"message": "Alert Rule with symbol and threshold_price already exist", "status": False,
                "status_code": 400}


@router.delete("/{alert_rule_id}", status_code=204)
def delete(alert_rule_id: str, db: Session = Depends(get_db)):
    find_and_delete_alert_rule_by_id(alert_rule_id, db)
