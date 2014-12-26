#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Fetch temperature from OpenWeatherMap.org API
Calculating degree days
Plotting
"""

from pandas_degreedays import calculate_dd, inter_lin_nan, plot_temp
from openweathermap_requests import OpenWeatherMapRequests
import click
import datetime

def temp_from_openweathermap(api_key, lon, lat, range, column):
    cache_name = 'cache-openweathermap'
    ow = OpenWeatherMapRequests(api_key=api_key, cache_name=cache_name, expire_after=None) # no expiration for history

    stations = ow.find_stations_near(lon=lon, lat=lat, cnt=1)
    logging.info("\n%s" % stations)
    station_id = stations.iloc[0]['station.id']

    data = ow.get_historic_weather(station_id, start_date, end_date)
    logging.info("\n%s" % data)

    ts_temp = data[column] # get serie from DataFrame

    return(ts_temp)

@click.option('--api_key', default='', help=u"API Key for Wunderground")
@click.option('--lon', default=0.34189, help=u"Longitude")
@click.option('--lat', default=46.5798114, help=u"Latitude")
@click.option('--range', default='', help=u"Date range (YYYYMMDD:YYYYMMDD) or date (YYYYMMDD) or '' (current weather)")
@click.option('--column', default='main.temp.ma', help=u"Temperature column")
def main(api_key, lon, lat, range, column):
    if range=='':
        end_date = datetime.datetime.utcnow()
        start_date = end_date - datetime.timedelta(days=365*2)
    else:
        range = range.split(':')
        range = map(pd.to_datetime, range)
        if len(range)==1:
            raise(NotImplementedError)
        start_date = range[0]
        end_date = range[1]

    ts_temp = temp_from_openweathermap(api_key, lon, lat, range, column)

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
