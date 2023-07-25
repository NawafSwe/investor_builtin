CREATE DATABASE IF NOT EXISTS investor_bulletin;
USE investor_bulletin;
CREATE TABLE IF NOT EXISTS alerts_rules (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  symbol TEXT NOT NULL,
  name TEXT NOT NULL,
  threshold_price REAL NOT NULL,
  CONSTRAINT _alert_rule_constraint UNIQUE (symbol, threshold_price)
);