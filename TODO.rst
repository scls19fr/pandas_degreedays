pandas\_degreedays (ToDo list)
==============================

cumsum by year, by month - see group-by
breakdown ?


from pandas_degreedays.provider import WeatherHistory
w = WeatherHistory('OpenWeatherMap', cache=..., ....)
df = w.get(place, start_date, stop_date)