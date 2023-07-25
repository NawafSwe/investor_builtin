""" Alert Rule Service"""
from sqlalchemy.orm import Session
from resources.alert_rules.alert_rule_dal import AlertRuleRepository
from resources.alert_rules.alert_rule_model import AlertRule
from resources.alert_rules.exceptions import AlertRuleAlreadyExist
from resources.alert_rules.alert_rule_schema import CreateAlertRuleCommand, UpdateAlertRuleCommand

"""_summary_
this file to write any business logic for the Alert Rules
"""


def create_new_rule(command: CreateAlertRuleCommand, db: Session) -> AlertRule:
    """
    create new a rule
    :param command: command object contains information about the new alert rule
    :param db: sqlalchemy.orm.Session
    :return: Created Alert Rule
    """
    repository: "AlertRuleRepository" = AlertRuleRepository(db)
    if repository.is_alert_rule_already_exist(command.symbol, command.threshold_price):
        raise AlertRuleAlreadyExist("Alert Rule with symbol and threshold_price already exist")
    alert_rule = repository.create(command)
    db.commit()
    db.refresh(alert_rule)
    return alert_rule


def update_alert_rule_by_id(rule_id: str, command: UpdateAlertRuleCommand, db: Session):
    """
    update alert rule by id
    :param rule_id: the id of the rule
    :param command: command object contains information about the new alert rule
    :param db: sqlalchemy.orm.Session
    :return: Updated alert rule
    """
    repository: "AlertRuleRepository" = AlertRuleRepository(db)
    is_symbol_and_threshold_price_given = command.symbol is not None and command.threshold_price is not None
    if is_symbol_and_threshold_price_given and repository.is_alert_rule_already_exist(
            command.symbol, command.threshold_price):
        raise AlertRuleAlreadyExist("Alert Rule with symbol and threshold_price already exist")

    command = command.model_dump(exclude_none=True)
    alert_rule = repository.update_by_id(rule_id, command)
    db.bulk_save_objects([alert_rule])
    db.commit()
    db.refresh(alert_rule)
    return alert_rule


def get_all_alert_rules(db: Session):
    """
    get all alert rules
    :param db: sqlalchemy.orm.Session
    :return: return list of alert rules
    """
    return AlertRuleRepository(db).find_all()


def find_alert_rule_by_id(rule_id: str, db: Session):
    """
    find alert rule by id
    :param rule_id: rule id
    :param db: sqlalchemy.orm.Session
    :return: Alert Rule
    """
    return AlertRuleRepository(db).find_by_id(rule_id)


def find_and_delete_alert_rule_by_id(rule_id: str, db: Session) -> None:
    """
    find and delete alert rule by id
    :param rule_id: the rule id to be deleted
    :param db: sqlalchemy.orm.Session
    :return: None
    """
    alert_rule = AlertRuleRepository(db).delete_by_id(rule_id)
    if alert_rule:
        db.delete(alert_rule)
        db.commit()
