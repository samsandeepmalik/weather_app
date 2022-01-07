import datetime
import sys
import time

from api.db.db_adaptor import DBAdaptor
from api.initializer import InitializeApp
from api.model.writer import AppWriter
from api.poller.weather_poller import PollerAPI
from api.processor.weather_data_processor import WeatherProcessor


def init():
    return InitializeApp('./config/app_conf.yaml').init()


def process(conf_dict):
    processor = WeatherProcessor(conf_dict)
    return processor.process()


if __name__ == "__main__":

    initializer = init()
    global conf, log
    conf = initializer.get_confi_map()
    log = initializer.get_logger()
    welcome_text = '''
****************************************************************
*                           WEATHER APP                        *
****************************************************************
    '''
    log.info("Waiting MySQL DB to start up for 60 seconds...")
    time.sleep(60)

    log.info("\n{}\n".format(welcome_text))
    log.info("Starting at {}\n".format(datetime.datetime.now()))
    api_poller = PollerAPI()
    writer = AppWriter(conf)
    try:
        for day in range(0, 5):
            weather_info = api_poller.poll_historical_weather_report(conf, day)
            historical_data = list(weather_info)
            data_size = len(historical_data)
            if data_size < 10:
                log.warning("Weather dataset size is less than expected, please check the logs for more information")

            if data_size > 0:
                transformed_dataset = list(historical_data)
                if not writer.write_weather_data(transformed_dataset):
                    raise Exception("Exception occurred while persisting weather data in MySQL DB. "
                                    "For more information on exception please check logs")
                else:
                    if not process(conf):
                        raise Exception("Exception occurred while processing weather data. "
                                        "For more information on exception please check logs")
    except Exception as err:
        log.error("Exception occurred polling and persisting the data", exc_info=True)
        sys.exit(1)

    log.info("Completing at {}\n".format(datetime.datetime.now()))
