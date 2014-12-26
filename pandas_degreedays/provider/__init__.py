#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from pandas_degreedays.provider.openweathermap import TemperatureProviderOpenWeatherMap

class TemperatureProviderFactory(object):
    def __init__(self):
        raise(NotImplementedError)

class TemperatureProviderBase(object):
    def __init__(self, *args, **kwargs):
        raise(NotImplementedError)


class TemperatureProviderOpenWeatherMap(TemperatureProviderBase):
    pass

TEMPERATURE_PROVIDER_FACTORY = TemperatureProviderFactory()

def TemperatureProvider(name, *args, **kwargs):
    raise(NotImplementedError)
