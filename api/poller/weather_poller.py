import logging
import sys

from api.weather_api import WeatherAPI
import api.weather_util as wu


class PollerAPI:

    def __init__(self):
        self.__log = logging.getLogger('weather_app')

    def poll_current_weather_report(self, conf):
        weather = WeatherAPI(conf)
        locations = conf['METADATA']['LOCATIONS']
        for loc in locations:
            lat = loc['LAT']
            long = loc['LONG']
            city = loc['CITY']
            self.__log.info('Start polling weather data for lat : {}, log : {}, city : {} location'
                            .format(lat, long, city))
            try:
                weather_data = weather.fetch_daily_weather_report(lat, long)
            except Exception as err:
                self.__log.error("Exception occurred while polling weather data for lat: {}, lon: {}, city: {}"
                                 .format(lat, long, city))
            yield weather_data

    def poll_historical_weather_report(self, conf, days=5):
        weather = WeatherAPI(conf)
        locations = conf['METADATA']['LOCATIONS']
        weather_data_container = []
        for loc in locations:
            lat = loc['LAT']
            long = loc['LONG']
            city = loc['CITY']
            self.__log.info('Start polling weather data for lat : {}, log : {}, city : {} location'
                            .format(lat, long, city))
            try:
                past_date = wu.get_past_datetime(days)
                weather_data = weather.fetch_past_weather_report(lat, long, past_date, city)
                weather_data_container.append(weather_data)
            except Exception as err:
                self.__log.error("Exception occurred while polling weather data", exc_info=True)
                raise Exception(
                    "Exception occurred while polling weather data for lat: {}, lon: {}, city: {}, past_date: {}"
                    .format(lat, long, city, past_date))
        return weather_data_container
