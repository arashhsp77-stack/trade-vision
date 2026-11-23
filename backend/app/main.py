import os
import secrets
from datetime import datetime, timezone
from decimal import Decimal
from fastapi import FastAPI, Depends, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import desc
from .database import Base, engine, get_db
from .models import Trade
from .schemas import TradeCreate, TradeClose, TradeOut

Base.metadata.create_all(bind=engine)
app = FastAPI(title="TRADE VISION API", version="0.1.0")
origins = [x.strip() for x in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=False,
                   allow_methods=["GET", "POST", "PATCH", "OPTIONS"],
                   allow_headers=["Authorization", "Content-Type"])

def require_admin(authorization: str | None = Header(default=None)):
    expected = os.getenv("ADMIN_API_TOKEN", "")
    if not expected or expected.startswith("CHANGE_ME"):
        raise HTTPException(status_code=503, detail="Admin token is not configured securely.")
    supplied = authorization.removeprefix("Bearer ").strip() if authorization else ""
    if not secrets.compare_digest(supplied, expected):
        raise HTTPException(status_code=401, detail="Invalid admin token.")
    return True

@app.get("/health")
def health():
    return {"status": "ok", "service": "trade-vision-api"}

@app.post("/api/admin/trades", response_model=TradeOut, dependencies=[Depends(require_admin)])
def create_trade(payload: TradeCreate, db: Session = Depends(get_db)):
    public_id = f"{payload.symbol.upper().replace('-', '')}-{secrets.token_hex(3).upper()}"
    trade = Trade(public_id=public_id, symbol=payload.symbol.upper(), side=payload.side,
                  timeframe=payload.timeframe, leverage=payload.leverage, margin_mode=payload.margin_mode,
                  entry_price=payload.entry_price, quantity=payload.quantity, stop_loss=payload.stop_loss,
                  take_profit=payload.take_profit, notes=payload.notes, visibility=payload.visibility, status="OPEN")
    db.add(trade); db.commit(); db.refresh(trade)
    return trade

@app.post("/api/admin/trades/{trade_id}/close", response_model=TradeOut, dependencies=[Depends(require_admin)])
def close_trade(trade_id: str, payload: TradeClose, db: Session = Depends(get_db)):
    trade = db.get(Trade, trade_id)
    if not trade: raise HTTPException(status_code=404, detail="Trade not found")
    if trade.status != "OPEN": raise HTTPException(status_code=409, detail="Trade is already closed")
    entry, qty = Decimal(str(trade.entry_price)), Decimal(str(trade.quantity))
    gross = (payload.exit_price-entry)*qty if trade.side == "LONG" else (entry-payload.exit_price)*qty
    net = gross - payload.fees - payload.funding_fee
    trade.exit_price, trade.fees, trade.funding_fee = payload.exit_price, payload.fees, payload.funding_fee
    trade.gross_pnl, trade.net_pnl = gross, net
    trade.closed_at = payload.closed_at or datetime.now(timezone.utc)
    trade.status = "CLOSED"
    if payload.publish: trade.visibility = "PUBLIC"
    db.commit(); db.refresh(trade)
    return trade

@app.get("/api/admin/trades", response_model=list[TradeOut], dependencies=[Depends(require_admin)])
def admin_trades(db: Session = Depends(get_db)):
    return db.query(Trade).order_by(desc(Trade.created_at)).limit(200).all()

@app.get("/api/public/trades", response_model=list[TradeOut])
def public_trades(db: Session = Depends(get_db)):
    return db.query(Trade).filter(Trade.visibility.in_(["LIVE", "PUBLIC"])).order_by(desc(Trade.created_at)).limit(100).all()
