#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import traceback

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
        try:
            from pandas_degreedays.provider.openweathermap import TemperatureProviderOpenWeatherMap
            self.add('OpenWeatherMap', TemperatureProviderOpenWeatherMap)
            self.add('owm', TemperatureProviderOpenWeatherMap)
        except:
            logging.error(traceback.format_exc())

    def add(self, name, cls):
        """
        Adds (register) a TemperatureProvider class using a name
        """
        self._d_factory[name.lower()] = cls

    def factory(self, name, *args, **kwargs):
        """
        Returns a TemperatureProvider (factory) using a name and arguments
        """
        try:
            return(self._d_factory[name.lower()](*args, **kwargs))
        except:
            logging.error(traceback.format_exc())
            raise(NotImplementedError("TemperatureProvider '%s' not implemented - should be in %s" % (name, self._d_factory.keys())))

TEMPERATURE_PROVIDER_FACTORY = TemperatureProviderFactory()

def TemperatureProvider(name, *args, **kwargs):
    """
    Creates a TemperatureProvider to fetch temperature from a number of online sources.

    Currently supports 
        * [OpenWeatherMap.org](http://www.openweathermap.org/) using 

    Parameters
    ----------

    :param name: data source
    :type name: str

        * "OpenWeatherMap" (can also be simply "owm")
    """

    return(TEMPERATURE_PROVIDER_FACTORY.factory(name, *args, **kwargs))
