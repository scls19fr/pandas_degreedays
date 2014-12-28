#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Reading XLS file with temperature (sample)
Calculating degree days
Plotting
"""

import click

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pandas_degreedays import calculate_dd, inter_lin_nan, plot_temp
from pandas_degreedays import yearly_month

@click.command()
@click.option('--filename', default='temperature_sample.xls', help=u"Filename of input file")
@click.option('--col_dt', default='datetime', help=u"Name of column for datetime (index)")
@click.option('--col_temp', default='temp', help=u"Name of column for temp")
@click.option('--method', default='pro', help=u"Degree days method ('pro' or 'meteo')")
@click.option('--typ', default='heating', help=u"Degree days type ('heating' or 'cooling')")
@click.option('--tref', default=18.0, help=u"Reference temperature to calculate degree days")
@click.option('--group', default='yearly', help=u"Grouping period ('yearly', 'yearly10', 'monthly')")
def main(filename, col_dt, col_temp, method, typ, tref, group):
    basepath = os.path.dirname(__file__)
    filename = os.path.join(basepath, filename)
    #filename='sample/temperature_sample.xls'
    df_temp = pd.read_excel(filename)
    df_temp = df_temp.set_index(col_dt)
    ts_temp = df_temp[col_temp] # get serie from DataFrame
    #df_temp = df_temp.set_index('datetime')
    #ts_temp = df_temp['temp']

    ts_temp = inter_lin_nan(ts_temp, '1H') # interpolates linearly NaN

    print(ts_temp) # display serie (time serie of temperature values)
    #print(ts_temp.dtypes)
    #print(ts_temp.index)

    # calculates and display degree days
    df_degreedays = calculate_dd(ts_temp, method=method, typ=typ, Tref=tref, group=group)
    #df_degreedays = calculate_dd(ts_temp, method='pro', typ='heating', Tref=18.0, group='monthly')
    #df_degreedays = calculate_dd(ts_temp, method='pro', typ='heating', Tref=18.0, group='yearly')
    month = 10
    df_degreedays = calculate_dd(ts_temp, method='pro', typ='heating', Tref=18.0, group='yearly10')
    #df_degreedays = calculate_dd(ts_temp, method='pro', typ='heating', Tref=18.0, group=lambda dt: yearly_month(dt, month))
    #print(df_degreedays)

    #df_degreedays['DD_7'] = pd.rolling_mean(df_degreedays['DD'], 7)

    plot_temp(ts_temp, df_degreedays)
    plt.show()

    #df_degreedays = df_degreedays.reset_index()
    groupname = 'yearly10'
    #df_degreedays['duration'] = (df_degreedays['date'] - df_degreedays[groupname].map(lambda year: datetime.datetime(year, month, 1))).map(lambda td: td.astype('timedelta64[D]')/np.timedelta64(1, 'D'))
    df_degreedays_yearly = pd.pivot_table(df_degreedays, values='DD_cum', index='duration', columns=groupname)


if __name__ == "__main__":
    main()
