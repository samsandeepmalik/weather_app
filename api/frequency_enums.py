from enum import Enum


class WeatherFreqEnum(Enum):
    CURRENT = 'current'
    MINUTELY = 'minutely'
    HOURLY = 'hourly'
    DAILY = 'daily'
    ALERTS = 'alerts'