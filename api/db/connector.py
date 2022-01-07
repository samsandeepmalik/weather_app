import logging
import sys
import os

from pymysql import OperationalError
from api.db.mysql_adaptor import MYSQL


class DBUtil:

    def __init__(self, conf):
        self.__log = logging.getLogger('weather_app')
        self.__active_db = conf['ACTIVE_DB']
        conn_details = conf['DB'][self.__active_db]
        self.__db_name = os.environ['MYSQL_DATABASE']
        self.__host = os.environ['MYSQL_HOST']
        self.__port = os.environ['MYSQL_PORT']
        self.__port = conn_details['port']
        self.__user = os.environ['MYSQL_USER']
        self.__password = os.environ['MYSQL_PASSWORD']

    def connect_db(self):
        self.__log.info("Initializing {} database connection".format(self.__active_db))
        try:
            if self.__active_db == 'MYSQL':
                mysql = MYSQL(self.__log)
                mysql.init_db(self.__host,
                              self.__port,
                              self.__user,
                              self.__password,
                              self.__db_name)
                return mysql
            else:
                return None
        except OperationalError:
            self.__log.error("Exception occurred while trying to connect to {} database : "
                             .format(self.__active_db, self.__active_db),
                             exc_info=True)
            sys.exit(1)


