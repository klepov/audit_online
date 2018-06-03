from datetime import date

from model import WeatherRepository


class Presenter:

    def __init__(self):
        self.repository = WeatherRepository()
        self.view = None

    def __load_new_data(self):
        return self.repository.load_data()

    def __save_loaded_data(self, data):
        self.repository.save_days(data)

    def load_data(self):
        days = self.__load_new_data()

        if days is None:
            raise ValueError('data was not uploaded')

        self.__save_loaded_data(days)


    def compare_two_date(self, day):
        date_now = date.today()

        new_date = date_now.replace(day=date_now.day + day)
        need_day_from_db = self.repository.get_day_by_date(new_date)
        today_day = self.repository.get_day_by_date(date_now)

        if need_day_from_db is None or today_day is None:
            return

        return self.__calculate(today_day, need_day_from_db)

    def __calculate(self, today, need):
        today_temp, need_temp = today.temp, need.temp

        coef = need_temp*100/today_temp

        if coef > 100:
            coef = 100
        elif coef < 0:
            coef = 0

        return 100-int(coef)