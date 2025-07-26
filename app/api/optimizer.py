from fastapi import APIRouter, HTTPException, Query
from app.utils.calculations import get_optimal_sell_price_psx

router = APIRouter()

@router.get("/optimal-sell-price/")
async def optimal_sell_price_psx(
    target_profit: float = Query(..., gt=0, description="Target profit amount"),
    buy_price: float = Query(..., gt=0, description="Buy price"),
    num_shares: int = Query(..., gt=0, description="Number of shares"),
    day_trade: bool = False
):
    try:
        sell_price = get_optimal_sell_price_psx(target_profit, buy_price, num_shares, day_trade)
        return {"sell_price": round(sell_price, 2)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))