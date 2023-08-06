import pandas as pd
import psycopg2
import psycopg2.extras
import sql as sql


class DatabaseManager:

    def __init__(self, config):
        self.config = config
        self.conn = None
        self.cursor = None

    def connect_db(self):
        config = self.config
        user = config["postgres_user"]
        password = config["postgres_password"]
        host = config["db_ip_address"]
        port = config["port"]
        database = config["postgres_db"]
        try:
            conn = psycopg2.connect(
                user=user,
                password=password,
                host=host,
                database=database,
                port=port,
                cursor_factory=psycopg2.extras.RealDictCursor)

        except psycopg2.DatabaseError as error:
            self.conn.rollback()
            raise error
        self.cursor = conn.cursor()
        self.conn = conn
        self.conn.autocommit = True

    def receive_sql_fetchall(self, sql_query: str) -> pd.DataFrame:

        try:
            self.cursor.execute(sql_query)
        except psycopg2.DatabaseError as error:
            self.conn.rollback()
            raise error
        return self.cursor.fetchall()

    def send_sql(self, sql_query: str) -> pd.DataFrame:

        try:
            self.cursor.execute(sql_query)
        except psycopg2.DatabaseError as error:
            self.conn.rollback()
            raise error

    def df_insert(self, data_frame: pd.DataFrame, table: str, conflict_id: str = None):

        try:
            if not data_frame.empty:
                data_frame_columns = list(data_frame)
                columns = ",".join(data_frame_columns)
                values = "VALUES({})".format(
                    ",".join(["%s" for _ in data_frame_columns])
                )
                if conflict_id:
                    insert_query = "INSERT INTO {} ({}) {} ON CONFLICT ({}) DO NOTHING;" \
                        .format(table,
                                columns,
                                values,
                                conflict_id)
                else:
                    insert_query = "INSERT INTO {} ({}) {};" \
                        .format(table,
                                columns,
                                values)
                psycopg2.extras.execute_batch(
                    self.cursor, insert_query, data_frame.values
                )
        except psycopg2.DatabaseError as error:
            self.conn.rollback()
            raise error

    def close_conn(self):

        self.cursor.close()

    def update_df(self, data_frame: pd.DataFrame, table: str):

        for i in range(len(data_frame)):
            row = data_frame.iloc[i]
            self.send_sql(sql.update_table(table, row))
