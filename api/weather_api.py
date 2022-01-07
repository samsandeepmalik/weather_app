import logging

import requests
from api.frequency_enums import WeatherFreqEnum
import api.weather_util as wu
import os


class WeatherAPI:

    def __init__(self, conf):
        self.__BASE_URL = conf['API']['base_url']
        self.__TIMEMACHINE_BASE_URL = conf['API']['past_data_base_url']
        self.__API_KEY = os.environ['API_KEY']
        self.__log = logging.getLogger('weather_app')

    def __fetch_weather_info(self, lat, long, lang, excludes):
        url = self.__BASE_URL + "appid={}&lat={}&lon={}&lang={}&exclude={}" \
            .format(self.__API_KEY, lat, long, lang, excludes)
        print(url)
        return requests.get(url)

    def __build_excludes(self, except_freq):
        for freq in WeatherFreqEnum:
            if freq not in except_freq and freq != WeatherFreqEnum.CURRENT:
                yield freq.value

    def fetch_daily_weather_report(self, lat, long, lang='en',
                                   frequency=[WeatherFreqEnum.DAILY, WeatherFreqEnum.HOURLY]):
        excludes = ",".join(list(self.__build_excludes(frequency)))
        data = self.__fetch_weather_info(lat, long, lang, excludes).json()
        data['TYPE'] = 'CURRENT'
        return data

    def fetch_past_weather_report(self, lat, long, past_date, city=None, lang='en'):
        unix_time = wu.convert_to_unix_time(past_date)

        url = self.__TIMEMACHINE_BASE_URL + "lat={}&lon={}&lang={}&dt={}&appid={}" \
            .format(lat, long, lang, unix_time, self.__API_KEY)
        self.__log.debug(url)
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            data['TYPE'] = 'PAST'
            return data
        else:
            response.raise_for_status()
