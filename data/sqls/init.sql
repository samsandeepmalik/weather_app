CREATE TABLE IF NOT EXISTS `WEATHER`.`DAILY_WEATHER` (
  `weather_date` datetime NOT NULL,
  `lat` decimal(10,5) NOT NULL,
  `lon` decimal(10,5) NOT NULL,
  `type` varchar(20) NOT NULL,
  `timezone` varchar(100) NOT NULL,
  `timezone_offset` int NOT NULL,
  `sunrise` bigint NOT NULL,
  `sunset` bigint NOT NULL,
  `temp` decimal(10,0) DEFAULT NULL,
  `feels_like` decimal(10,0) NOT NULL,
  `pressure` int NOT NULL,
  `humidity` int NOT NULL,
  `dew_point` decimal(10,0) NOT NULL,
  `clouds` int NOT NULL,
  `visibility` int NOT NULL,
  `wind_speed` int NOT NULL,
  `wind_deg` int NOT NULL,
  `weather` json DEFAULT NULL,
  PRIMARY KEY (`weather_date`,`lat`,`lon`),
  KEY `ix_DAILY_WEATHER_lon` (`lon`),
  KEY `ix_DAILY_WEATHER_lat` (`lat`),
  KEY `ix_DAILY_WEATHER_weather_date` (`weather_date`)
);

CREATE TABLE IF NOT EXISTS `WEATHER`.`HOURLY_WEATHER` (
  `weather_date` datetime NOT NULL,
  `lat` decimal(10,5) NOT NULL,
  `lon` decimal(10,5) NOT NULL,
  `temp` decimal(10,0) DEFAULT NULL,
  `feels_like` decimal(10,0) NOT NULL,
  `pressure` int NOT NULL,
  `humidity` int NOT NULL,
  `dew_point` decimal(10,0) NOT NULL,
  `clouds` int NOT NULL,
  `visibility` int NOT NULL,
  `wind_speed` int NOT NULL,
  `wind_deg` int NOT NULL,
  `weather` json DEFAULT NULL,
  PRIMARY KEY (`weather_date`,`lat`,`lon`),
  KEY `ix_HOURLY_WEATHER_lon` (`lon`),
  KEY `ix_HOURLY_WEATHER_lat` (`lat`),
  KEY `ix_HOURLY_WEATHER_weather_date` (`weather_date`)
);

CREATE TABLE IF NOT EXISTS `WEATHER`.`WEATHER_STATS` (
  `weather_date` date NOT NULL,
  `lat` decimal(10,5) NOT NULL,
  `lon` decimal(10,5) NOT NULL,
  `daily_avg_temp` decimal(10,5) DEFAULT NULL,
  `daily_min_temp` decimal(10,5) DEFAULT NULL,
  `daily_max_temp` decimal(10,5) DEFAULT NULL,
  `monthly_max_temp` decimal(10,5) DEFAULT NULL,
  PRIMARY KEY (`weather_date`,`lat`,`lon`),
  KEY `ix_WEATHER_DAILY_STATS_weather_date` (`weather_date`),
  KEY `ix_WEATHER_DAILY_STATS_lat` (`lat`),
  KEY `ix_WEATHER_DAILY_STATS_lon` (`lon`)
);