from contextlib import contextmanager
from tiny_url import APP_SETTINGS
import psycopg2


@contextmanager
def get_database_connection():
    conn = psycopg2.connect(
        dbname=APP_SETTINGS.DB_NAME,
        user=APP_SETTINGS.DB_USER,
        password=APP_SETTINGS.DB_PASSWORD,
        host=APP_SETTINGS.DB_HOST,
        port=APP_SETTINGS.DB_PORT
    )

    cursor = conn.cursor()

    yield cursor

    conn.commit()
    cursor.close()
    conn.close()
