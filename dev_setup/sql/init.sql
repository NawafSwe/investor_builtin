CREATE DATABASE IF NOT EXISTS investor_bulletin;
USE investor_bulletin;
CREATE TABLE IF NOT EXISTS alerts_rules (
  id INTEGER NOT NULL,
  symbol TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL UNIQUE,
  threshold_price REAL NOT NULL,
  PRIMARY KEY (id)
);