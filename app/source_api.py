
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/source")

ORDERS = [
    {"id": "O101", "amount": 100},
    {"id": "O102", "amount": 200},
    {"id": "O103", "amount": 300},
    {"id": "O103", "amount": 300},
    {"id": "O104", "amount": 400},
    {"id": "O105", "amount": 500},
]


@router.get("/orders")
def get_orders(cursor: int = 0, limit: int = 2):
    if cursor < 0 or limit < 1 or limit > 100:
        raise HTTPException(400, "Invalid pagination")

    page = ORDERS[cursor:cursor + limit]
    next_position = cursor + limit

    next_cursor = (
        next_position
        if next_position < len(ORDERS)
        else None
    )

    return {
        "records": page,
        "next_cursor": next_cursor,
    }
