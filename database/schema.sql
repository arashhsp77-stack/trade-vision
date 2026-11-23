CREATE TABLE IF NOT EXISTS trades (
    id UUID PRIMARY KEY,
    public_id VARCHAR(48) UNIQUE NOT NULL,
    exchange VARCHAR(30) NOT NULL DEFAULT 'TOOBIT',
    symbol VARCHAR(50) NOT NULL,
    side VARCHAR(10) NOT NULL CHECK (side IN ('LONG','SHORT')),
    timeframe VARCHAR(12),
    leverage NUMERIC(10,2),
    margin_mode VARCHAR(12) CHECK (margin_mode IN ('ISOLATED','CROSS')),
    status VARCHAR(16) NOT NULL DEFAULT 'OPEN',
    visibility VARCHAR(16) NOT NULL DEFAULT 'PRIVATE',
    entry_price NUMERIC(30,12) NOT NULL,
    exit_price NUMERIC(30,12),
    stop_loss NUMERIC(30,12),
    take_profit NUMERIC(30,12),
    quantity NUMERIC(30,12) NOT NULL,
    fees NUMERIC(30,12) NOT NULL DEFAULT 0,
    funding_fee NUMERIC(30,12) NOT NULL DEFAULT 0,
    gross_pnl NUMERIC(30,12),
    net_pnl NUMERIC(30,12),
    notes TEXT,
    opened_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    closed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS ix_trades_symbol ON trades(symbol);
CREATE INDEX IF NOT EXISTS ix_trades_status ON trades(status);
CREATE INDEX IF NOT EXISTS ix_trades_visibility ON trades(visibility);

-- Planned V1.1 tables: trade_fills, trade_events, trade_images, market_candles.
-- They are intentionally not exposed as production features in this first starter.
