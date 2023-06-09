from typing import List, Optional
from fastapi import FastAPI, Query

app = FastAPI()

# Example list of trades
trades = [
    {
        "trade_id": "1",
        "asset_class": "Equity",
        "counterparty": "ABC Corp",
        "instrument_id": "TSLA",
        "instrument_name": "Tesla Inc",
        "trade_date_time": "2023-05-01T10:00:00",
        "trade_details": {
            "buySellIndicator": "BUY",
            "price": 100.0,
            "quantity": 10
        },
        "trader": "John Doe"
    },
    # Add more trade entries here
]

# Endpoint to fetch a list of trades with pagination and sorting
@app.get("/trades")
def get_trades(
    asset_class: Optional[str] = Query(None, description="Asset class of the trade."),
    end: Optional[str] = Query(None, description="The maximum date for the tradeDateTime field."),
    max_price: Optional[float] = Query(None, description="The maximum value for the tradeDetails.price field."),
    min_price: Optional[float] = Query(None, description="The minimum value for the tradeDetails.price field."),
    start: Optional[str] = Query(None, description="The minimum date for the tradeDateTime field."),
    trade_type: Optional[str] = Query(None, description="The tradeDetails.buySellIndicator is a BUY or SELL"),
    page: int = Query(1, description="Page number"),
    limit: int = Query(10, description="Number of trades per page"),
    sort_by: Optional[str] = Query(None, description="Field to sort by")
):
    filtered_trades = trades

    if asset_class:
        filtered_trades = [trade for trade in filtered_trades if trade.get("asset_class") == asset_class]

    if end:
        filtered_trades = [trade for trade in filtered_trades if trade.get("trade_date_time") <= end]

    if max_price:
        filtered_trades = [trade for trade in filtered_trades if trade.get("trade_details", {}).get("price") <= max_price]

    if min_price:
        filtered_trades = [trade for trade in filtered_trades if trade.get("trade_details", {}).get("price") >= min_price]

    if start:
        filtered_trades = [trade for trade in filtered_trades if trade.get("trade_date_time") >= start]

    if trade_type:
        filtered_trades = [trade for trade in filtered_trades if trade.get("trade_details", {}).get("buySellIndicator") == trade_type]

    # Sorting trades
    if sort_by:
        filtered_trades = sorted(filtered_trades, key=lambda x: x.get(sort_by, ""))

    # Pagination
    start_index = (page - 1) * limit
    end_index = start_index + limit
    paginated_trades = filtered_trades[start_index:end_index]

    return paginated_trades

# Endpoint to fetch a single trade by ID
@app.get("/trades/{trade_id}")
def get_trade_by_id(trade_id: str):
    for trade in trades:
        if trade.get("trade_id") == trade_id:
            return trade
    return {"error": "Trade not found"}

# Endpoint for searching trades
@app.get("/trades/search")
def search_trades(search: str = Query(..., description="Search term")):
    search = search.lower()
    searched_trades = []

    for trade in trades:
        if (
            search in trade.get("counterparty", "").lower()
            or search in trade.get("instrument_id", "").lower()
            or search in trade.get("instrument_name", "").lower()
            or search in trade.get("trader", "").lower()
        ):
            searched_trades.append(trade)

    return searched_trades