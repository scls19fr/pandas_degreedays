#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Fetch temperature from OpenWeatherMap.org API
Calculating degree days
Plotting
"""
import click

from pandas_degreedays import calculate_dd, inter_lin_nan, plot_temp
from pandas_degreedays.provider import TemperatureProvider
import datetime
import os
import logging
import logging.config
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def temp_from_openweathermap(api_key, lon, lat, start_date, end_date, column):
    cache_name = 'cache-openweathermap'
    ow = OpenWeatherMapRequests(api_key=api_key, cache_name=cache_name, expire_after=None) # no expiration for history

    stations = ow.find_stations_near(lon=lon, lat=lat, cnt=1)
    logging.info("\n%s" % stations)
    station_id = stations.iloc[0]['station.id']

    data = ow.get_historic_weather(station_id, start_date, end_date)
    logging.info("\n%s" % data)

    ts_temp = data[column] # get serie from DataFrame

    return(ts_temp)

@click.command()
@click.option('--api_key', default='', help=u"API Key for Wunderground")
@click.option('--lon', default=0.34189, help=u"Longitude")
@click.option('--lat', default=46.5798114, help=u"Latitude")
@click.option('--range', default='', help=u"Date range (YYYYMMDD:YYYYMMDD) or date (YYYYMMDD) or '' (current weather)")
@click.option('--column', default='main.temp.ma', help=u"Temperature column")
def main(api_key, lon, lat, range, column):
    #if api_key=='':
    #    try:
    #        api_key = os.environ[ENV_VAR_API_KEY]
    #    except:
    #        logging.warning("You should get an API key from OpenWeatherMap.org and pass it us using either --api_key or using environment variable %r" % ENV_VAR_API_KEY)
    #        api_key = None

    if range=='':
        dt = datetime.datetime.utcnow()
        #dt = datetime.datetime.fromordinal(dt.toordinal())
        dt = datetime.datetime(year=dt.year, month=dt.month, day=dt.day) # yesterday 00:00
        dt = dt - datetime.timedelta(days=1)
        end_date = dt
        start_date = end_date - datetime.timedelta(days=int(365*2.5))
    else:
        range = range.split(':')
        range = map(pd.to_datetime, range)
        if len(range)==1:
            raise(NotImplementedError)
        start_date = range[0]
        end_date = range[1]

    temp_provider = TemperatureProvider('OpenWeatherMap', api_key=api_key)
    ts_temp = temp_provider.get_from_coordinates(lon, lat, start_date, end_date, column)

    #ts_temp = temp_from_openweathermap(api_key, lon, lat, start_date, end_date, column)

    ts_temp = inter_lin_nan(ts_temp, '1H') # interpolates linearly NaN

    print(ts_temp) # display serie (time serie of temperature values)
    #print(ts_temp.dtypes)
    #print(ts_temp.index)

    # calculates and display degree days
    df_degreedays = calculate_dd(ts_temp, method='pro', typ='heating', Tref=18.0, group='yearly')
    print(df_degreedays)

    #df_degreedays['DD_7'] = pd.rolling_mean(df_degreedays['DD'], 7)

    plot_temp(ts_temp, df_degreedays)
    plt.show()

if __name__ == "__main__":
    basepath = os.path.dirname(__file__)
    logging.config.fileConfig(os.path.join(basepath, "logging.conf"))
    logger = logging.getLogger("simpleExample")
    main()
