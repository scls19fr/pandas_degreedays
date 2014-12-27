#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Reading XLS file with temperature (sample)
Calculating degree days
Plotting
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

from pandas_degreedays import calculate_dd, inter_lin_nan, plot_temp

def main():
    basepath = os.path.dirname(__file__)
    filename = os.path.join(basepath, 'temperature_sample.xls')
    df_temp = pd.read_excel(filename)
    df_temp = df_temp.set_index('datetime')

    ts_temp = df_temp['temp'] # get serie from DataFrame

    ts_temp = inter_lin_nan(ts_temp, '1H') # interpolates linearly NaN

    print(ts_temp) # display serie (time serie of temperature values)
    #print(ts_temp.dtypes)
    #print(ts_temp.index)

    # calculates and display degree days
    df_degreedays = calculate_dd(ts_temp, method='pro', typ='heating', Tref=18.0, group='yearly')
    #df_degreedays = calculate_dd(ts_temp, method='pro', typ='heating', Tref=18.0, group='yearly10')
    #df_degreedays = calculate_dd(ts_temp, method='pro', typ='heating', Tref=18.0, group=lambda dt: yearly_month(dt, 8))
    print(df_degreedays)

    #df_degreedays['DD_7'] = pd.rolling_mean(df_degreedays['DD'], 7)

    plot_temp(ts_temp, df_degreedays)
    plt.show()

if __name__ == "__main__":
    main()
