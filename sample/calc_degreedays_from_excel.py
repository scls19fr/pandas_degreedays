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
    df_temp = pd.read_excel(filename)
    df_temp = df_temp.set_index(col_dt)
    ts_temp = df_temp[col_temp] # get serie from DataFrame

    ts_temp = inter_lin_nan(ts_temp, '1H') # interpolates linearly NaN

    print(ts_temp) # display serie (time serie of temperature values)
    #print(ts_temp.dtypes)
    #print(ts_temp.index)

    # calculates and display degree days
    df_degreedays = calculate_dd(ts_temp, method=method, typ=typ, Tref=tref, group=group)
    #df_degreedays = calculate_dd(ts_temp, method='pro', typ='heating', Tref=18.0, group='monthly')
    #df_degreedays = calculate_dd(ts_temp, method='pro', typ='heating', Tref=18.0, group='yearly')
    #df_degreedays = calculate_dd(ts_temp, method='pro', typ='heating', Tref=18.0, group='yearly10')
    #df_degreedays = calculate_dd(ts_temp, method='pro', typ='heating', Tref=18.0, group=lambda dt: yearly_month(dt, 10))
    print(df_degreedays)

    #df_degreedays['DD_7'] = pd.rolling_mean(df_degreedays['DD'], 7)

    plot_temp(ts_temp, df_degreedays)
    plt.show()

if __name__ == "__main__":
    main()
