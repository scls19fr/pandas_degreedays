#pandas_degreedays

Pandas Degree Days (`pandas_degreedays`) is a Python package to calculate
[degree days](http://en.wikipedia.org/wiki/Degree_day).

You must provide a [Pandas Series](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.html) with temperature values.

Let's call `ts_temp` this Serie which look like:

    datetime
    2014-03-20 23:00:00    11
    2014-03-20 23:30:00    11
    2014-03-21 00:00:00    11
    2014-03-21 00:30:00    11
    2014-03-21 01:00:00    11
    2014-03-21 01:30:00    11
    ...
    2014-11-01 20:00:00    12
    2014-11-01 20:30:00    12
    2014-11-01 21:00:00    12
    2014-11-01 21:30:00    12
    2014-11-01 22:00:00    12
    2014-11-01 22:30:00    12
    Name: temp, Length: 10757

You can get a time serie with temperature in `sample` folder and read it using:

    import pandas as pd
    filename = 'temperature_sample.xls'
    df_temp = pd.read_excel(filename)
    df_temp = df_temp.set_index('datetime')
    ts_temp = df_temp['temp']

We can calculate degree days using:

    from pandas_degreedays import calculate_dd
    df_degreedays = calculate_dd(ts_temp, method='pro', typ='heating', Tref=18.0)

It outputs a [Pandas DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html) 
with degree days like:

                Tmin  Tmax   Tavg  Tref         DD      DD_cum
    2014-03-22   7.0  11.0   9.00    18   9.000000    9.000000
    2014-03-23   3.0  12.0   7.50    18  10.500000   19.500000
    2014-03-24   0.0  10.0   5.00    18  13.000000   32.500000
    2014-03-25   6.0  10.0   8.00    18  10.000000   42.500000
    2014-03-26   5.0  12.0   8.50    18   9.500000   52.000000
    2014-03-27   2.0   8.0   5.00    18  13.000000   65.000000
    ...          ...   ...    ...   ...        ...         ...
    2014-10-26   5.0  17.0  11.00    18   7.000000  653.547663
    2014-10-27   9.0  22.0  15.50    18   3.336923  656.884586
    2014-10-28   7.5  20.0  13.75    18   4.544400  661.428986
    2014-10-29   8.0  19.0  13.50    18   4.618182  666.047168
    2014-10-30  12.0  22.0  17.00    18   1.992000  668.039168
    2014-10-31  11.0  24.0  17.50    18   2.143077  670.182245

    [224 rows x 6 columns]

![figure](https://github.com/scls19fr/pandas_degreedays/blob/master/sample/figure.png)

## About Pandas
[**pandas**](http://pandas.pydata.org/) is a Python package providing fast, flexible, and expressive data
structures designed to make working with "relational" or "labeled" data both
easy and intuitive.
It's a very convenient library to work with time series.

## Links
* Source code and issue tracking can be found at [GitHub](https://github.com/scls19fr/pandas_degreedays).
