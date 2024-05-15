from psycopg2.extras import NamedTupleCursor
import psycopg2


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
        return self.curs

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print("Ошибка подключения к базе данных:", exc_val)
        self.curs.close()
        self.conn.commit()
        self.conn.close()


class URLRepository:
    """This class is used to work with
    the postgresql database to write
    and extract data according to templates
    in the database.sql file.
    """
    def __init__(self, db_url) -> None:
        self.db_url = db_url

    def create_url(self, name):
        with ConnectDB(self.db_url) as curs:
            curs.execute("""INSERT INTO urls (name)
                            VALUES
                                (%s)
                            RETURNING id;""", (name,))
            return curs.fetchone().id

    def create_url_check(self, id, status_code, h1, title, description):
        with ConnectDB(self.db_url) as curs:
            curs.execute("""INSERT INTO url_checks (
                                url_id,
                                status_code,
                                h1,
                                title,
                                description)
                            VALUES
                                (%s, %s, %s, %s, %s);
                                """, (id, status_code, h1, title, description))

    def find_all_urls(self):
        with ConnectDB(self.db_url) as curs:
            curs.execute("""SELECT
                            urls.id AS id,
                            urls.name,
                            url_checks.created_at as last_check,
                            url_checks.status_code
                        FROM urls
                        LEFT JOIN url_checks
                            ON urls.id = url_checks.url_id
                            AND url_checks.id = (SELECT max(id)
                                                FROM url_checks
                                                WHERE urls.id = url_id)
                        ORDER BY
                            urls.id DESC;""")
            return curs.fetchall()

    def find_url_by_name(self, name):
        with ConnectDB(self.db_url) as curs:
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
        with ConnectDB(self.db_url) as curs:
            curs.execute('''SELECT
                                id,
                                name,
                                created_at
                            FROM
                                urls
                            WHERE
                                id = %s;''', (id,))
            return curs.fetchone()

    def find_url_check(self, id):
        with ConnectDB(self.db_url) as curs:
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
