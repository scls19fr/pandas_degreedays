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

from pandas_degreedays import calculate_dd

def main():
    basepath = os.path.dirname(__file__)
    filename = os.path.join(basepath, 'temperature_sample.xls')
    df_temp = pd.read_excel(filename)
    df_temp = df_temp.set_index('datetime')

    ts_temp = df_temp['temp']

    print(ts_temp)
    #print(ts_temp.dtypes)
    #print(ts_temp.index)

    df_degreedays = calculate_dd(ts_temp, method='pro', typ='heating', Tref=18.0)
    print(df_degreedays)

    #df_degreedays['DD_7'] = pd.rolling_mean(df_degreedays['DD'], 7)

    fig, axes = plt.subplots(nrows=4, ncols=1)
    ts_temp.resample('1H').plot(ax=axes[0])
    df_degreedays[['Tmin', 'Tavg', 'Tmax', 'Tref']].plot(ax=axes[1], legend=False)
    df_degreedays['DD'].plot(ax=axes[2])
    #df_degreedays[['DJU', 'DJU_7']].plot(ax=axes[2])
    df_degreedays['DD_cum'].plot(ax=axes[3])
    plt.show()

if __name__ == "__main__":
    main()
