import os
import sys
import logging
import yaml
import time
import logging.handlers as handlers
from api.loader.yaml_loader import Loader


class InitializeApp:

    def __init__(self, CONFIGURATION_FILE_PATH):
        if not os.path.exists(CONFIGURATION_FILE_PATH):
            print("Config YAMl file is not exits..")
            sys.exit(1)

        self.CONFIGURATION_FILE_PATH = CONFIGURATION_FILE_PATH
        self.__conf = self.__parse_config()

    def __validate_args(self):
        msg = "Validating required arguments and environment variables..."
        print(msg)

        if 'LOG_LOCATION' in os.environ:
            log_path = os.environ['LOG_LOCATION']
        else:
            log_path = self.__conf['MONITORING']['LOG_LOCATION']
        if not os.path.exists(log_path):
            print('Passed logging file path is not valid. File path : {}'
                  .format(log_path))
            sys.exit(1)
        else:
            self.__init_logger(log_path)

        if "API_KEY" not in os.environ:
            self.__log.error("API_KEY environment variable is not configured...")
            sys.exit(1)

        if "MYSQL_HOST" not in os.environ or "MYSQL_PORT" not in os.environ or "MYSQL_USER" not in os.environ\
                or "MYSQL_PASSWORD" not in os.environ or "MYSQL_DATABASE" not in os.environ:
            self.__log.error("MYSQL database related environment variable is not configured. Such as [MYSQL_HOST,"
                             "MYSQL_PORT,MYSQL_USER,MYSQL_PASSWORD,MYSQL_DATABASE]")
            sys.exit(1)

        self.__log.info(msg)
        self.__log.info("Validation completed successfully...")
        self.__log.info("you can find application logs at '{}' location".format(log_path))
        self.__log.info("Environment Variables : \n{}".format(os.environ))

    def __init_logger(self, log_path):
        self.__log = logging.getLogger('weather_app')
        log_handler = handlers.TimedRotatingFileHandler(log_path + '/weather_app.log'
                                                        , when='d', interval=1, backupCount=5)

        if 'LOG_LEVEL' in os.environ:
            self.__log.setLevel(os.environ['LOG_LEVEL'])
            log_handler.setLevel(os.environ['LOG_LEVEL'])
        else:
            self.__log.setLevel(logging.INFO)
            log_handler.setLevel(logging.INFO)

        # Here we set our logHandler's formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        log_handler.setFormatter(formatter)
        self.__log.addHandler(log_handler)

        # create console handler and set level to debug
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(formatter)
        self.__log.addHandler(console)

    def __parse_config(self):
        with open(self.CONFIGURATION_FILE_PATH, 'r') as config:
            conf = yaml.load(config, Loader)
        return conf

    def init(self):
        self.__validate_args()
        return self

    def get_logger(self):
        return self.__log

    def get_confi_map(self):
        return self.__conf
