
from app.db import connect, save_page


def test_duplicate_orders_do_not_create_extra_rows():
    records = [
        {"id": "TEST101", "amount": 100},
        {"id": "TEST102", "amount": 200},
        {"id": "TEST101", "amount": 100},
    ]

    save_page(records, None)
    save_page(records, None)

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT COUNT(*)
                FROM orders
                WHERE id LIKE 'TEST%'
                """
            )
            count = cur.fetchone()[0]

    assert count == 2
