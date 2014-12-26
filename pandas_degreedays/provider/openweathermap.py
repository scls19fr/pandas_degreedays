#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pandas_degreedays.provider.base import TemperatureProviderBase
from openweathermap_requests import OpenWeatherMapRequests
import logging

class TemperatureProviderOpenWeatherMap(TemperatureProviderBase):
    def init(self, *args, **kwargs):
        try:
            self.api_key = kwargs['api_key']
        except:
            self.api_key = None

    def get_from_coordinates(self, lon, lat, start_date, end_date, column='main.temp.ma'):
        cache_name = 'cache-openweathermap'
        ow = OpenWeatherMapRequests(api_key=self.api_key, cache_name=cache_name, expire_after=None) # no expiration for history

        stations = ow.find_stations_near(lon=lon, lat=lat, cnt=1)
        logging.info("\n%s" % stations)
        station_id = stations.iloc[0]['station.id']

        data = ow.get_historic_weather(station_id, start_date, end_date)
        logging.info("\n%s" % data)

        ts_temp = data[column] # get serie from DataFrame

        return(ts_temp)
