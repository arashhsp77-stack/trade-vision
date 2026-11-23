from datetime import datetime
from decimal import Decimal
from typing import Literal
from pydantic import BaseModel, Field, ConfigDict

class TradeCreate(BaseModel):
    symbol: str = Field(min_length=3, max_length=50)
    side: Literal["LONG", "SHORT"]
    timeframe: str | None = None
    leverage: Decimal | None = Field(default=None, gt=0, le=200)
    margin_mode: Literal["ISOLATED", "CROSS"] | None = None
    entry_price: Decimal = Field(gt=0)
    quantity: Decimal = Field(gt=0, description="Base-asset quantity for linear USDT-margined contracts")
    stop_loss: Decimal | None = Field(default=None, gt=0)
    take_profit: Decimal | None = Field(default=None, gt=0)
    notes: str | None = None
    visibility: Literal["PRIVATE", "LIVE"] = "PRIVATE"

class TradeClose(BaseModel):
    exit_price: Decimal = Field(gt=0)
    fees: Decimal = Field(default=Decimal("0"), ge=0)
    funding_fee: Decimal = Field(default=Decimal("0"))
    closed_at: datetime | None = None
    publish: bool = False

class TradeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    public_id: str
    exchange: str
    symbol: str
    side: str
    timeframe: str | None
    leverage: Decimal | None
    margin_mode: str | None
    status: str
    visibility: str
    entry_price: Decimal
    exit_price: Decimal | None
    stop_loss: Decimal | None
    take_profit: Decimal | None
    quantity: Decimal
    fees: Decimal
    funding_fee: Decimal
    gross_pnl: Decimal | None
    net_pnl: Decimal | None
    notes: str | None
    opened_at: datetime
    closed_at: datetime | None
    created_at: datetime
