import uuid
from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class Trade(Base):
    __tablename__ = "trades"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    public_id: Mapped[str] = mapped_column(String(48), unique=True, index=True)
    exchange: Mapped[str] = mapped_column(String(30), default="TOOBIT")
    symbol: Mapped[str] = mapped_column(String(50), index=True)
    side: Mapped[str] = mapped_column(String(10))
    timeframe: Mapped[str | None] = mapped_column(String(12), nullable=True)
    leverage: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    margin_mode: Mapped[str | None] = mapped_column(String(12), nullable=True)
    status: Mapped[str] = mapped_column(String(16), default="OPEN", index=True)
    visibility: Mapped[str] = mapped_column(String(16), default="PRIVATE", index=True)
    entry_price: Mapped[float] = mapped_column(Numeric(30, 12))
    exit_price: Mapped[float | None] = mapped_column(Numeric(30, 12), nullable=True)
    stop_loss: Mapped[float | None] = mapped_column(Numeric(30, 12), nullable=True)
    take_profit: Mapped[float | None] = mapped_column(Numeric(30, 12), nullable=True)
    quantity: Mapped[float] = mapped_column(Numeric(30, 12))
    fees: Mapped[float] = mapped_column(Numeric(30, 12), default=0)
    funding_fee: Mapped[float] = mapped_column(Numeric(30, 12), default=0)
    gross_pnl: Mapped[float | None] = mapped_column(Numeric(30, 12), nullable=True)
    net_pnl: Mapped[float | None] = mapped_column(Numeric(30, 12), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    opened_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
