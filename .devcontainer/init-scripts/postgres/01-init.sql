CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE SCHEMA IF NOT EXISTS trading;

CREATE TABLE IF NOT EXISTS trading.discovered_bots (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    address VARCHAR(42) NOT NULL,
    chain VARCHAR(20) NOT NULL,
    discovery_time TIMESTAMP NOT NULL DEFAULT NOW(),
    score DECIMAL(5,4) NOT NULL,
    strategy_type VARCHAR(50),
    performance_metrics JSONB,
    metadata JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
