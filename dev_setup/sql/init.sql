CREATE DATABASE IF NOT EXISTS investor_bulletin;
USE investor_bulletin;
CREATE TABLE IF NOT EXISTS alerts_rules (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  symbol TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL UNIQUE,
  threshold_price REAL NOT NULL
);