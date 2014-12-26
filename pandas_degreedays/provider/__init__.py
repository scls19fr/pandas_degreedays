#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from pandas_degreedays.provider.openweathermap import TemperatureProviderOpenWeatherMap

from openweathermap_requests import OpenWeatherMapRequests
import logging

class TemperatureProviderFactory(object):
    """
    TemperatureProviderFactory

    Factory of TemperatureProvider

    Only ONE factory need to be defined : TEMPERATURE_PROVIDER_FACTORY

    Additional TemperatureProvider can be add using:

    TEMPERATURE_PROVIDER_FACTORY.add('temperatureprovidername', TemperatureProviderClassName)
    """
    def __init__(self):
        self._d_factory = {}

        # === OpenWeatherMap ===
        self.add('OpenWeatherMap', TemperatureProviderOpenWeatherMap)

    def add(self, name, cls):
        self._d_factory[name.lower()] = cls

    def factory(self, name, *args, **kwargs):
        try:
            return(self._d_factory[name.lower()](*args, **kwargs))
        except:
            logging.error(traceback.format_exc())
            raise(NotImplementedError("TemperatureProvider '%s' not implemented - should be in %s" % (name, self._d_factory.keys())))

class TemperatureProviderBase(object):
    def __init__(self, *args, **kwargs):
        self.init(*args, **kwargs)

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

TEMPERATURE_PROVIDER_FACTORY = TemperatureProviderFactory()

def TemperatureProvider(name, *args, **kwargs):
    return(TEMPERATURE_PROVIDER_FACTORY.factory(name, *args, **kwargs))
