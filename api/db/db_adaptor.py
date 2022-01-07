import logging
from api.db.connector import DBUtil


class DBAdaptor:

    def __init__(self, conf):
        self.__log = logging.getLogger('weather_app')
        self.__db = DBUtil(conf).connect_db()

    def write(self, insert_stmt, weather_data):
        return self.__db.insert_batch(insert_stmt, weather_data)

    def read_daily_weather(self, table_name):
        dataset = self.__db.execute_query("SELECT * FROM {}}".format(table_name))
        columns = self.__db.get_table_columns('table_name')
        return columns, dataset

    def process_weather_data(self, sql_statement):
        return self.__db.execute_sql(sql_statement)