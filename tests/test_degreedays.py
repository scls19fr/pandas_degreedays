#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime

import pandas_degreedays
from pandas_degreedays import *

def test_version():
    """Test version"""
    isinstance(pandas_degreedays.__version__, basestring)

def test_degreedays_date_Tmin_before_6PM():
    """Tmin: BEFORE 6PM"""
    dt = datetime.datetime(year=2014, month=11, day=1, hour=12, minute=0)
    d = degreedays_date_Tn(dt)
    d2 = dt.date()
    assert(d == d2)

def test_degreedays_date_Tmin_after_6PM():
    """Tmin: AFTER 6PM"""
    dt = datetime.datetime(year=2014, month=11, day=1, hour=18, minute=0)
    d = degreedays_date_Tn(dt)
    dt2 = dt + datetime.timedelta(days=1)
    d2 = dt2.date()
    assert(d == d2)

def test_degreedays_date_Tmax_before_6AM():
    """Tmin: BEFORE 6AM"""
    dt = datetime.datetime(year=2014, month=11, day=1, hour=5, minute=0)
    d = degreedays_date_Tx(dt)
    dt2 = dt - datetime.timedelta(days=1)
    d2 = dt2.date()
    assert(d == d2)

def test_degreedays_date_Tmin_after_6AM():
    """Tmin: AFTER 6AM"""
    dt = datetime.datetime(year=2014, month=11, day=1, hour=7, minute=0)
    d = degreedays_date_Tx(dt)
    d2 = dt.date()
    assert(d == d2)

def test_degreedays():
    """Calculating degree days"""
    assert(hdd_meteo(10, 20, 18)==3)
    assert(hdd_meteo(10, 30, 18)==0)
    assert(cdd_meteo(10, 20, 18)==0)
    assert(cdd_meteo(10, 30, 18)==2)
    assert(hdd(5, 15, 18)==8)
    assert(hdd(20, 30, 18)==0)
    assert(hdd(10, 20, 18)==3.328)
    assert(cdd(5, 15, 18)==0)
    assert(cdd(20, 30, 18)==7)
    assert(cdd(10, 20, 18)==0.32799999999999996)

def test_sample():
    """Reading XLS file with temperature as time serie
    and calculate degree days"""
    filename = os.path.join('sample', 'temperature_sample.xls')
    df_temp = pd.read_excel(filename)
    df_temp = df_temp.set_index('datetime')
    ts_temp = df_temp['temp']
    df_degreedays = calculate_dd(ts_temp=ts_temp, method='pro', typ='heating', Tref=18.0)
    isinstance(df_degreedays, pd.DataFrame)
