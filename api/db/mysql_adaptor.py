import pymysql


class MYSQL:

    def __init__(self, logger, charset="utf-8"):
        self.__db_name = None
        self.connection = None
        self.__conn = None
        self.__log = logger
        self.__charset = charset

    def init_db(self, host, port, user, password, db_name):
        self.__db_name = db_name
        self.__conn = pymysql.connect(host=host, port=port, user=user, password=password, db=self.__db_name)

    def check_connection(self):
        self.__conn.ping(reconnect=True)

    def close_db(self):
        self.__conn.close()

    def get_table_columns(self, table_name):
        stmt = '''	SELECT COLUMN_NAME 
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_SCHEMA = '{}'
                    AND TABLE_NAME = '{}' 
                '''.format(self.__db_name, table_name)
        return self.execute_query(stmt)

    def execute_query(self, sql):
        try:
            # execute sql statement
            cursor = self.__conn.cursor()
            cursor.execute(sql)
            # get all rows in mysql
            results = cursor.fetchall()
            return results
        except Exception as exc:
            self.__log.error("Error: unable to fetch data", exc_info=True)
            print(exc.with_traceback())

    def execute_sql(self, sql):
        # sql is insert, delete or update statement
        cursor = self.__conn.cursor()
        try:
            cursor.execute(sql)
            cursor.close()
        except Exception as exc:
            self.__conn.rollback()
            self.__log.error("Error: unable to update data", exc_info=True)
            return False
        # commit sql to mysql
        self.__conn.commit()
        return True

    def insert_batch(self, sql, dataset):
        # sql is insert, delete or update statement
        with self.__conn.cursor() as cursor:
            try:
                cursor.executemany(sql, dataset)
                self.__conn.commit()
                return True
            except Exception as exc:
                self.__conn.rollback()
                self.__log.error("Error: unable to update data", exc_info=True)
                return False
            # commit sql to mysql
