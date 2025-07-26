from fastapi import APIRouter, HTTPException
from app.models.ohlcv import OHLCV
from app.db.supabase_client import get_server_access
from app.db.sql_loader import render_sql_template
import pandas as pd

router = APIRouter()

@router.get("/ohlcv/{ticker}", response_model=OHLCV)
async def get_ohlcv(ticker: str):
    try:
        supabase = get_server_access()
    except Exception as e:
        # Handle DB connection errors
        raise HTTPException(status_code=500, detail=f"Database connection error: {e}")

    try:
        sql = render_sql_template(
            "get_ohlcv.sql.j2",
            ticker=ticker  # use the requested symbol, not hardcoded "FCCL"
        )
        print(sql)
    except Exception as e:
        # Handle SQL template rendering errors
        raise HTTPException(status_code=500, detail=f"SQL template error: {e}")

    try:
        df = pd.read_sql(sql=sql, con=supabase)
        df['dt'] = df['dt'].astype(str)
        print(df)
    except Exception as e:
        # Handle SQL execution errors
        raise HTTPException(status_code=500, detail=f"Error executing SQL: {e}")

    # DataFrame checks and conversion
    try:
        if df.empty:
            raise HTTPException(status_code=404, detail=f"No OHLCV data found for ticker '{ticker}'.")

        required_columns = {'open', 'high', 'low', 'close', 'volume', 'ticker', 'dt'}
        missing_cols = required_columns - set(df.columns)
        if missing_cols:
            raise HTTPException(status_code=500, detail=f"Missing columns in result: {', '.join(missing_cols)}")

        record = df.iloc[0]
        return OHLCV(
            open=record['open'],
            high=record['high'],
            low=record['low'],
            close=record['close'],
            volume=record['volume'],
            ticker=record['ticker'],
            dt=record['dt']
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing OHLCV data: {e}")
