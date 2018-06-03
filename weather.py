# import requests
#
# from model import WeatherRepository, WeatherModel
#
# headers = {
#     "X-Yandex-API-Key": "124645b4-0ab1-4ba0-893d-c70d7b767451"
# }
#
# URL = 'https://api.weather.yandex.ru/v1/forecast?lat=0&lon=0&lang=ru_RU&hours=false&limit=7'
#
# response = requests.get(URL, headers=headers)
#
# # print(response.json())
#
# for day in response.json().get('forecasts'):
#     date = day.get('date_ts')
#     temp = day.get('parts').get('day_short').get('temp')
#
#     WeatherRepository().save_day(WeatherModel(date, temp))
#
#
# def parse():
#
#     # if date_arg is None or temp is None:
#     #     raise ValueError('empty arg')
#     #
#     # prepare_date = date.fromtimestamp(date_arg)
#     #
#     # if prepare_date.year == 1970:
#     #     raise ValueError('date is incorrect')
#
#
#     pass
from presenter import Presenter

Presenter().load_data()