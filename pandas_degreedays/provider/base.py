#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    pandas_degreedays.provider.base
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implements TemperatureProviderBase base class for TemperatureProviders
"""

class TemperatureProviderBase(object):
    def __init__(self, *args, **kwargs):
        self.init(*args, **kwargs)
