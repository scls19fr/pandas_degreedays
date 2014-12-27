#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Calculating Degree days

Tref= reference temperature (18° usually),
Tn = minimum temperature,
Tx= maximum temperature

A Degree Day (DD) is calculated from extreme weather temperatures of the place and the D-day:
* Tn : minimum temperature of D-day measured at 2 meters above ground level (under shelter)
between D-1 (previous day) 6PM to D-day 6PM (UTC).
* Tx : maximum temperature of D-day measured at 2 meters above ground level (under shelter)
between D-day 6AM to D+1 (next day) à 6AM (UTC).
* Tref : reference temperature threshold chosen.
* Mean = (Tn + Tx) / 2 : Average temperature of the day

Ref: http://climatheque.meteo.fr/Docs/DJC-methode.pdf

"""

import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from .version import __author__, __copyright__, __credits__, \
    __license__, __version__, __maintainer__, __email__, __status__, __url__

# Meteo
def hdd_meteo(Tn, Tx, Tref=18):
    """
    Returns Heating Degree Days (meteo method)

    >>> hdd_meteo(10, 20, 18)
    3

    >>> hdd_meteo(10, 30, 18)
    0
    """
    Tavg = (Tn + Tx) / 2
    if Tref<=Tavg:
        return(0)
    else: # Tref>Tavg
        return(Tref-Tavg)

def cdd_meteo(Tn, Tx, Tref=18):
    """
    Returns Cooling Degree Days (meteo method)

    >>> cdd_meteo(10, 20, 18)
    0

    >>> cdd_meteo(10, 30, 18)
    2
    """
    Tavg = (Tn + Tx) / 2
    if Tref>=Tavg:
        return(0)
    else: # Tref<Tavg
        return(Tavg-Tref)

# Degree Days - standard method (energy professionals method)
def hdd(Tn, Tx, Tref=18):
    """
    Returns Heating Degree Days (energy professionals method)

    >>> hdd(5, 15, 18)
    8

    >>> hdd(20, 30, 18)
    0

    >>> hdd(10, 20, 18)
    3.328
    """
    Tavg = (Tn + Tx) / 2
    if Tref>Tx:
        return(Tref-Tavg)
    elif Tref<=Tn:
        return(0)
    else: # Tn<Tref and Tref<=Tx:
        return((Tref-Tn)*(0.08+0.42*(Tref-Tn)/(Tx-Tn)))

def cdd(Tn, Tx, Tref=18):
    """
    Returns Cooling Degree Days (energy professionals method)

    >>> cdd(5, 15, 18)
    0

    >>> cdd(20, 30, 18)
    7

    >>> cdd(10, 20, 18)
    0.32799999999999996
    """
    Tavg = (Tn + Tx) / 2
    if Tref>Tx:
        return(0)
    elif Tref<=Tn:
        return(Tavg-Tref)
    else: # Tn<Tref and Tref<=Tx
        return((Tx-Tref)*(0.08+0.42*(Tx-Tref)/(Tx-Tn)))


def degreedays_date(dt):
    """
    Returns date from a datetime

    >>> dt = datetime.datetime(year=2014, month=11, day=1, hour=12, minute=0)
    >>> degreedays_date_Tn(dt)
    datetime.date(2014, 11, 1)
    """
    return(dt.date())


def degreedays_date_Tn(dt): # Tn = Tmin
    """
    Returns date from a datetime for Tmin

    Before 6PM
    >>> dt = datetime.datetime(year=2014, month=11, day=1, hour=12, minute=0)
    >>> degreedays_date_Tn(dt)
    datetime.date(2014, 11, 1)

    After 6PM (next day)
    >>> dt = datetime.datetime(year=2014, month=11, day=1, hour=19, minute=0)
    >>> degreedays_date_Tn(dt)
    datetime.date(2014, 11, 2)
    """
    if dt.hour<18:
        return(dt.date())
    else:
        dt2 = dt + datetime.timedelta(days=1) # after 6PM next day returned as date
        return(dt2.date())

def degreedays_date_Tx(dt): # Tx = Tmax
    """
    Returns date from a datetime for Tmax

    Avant 6h (jour précédent)
    >>> dt = datetime.datetime(year=2014, month=11, day=2, hour=5, minute=0)
    >>> degreedays_date_Tx(dt)
    datetime.date(2014, 11, 1)

    Après 6h
    >>> dt = datetime.datetime(year=2014, month=11, day=1, hour=7, minute=0)
    >>> degreedays_date_Tx(dt)
    datetime.date(2014, 11, 1)

    """
    if dt.hour<6:
        dt2 = dt - datetime.timedelta(days=1) # before 6PM previous day is returned
        return(dt2.date())
    else:
        return(dt.date())

def inter_lin_nan(ts, rule):
    """
    Re-sampling using rule (eg '1H')
    interpolates linearly NaN
    of time series ts
    """
    ts = ts.resample(rule)
    mask = np.isnan(ts)
    # interpolling missing values
    ts[mask] = np.interp(np.flatnonzero(mask), np.flatnonzero(~mask), ts[~mask])
    return(ts)

def calc_dates_currentday(ts):
    """
    Calculating dates from current day

    Returns a dataframe with datetime as index
    a column with temperature values
    two columns for dates to calculate degree days
        D_MAX for maximum temperature = current day
        D_MIN for minimum temperature = current day
    """
    df_temp = pd.DataFrame(data=ts, index=ts.index)
    df_temp["D_MAX"] = df_temp.index.map(degreedays_date) # calculating date
    df_temp["D_MIN"] = df_temp.index.map(degreedays_date) # calculating date
    return(df_temp)

def calc_dates_6hours(ts):
    """
    Calculating dates for the determination of Tmax and Tmin

    Returns a dataframe with datetime as index
    a column with temperature values
    two columns for dates to calculate degree days
        D_MAX for maximum temperature
        D_MIN for minimum temperature
    """
    df_temp = pd.DataFrame(data=ts, index=ts.index)
    df_temp["D_MAX"] = df_temp.index.map(degreedays_date_Tx) # calculating date for Tmax
    df_temp["D_MIN"] = df_temp.index.map(degreedays_date_Tn) # calculating date for Tmin
    return(df_temp)

def yearly_month(dt, month=10):
    """
    Returns year given a datetime and a month as start
    """
    if dt.month>=month:
        return(dt.year)
    else:
        return(dt.year-1)

def yearly(dt):
    """
    Returns year given a datetime
    """
    return(dt.year)

def monthly(dt):
    """
    Returns (year, month)
    """
    return(dt.year, dt.month)

def weekly(dt):
    """
    Returns (year, week_number)
    """
    return(dt.isocalendar()[0:2])

def calculate_dd(ts_temp, method='pro', typ='heating', Tref=18.0, group='yearly'):
    """
    Calculating degree days from time series with temperature values: ts_temp
    method: 'meteo' or 'pro'
    typ: 'heating' or 'cooling'

    Returns a dataframe with date (day) as index
    columns:
        Tmin
        Tmax
        Tref
        Tavg
        DD
        DD_cum
    """

    #assert(isinstance(ts_temp, pd.Series))

    lst_allowed_degreedays_method = ['meteo', 'pro']
    lst_allowed_degreedays_typ = ['heating', 'cooling']

    d_func = {
        'meteo': {
            'heating': hdd_meteo, # cooling degree day - meteo method
            'cooling': cdd_meteo, # heating degree day - meteo method
        },
        'pro': {
            'heating': hdd, # heating degree day - pro method
            'cooling': cdd, # cooling degree day - pro method
        }
    }

    if method in lst_allowed_degreedays_method:
        df_temp = calc_dates_6hours(ts_temp)

        ts_temp_min = df_temp.groupby('D_MIN')[ts_temp.name].min()
        ts_temp_min.name = "Tmin"
        ts_temp_min.index.name = "DATE"
        ts_temp_min = ts_temp_min[:-1] # remove last day (next day for Tmin)
        #ts_temp_min[-1] = np.nan

        ts_temp_max= df_temp.groupby('D_MAX')[ts_temp.name].max()
        ts_temp_max.name = "Tmax"
        ts_temp_max.index.name = ts_temp_min.index.name
        ts_temp_max = ts_temp_max[1:] # remove first day (previous day for Tmax)
        #ts_temp_max[1] = np.nan

        df_degreedays = pd.concat([ts_temp_min, ts_temp_max], axis=1)

        df_degreedays = df_degreedays[1:-1] # remove last day (next day for Tmin)
        # remove first day (previous day for Tmax)

        # daily average temperature
        #df_degreedays['Tavg'] = ts_temp.resample('1D', how='mean')

        # daily average temperature between Tmin and Tmax
        df_degreedays['Tavg'] = (df_degreedays['Tmin'] + df_degreedays['Tmax']) / 2
        df_degreedays['Tref'] = Tref # reference temperature

        f_calc_dju = d_func[method][typ] # choosing function to apply
        # inside dictionary according computing method (meteo or pro)
        # and type of calculation of degree days (heating or cooling)

        df_degreedays['DD'] = df_degreedays.apply(lambda row: f_calc_dju(row['Tmin'], row['Tmax'], Tref), axis=1) # applying function to dataframe

        df_degreedays.index = pd.to_datetime(df_degreedays.index)
        df_degreedays.index.name = 'date'
        #print(df_degreedays.index)
        #print(type(df_degreedays.index[0]))
        df_degreedays = df_degreedays.resample('1D')

        #df_degreedays['year'] = df_degreedays.index.map(lambda x: x.year)
        #df_degreedays['year_month'] = df_degreedays.index.map(lambda x: (x.year, x.month)) # (year, month)
        #df_degreedays['year_week'] = df_degreedays.index.map(lambda x: x.isocalendar()[0:2]) # (year, week_number)
        
        #d_groups = {
        #    'yearly': 'year',
        #    'monthly': 'year_month',
        #    'weekly': 'year_week',
        #}

        d_groups = {
            'yearly': yearly,
            'yearly10': lambda dt: yearly_month(dt, 10),
            'monthly': monthly,
            'weekly': weekly,
        }

        try:
            f_group_col = d_groups[group]
            group_col = 'group_col'
            df_degreedays[group_col] = df_degreedays.index.map(f_group_col)
            df_degreedays['DD_cum'] = df_degreedays.groupby(group_col)['DD'].cumsum()
            
        except:
            df_degreedays['DD_cum'] = df_degreedays['DD'].cumsum()

        return(df_degreedays)

    else:
        raise(NotImplementedError("Methode %s non disponible" % method))

def plot_temp(ts_temp, df_degreedays):
    """
    plot temperature (time serie), temperature (min/max)
    degree days and cumulated degree days
    ts_temp is an hourly time serie
    df_degreedays is a daily dataframe
    """
    fig, axes = plt.subplots(nrows=4, ncols=1)
    ts_temp.resample('1H').plot(ax=axes[0])
    df_degreedays[['Tmin', 'Tavg', 'Tmax', 'Tref']].plot(ax=axes[1], legend=False)
    df_degreedays['DD'].plot(ax=axes[2])
    #df_degreedays[['DJU', 'DJU_7']].plot(ax=axes[2])
    df_degreedays['DD_cum'].plot(ax=axes[3])

if __name__ == "__main__":
    # To run doctest (unit tests inside docstrings)
    # run python filename.py -v
    import doctest
    doctest.testmod()