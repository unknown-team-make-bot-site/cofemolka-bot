import datetime
import sqlite3 as sql

from singleton import Singleton


class DatabaseUtils(object, metaclass=Singleton):
    TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self):
        self.conn = sql.connect('../mydb.db', check_same_thread=False)

    def connect(self):
        self.conn = sql.connect('../mydb.db', check_same_thread=False)

    def create_table(self, tablename, cols_str):
        current = self.conn.cursor()
        q = f"CREATE TABLE IF NOT EXISTS {tablename} ({cols_str});"
        current.execute(q)
        self.conn.commit()

    def close(self):
        self.conn.close()

    def exec(self, query, values = ""):
            if not self.conn:
                self.connect()
            cursor = self.conn.cursor()
            cursor.execute(query, values)
            self.conn.commit()
            return cursor

    def exec_one_value(self, query, value = ""):
        if not self.conn:
            self.connect()
        cursor = self.conn.cursor()
        cursor.execute(query, (value,))
        self.conn.commit()
        return cursor

    def add(self, table, col_list="", values=""):
        columns = ", ".join([col for col in col_list])
        query = f"""
        INSERT INTO
        {table} ({columns})
        VALUES
        (?, ?, ?, ?, ?, ?);
        """
        cursor = self.exec(query, values=values)
        return cursor.lastrowid

    def add_one_column(self, table, col_list="", values=""):
        columns = ", ".join([col for col in col_list])
        query = f"""
        INSERT INTO
        {table} ({columns})
        VALUES
        (?);
        """
        cursor = self.exec_one_value(query, value=values)
        return cursor.lastrowid

    def delete_row(self, table, row_id):
        query = f"DELETE FROM {table} WHERE id = {row_id}"
        self.exec(query)

    def exec_fetchone(self, query):
        if not self.conn:
            self.connect()
        cursor = self.conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        return result

    def exec_fetchall(self, query):
        if not self.conn:
            self.connect()
        cursor = self.conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def get_rows_count(self, table):
        query = f"""
        SELECT COUNT(*) FROM {table}
        """

        return self.exec_fetchone(query)

    def close(self):
        if self.conn: self.conn.close()

    def get(self, table):
        query = f"""
        SELECT * FROM {table}
        """
        return self.exec_fetchall(query)

    def get_type(self, table, type):
        query = f"""
        SELECT * FROM {table} WHERE type={type}"""
        return self.exec_fetchall(query)

    def get_by_ids(self, ids, table):
        if len(ids) == 0: return None
        query = f"""
               SELECT * FROM {table} WHERE id in ({", ".join([str(id) for id in ids])})
               """
        return self.exec_fetchall(query)

    def update_row(self, table, row_id, updates_str):
        query = f"UPDATE {table} SET {updates_str} WHERE id = {row_id}"
        return self.exec(query)

    @staticmethod
    def timestamp_to_sql_time(ts):
        return datetime.datetime.fromtimestamp(ts).strftime(DatabaseUtils.TIME_FORMAT)

    def get_by_id(self, row_id, table):
        return self.get_by_ids([row_id], table=table)[0]

    def get_by_param(self, param, val, table):
        query = f"SELECT * FROM {table} WHERE {param} = '{val}';"
        return self.exec_fetchall(query)

    def delete_all(self, table_name):
        query = f"DELETE FROM {table_name}"
        return self.exec(query)

    def delete_table(self, table_name):
        query = f"DROP TABLE {table_name}"
        return self.exec_one_value(query)
