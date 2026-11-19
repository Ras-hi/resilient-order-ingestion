
import logging
import random
import time

import httpx

from app.db import connect, save_page

logger = logging.getLogger(__name__)

SOURCE_URL = "http://127.0.0.1:8000/source/orders"
RETRYABLE = {429, 500, 502, 503, 504}


def fetch_page(client, cursor, limit=2):
    for attempt in range(3):
        try:
            response = client.get(
                SOURCE_URL,
                params={"cursor": cursor, "limit": limit},
            )

            if response.status_code in RETRYABLE:
                response.raise_for_status()

            response.raise_for_status()
            return response.json()

        except (httpx.TimeoutException,
                httpx.NetworkError,
                httpx.HTTPStatusError) as exc:

            if isinstance(exc, httpx.HTTPStatusError):
                if exc.response.status_code not in RETRYABLE:
                    raise

            if attempt == 2:
                raise

            delay = random.uniform(
                0, min(4, 0.5 * (2 ** attempt))
            )

            logger.warning(
                "Fetch failed cursor=%s attempt=%s delay=%.2f",
                cursor, attempt + 1, delay
            )
            time.sleep(delay)


def get_checkpoint():
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT next_cursor, completed
                FROM checkpoints
                WHERE source_name = 'orders'
                """
            )
            result = cur.fetchone()

    return result if result else (0, False)


def ingest():
    pages = 0

    with httpx.Client(timeout=5.0) as client:
        while True:
            cursor, completed = get_checkpoint()

            if completed:
                return {"status": "completed", "pages": pages}

            page = fetch_page(client, cursor)

            records = page["records"]
            next_cursor = page["next_cursor"]

            # TODO: validate the page and each record
            # before committing the checkpoint.

            save_page(records, next_cursor)
            pages += 1

            logger.info(
                "Committed page=%s records=%s",
                pages, len(records)
            )
