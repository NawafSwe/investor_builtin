CREATE DATABASE IF NOT EXISTS investor_bulletin;
USE investor_bulletin;
CREATE TABLE IF NOT EXISTS alerts_rules
(
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    symbol          TEXT NOT NULL,
    name            TEXT NOT NULL,
    threshold_price REAL NOT NULL,
    created_at      DATE NOT NULL    DEFAULT now(),
    updated_at      DATE NOT NULL    DEFAULT now(),
    CONSTRAINT _alert_rule_constraint UNIQUE (symbol, threshold_price)
);

CREATE TABLE alerts
(
    id                       UUID            DEFAULT gen_random_uuid() PRIMARY KEY,
    name                     STRING NOT NULL,
    symbol                   STRING NOT NULL,
    original_threshold_price STRING NOT NULL,
    reached_threshold_price  STRING NOT NULL,
    created_at               DATE   NOT NULL DEFAULT now(),
    updated_at               DATE   NOT NULL DEFAULT now()
);