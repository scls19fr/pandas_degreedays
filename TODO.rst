pandas\_degreedays (ToDo list)
==============================

cumsum by year, by month - see group-by
breakdown ?

::

    from pandas_degreedays.provider import WeatherHistory
    w = WeatherHistory('OpenWeatherMap', cache=..., ....)
    df = w.get(place, start_date, stop_date)

see projet 
https://github.com/scls19fr/openweathermap_requests
to fetch historical weather data

::

    pip install openweathermap_requests


::

    $ python openweathermap_requests.py --range 20120101:20141215 -lon ... -lat ...


Read Excel file

::

    df = pd.read_excel("openweathermap_0.34189_46.5798114_20120101_20141215.xls", skiprows=1)
    df = df.set_index('dt')
    idx = df.index
    s_idx = pd.Series(idx)
    diff_idx = (s_idx-s_idx.shift(1))[1:]
    s_sampling_period = diff_idx.value_counts()
    sampling_period = s_sampling_period[0] # most prevalent sampling period

    see also data_quality.py

