from fastapi import FastAPI
from app.api import ohlcv, optimizer

app = FastAPI(
    title="OHLCV API",
    version="0.1.0"
)

app.include_router(ohlcv.router, prefix="/api")
app.include_router(optimizer.router, prefix="/api")