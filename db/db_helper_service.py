import mysql.connector


class DatabaseHelperService:
    def __init__(self, name):
        self._conn = mysql.connector.connect(host="localhost",
                                             user="root",
                                             database=name)
        self._cursor = self._conn.cursor()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

