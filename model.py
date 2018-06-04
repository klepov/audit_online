import requests
from peewee import SqliteDatabase, Model, DateField, IntegerField, DoesNotExist


class BaseModel(Model):
    class Meta:
        database = SqliteDatabase('weather.sqlite')


class WeatherModel:
    date = None
    temp = None

    def __init__(self, date=None, temp=None) -> None:
        self.date = date
        self.temp = temp

    @staticmethod
    def transform_db_to_model(weather):
        return WeatherModel(date=weather.date, temp=weather.temp)


class WeatherDatabaseModel(BaseModel):
    date = DateField()
    temp = IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_table(WeatherDatabaseModel)

    def save_day(self, weather):
        self.__save_day(weather)

    def get_day_by_date(self, by_date):
        return self.__get_by_date(by_date)

    def __save_day(self, weather):
        maybe_db = self.__select_from_db(weather.date)

        if maybe_db:
            return WeatherDatabaseModel.update(temp=weather.temp) \
                .where(WeatherDatabaseModel.date == weather.date)

        return WeatherDatabaseModel(date=weather.date, temp=weather.temp).save()

    def __get_by_date(self, by_date):
        req = self.__select_from_db(by_date)
        if req is None:
            return
        return WeatherModel.transform_db_to_model(req)

    @staticmethod
    def __select_from_db(by_date):
        try:
            return WeatherDatabaseModel.get(WeatherDatabaseModel.date == by_date)
        except DoesNotExist:
            return None


class WeatherNetwork:

    def load_data(self):
        response = self.__send_request()
        if response is None:
            raise ValueError('response is empty')
        return self.__parse(response)

    def __parse(self, response):
        days = []
        for day in response.json().get('forecasts'):
            date = day.get('date')
            temp = day.get('parts').get('day_short').get('temp')
            days.append(WeatherModel(date, temp))
        return days

    def __send_request(self):

        TOKEN = "124645b4-0ab1-4ba0-893d-c70d7b767451"
        URL = 'https://api.weather.yandex.ru/v1/forecast?lat=55.7437256&lon=37.6271067&lang=ru_RU&hours=false&limit=7'
        headers = {
            "X-Yandex-API-Key": TOKEN
        }

        response = requests.get(URL, headers=headers)

        if response.status_code == 200:
            return response


class WeatherRepository:

    def __init__(self):
        self.db = WeatherDatabaseModel()
        self.network = WeatherNetwork()

    def save_days(self, days):
        for day in days:
            self.save_day(day)

    def save_day(self, weather):
        self.db.save_day(weather)

    def get_day_by_date(self, p_date):
        return self.db.get_day_by_date(p_date)

    def load_data(self):
        return self.network.load_data()
