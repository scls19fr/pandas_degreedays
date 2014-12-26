#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from pandas_degreedays.provider.openweathermap import TemperatureProviderOpenWeatherMap

from pandas_degreedays.provider.openweathermap import TemperatureProviderOpenWeatherMap
#from openweathermap_requests import OpenWeatherMapRequests
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

TEMPERATURE_PROVIDER_FACTORY = TemperatureProviderFactory()

def TemperatureProvider(name, *args, **kwargs):
    return(TEMPERATURE_PROVIDER_FACTORY.factory(name, *args, **kwargs))
