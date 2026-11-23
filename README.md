# TRADE VISION — V1 Starter

A first working foundation for a public crypto-futures trading journal.

## Included
- Next.js dark admin panel for manually registering trades
- FastAPI backend
- PostgreSQL database via Docker Compose
- Initial trade schema and basic long/short PnL calculation
- Admin API token protection for write/admin endpoints
- Public read-only trade list endpoint

## Important scope and safety
This is a development starter, not a production deployment. Before exposing it publicly:
1. Replace `CHANGE_ME_LONG_RANDOM_SECRET` with a strong random secret.
2. Add HTTPS, backups, rate limits, monitoring, and proper user authentication.
3. Review the exchange contract specifications for every symbol.
4. The initial PnL formula assumes a linear USDT-margined contract and quantity expressed in base-asset units. Inverse contracts and contract-multiplier instruments need a symbol-specific calculation adapter.
5. Trades entered manually are not independently verified executions. Public pages must not imply exchange-verified execution.
6. Do not add Toobit trading credentials or API keys to this project. V1 needs public market data only.

## Requirements
- Docker Desktop
- Node.js 20+
- Python 3.11+ (only if running backend outside Docker)

## Start database + backend
From this folder:

```bash
docker compose up --build
```

Backend API: http://localhost:8000  
API docs: http://localhost:8000/docs

The backend reads `ADMIN_API_TOKEN` from `.env`.

## Start frontend
Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:3000

If needed, create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

In the admin panel, paste the same `ADMIN_API_TOKEN` value from the root `.env`.

## Environment
Copy `.env.example` to `.env`, then change the token before use.

## First test
1. Open http://localhost:3000
2. Enter the admin token.
3. Register a test trade.
4. Confirm it appears in the table.
5. Open http://localhost:8000/docs to inspect the API.

## Next development milestones
- Trade fills (partial entries/exits)
- Image upload to private object storage
- Trade event/audit log
- Toobit public futures candles and symbol metadata
- Interactive public trade-detail chart
- Verified performance calculations and snapshots
- Separate public website and admin authentication
