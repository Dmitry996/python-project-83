from psycopg2.extras import NamedTupleCursor
import psycopg2
import time


class ConnectDB:
    """
    This class is used to work with
    the postgresql database in the context manager.
    """
    def __init__(self, db_url) -> None:
        self.db_url = db_url

    def __enter__(self):
        self.conn = psycopg2.connect(self.db_url)
        self.curs = self.conn.cursor(cursor_factory=NamedTupleCursor)
        self.start_time = time.time()  # noqa: E501 проверка времени запроса к бд
        return self.curs

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print("Ошибка подключения к базе данных:", exc_val)
        self.curs.close()
        self.conn.commit()
        self.conn.close()
        elapsed_time = time.time() - self.start_time  # noqa: E501 проверка времени запроса к бд
        print(f"Elapsed time: {elapsed_time} seconds")  # noqa: E501 распечатка времени запроса


class URLRepository:
    def __init__(self, db_url) -> None:
        self.db_url = db_url

    def connect(self):
        self.conn = psycopg2.connect(self.db_url)
        return self.conn

    def create_url(self, name):
        with self.connect() as conn:
            with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
                curs.execute("""INSERT INTO
                                urls (name)
                                VALUES
                                (%s)
                                RETURNING id;""", (name,))
                return curs.fetchone().id

    def find_all_urls(self):
        with self.connect() as conn:
            with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
                curs.execute("""SELECT
                                    id,
                                    name,
                                    created_at
                                FROM
                                    urls
                                ORDER BY
                                    id DESC;""")
                return curs.fetchall()

    def find_url_by_name(self, name):
        with self.connect() as conn:
            with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
                curs.execute('''SELECT
                                    id,
                                    name,
                                    created_at
                                FROM
                                    urls
                                WHERE
                                    name = %s;''', (name,))
                return curs.fetchone()

    def find_url_by_id(self, id):
        with self.connect() as conn:
            with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
                curs.execute('''SELECT
                                    id,
                                    name,
                                    created_at
                                FROM
                                    urls
                                WHERE
                                    id = %s;''', (id,))
                return curs.fetchone()

    def create_url_check(self, id, status_code, h1, title, description):
        with self.connect() as conn:
            with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
                curs.execute("""INSERT INTO url_checks (
                                    url_id,
                                    status_code,
                                    h1,
                                    title,
                                    description)
                                VALUES
                                    (%s, %s, %s, %s, %s);
                                """, (id, status_code, h1, title, description))

    def find_url_check(self, id):
        with self.connect() as conn:
            with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
                curs.execute("""SELECT
                                    id,
                                    url_id,
                                    status_code,
                                    h1,
                                    title,
                                    description,
                                    created_at
                                FROM
                                    url_checks
                                WHERE
                                    url_id = %s
                                ORDER BY
                                    id DESC;""", (id,))
                return curs.fetchall()

    def find_all_url_checks(self):
        with self.connect() as conn:
            with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
                curs.execute("""SELECT
                                    id,
                                    url_id,
                                    status_code,
                                    h1,
                                    title,
                                    description,
                                    created_at
                                FROM
                                    url_checks
                                ORDER BY
                                    url_id, created_at DESC;""")
                return curs.fetchall()
