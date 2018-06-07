from datetime import date

import requests
from peewee import Model, SqliteDatabase, DateField, IntegerField, DoesNotExist


class BaseModel(Model):
    class Meta:
        database = SqliteDatabase('weather_short.sqlite')


class WeatherDatabaseModel(BaseModel):
    date, temp = DateField(), IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_table(WeatherDatabaseModel)


TOKEN = "124645b4-0ab1-4ba0-893d-c70d7b767451"
URL = 'https://api.weather.yandex.ru/v1/forecast?lat=55.7437256&lon=37.6271067&lang=ru_RU&hours=false&limit=7'
headers = {
    "X-Yandex-API-Key": TOKEN
}


def parse():
    for day in requests.get(URL, headers=headers).json().get('forecasts'):
        date, temp = day.get('date'), day.get('parts').get('day_short').get('temp')
        try:
            if WeatherDatabaseModel().get(WeatherDatabaseModel.date == date): WeatherDatabaseModel().update(
                temp=temp).where(WeatherDatabaseModel.date == date)
        except DoesNotExist:
            WeatherDatabaseModel(date=date, temp=temp).save()


def calculate(day):
    try:
        need = WeatherDatabaseModel.get(
            WeatherDatabaseModel.date == date.today().replace(day=date.today().day + day)).temp

        now = WeatherDatabaseModel.get(WeatherDatabaseModel.date ==
                                       date.today()
                                       ).temp
    except DoesNotExist:
        print("error")
        return

    if now == 0:
        now = 1
    if need < now:
        result = ((need - now) / now) * 100
    else:
        result = ((now - need) / now) * 100
    result = int(result)
    if result < 0:
        result = result * -1
    return result


try:
    print('разница сегодняшней погоды и погоды через несколько дней составляет {}%'.format(calculate(int(input("от 1 до 6 ")))))
except ValueError:
    print("error")
