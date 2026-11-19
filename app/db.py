
import os
import psycopg

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://orders:localdev@localhost:5432/ordersdb"
)


def connect():
    return psycopg.connect(DATABASE_URL)


def save_page(records, next_cursor):
    with connect() as conn:
        with conn.cursor() as cur:
            for order in records:
                cur.execute(
                    """
                    INSERT INTO orders (id, amount)
                    VALUES (%s, %s)
                    ON CONFLICT (id)
                    DO UPDATE SET amount = EXCLUDED.amount
                    """,
                    (order["id"], order["amount"]),
                )

            cur.execute(
                """
                INSERT INTO checkpoints
                    (source_name, next_cursor, completed)
                VALUES ('orders', %s, %s)
                ON CONFLICT (source_name)
                DO UPDATE SET
                    next_cursor = EXCLUDED.next_cursor,
                    completed = EXCLUDED.completed
                """,
                (next_cursor, next_cursor is None),
            )
