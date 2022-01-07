import json
import logging

from api.db.db_adaptor import DBAdaptor
from api.weather_util import convert_to_human_readable_format

INSERT_STMT_FOR_DAILY_WEATHER = '''
REPLACE INTO WEATHER.DAILY_WEATHER (
    WEATHER_DATE,LAT,LON,TYPE,TIMEZONE,TIMEZONE_OFFSET,SUNRISE,SUNSET,TEMP,FEELS_LIKE,PRESSURE,
    HUMIDITY,DEW_POINT,CLOUDS,VISIBILITY,WIND_SPEED,WIND_DEG,WEATHER
    ) VALUES ({})
'''.format(",".join(('%s ' * 18).split()))

INSERT_STMT_FOR_HOURLY_WEATHER = '''
REPLACE INTO WEATHER.HOURLY_WEATHER (
    WEATHER_DATE,LAT,LON,TEMP,FEELS_LIKE,PRESSURE,
    HUMIDITY,DEW_POINT,CLOUDS,VISIBILITY,WIND_SPEED,WIND_DEG,WEATHER
    ) VALUES ({})
'''.format(",".join(('%s ' * 13).split()))


class AppWriter:

    def __init__(self, conf):
        self.__conf = conf
        self.__adaptor = DBAdaptor(conf)
        self.__log = logging.getLogger('weather_app')

    def write_weather_data(self, dataset):
        daily_dataset = list(self.__map_daily_weather_data(dataset))
        if self.__adaptor.write(INSERT_STMT_FOR_DAILY_WEATHER, daily_dataset):
            hourly_dataset = self.__extract_hourly_data(dataset)
            mapped_hourly_dataset = list(self.__map_hourly_weather_data(hourly_dataset))
            self.__log.info("MySQL Insert statement is : \n{}".format(INSERT_STMT_FOR_HOURLY_WEATHER))
            return self.__adaptor.write(INSERT_STMT_FOR_HOURLY_WEATHER, mapped_hourly_dataset)
        else:
            return False

    def __write_hourly_weather_data(self, hourly_dataset):
        pass

    def __extract_hourly_data(self, dataset):
        hourly_dataset = []
        for data in dataset:
            hourly_dataset.append({(data['lat'], data['lon']): data['hourly']})
        return list(hourly_dataset)

    def __map_hourly_weather_data(self, dataset):
        for data_list in dataset:
            for key, value in data_list.items():
                lat, lon = key
                for data in value:
                    yield [
                        str(convert_to_human_readable_format(data['dt'])),
                        lat,
                        lon,
                        data['temp'],
                        data['feels_like'],
                        data['pressure'],
                        data['humidity'],
                        data['dew_point'],
                        data['clouds'],
                        data['visibility'],
                        data['wind_speed'],
                        data['wind_deg'],
                        json.dumps(data['weather'])
                    ]

    def __map_daily_weather_data(self, dataset):
        for data in dataset:
            yield [
                str(convert_to_human_readable_format(data['current']['dt'])),
                data['lat'],
                data['lon'],
                data['TYPE'],
                data['timezone'],
                data['timezone_offset'],
                data['current']['sunrise'],
                data['current']['sunset'],
                data['current']['temp'],
                data['current']['feels_like'],
                data['current']['pressure'],
                data['current']['humidity'],
                data['current']['dew_point'],
                data['current']['clouds'],
                data['current']['visibility'],
                data['current']['wind_speed'],
                data['current']['wind_deg'],
                json.dumps(data['current']['weather'])
            ]
