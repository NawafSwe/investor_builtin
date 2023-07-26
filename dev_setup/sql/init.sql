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
    new_price  STRING NOT NULL,
    created_at               DATE   NOT NULL DEFAULT now(),
    updated_at               DATE   NOT NULL DEFAULT now()
);


INSERT INTO alerts_rules (symbol, name, threshold_price)
VALUES ('AAPL', 'Apple Inc.', 150.00),
       ('MSFT', 'Microsoft Corporation', 250),
       ('GOOG', 'Alphabet Inc.', 2000),
       ('AMZN', 'Amazon.com, Inc.', 1000),
       ('META', 'MetLife, Inc.', 50.00);