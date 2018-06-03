from presenter import Presenter


class View():

    def __init__(self):
        self.presenter = Presenter()

    def cli(self):
        choice = 0
        while choice != 3:
            choice = self.__endless_menu(self.__main_menu)
            if choice == 1:
                self.presenter.load_data()
                print('обновлено')

            elif choice == 2:
                day = self.__endless_menu(self.__compare_menu)

                while not (1 <= day <= 7):
                    print('неверный параметр')
                    day = self.__endless_menu(self.__compare_menu)

                result = self.presenter.compare_two_date(day)
                if result is None:
                    print('ошибка')
                    continue

                print('разница сегодняшней погоды и погоды через {} дня составляет {}%'.format(day, result))

    def __endless_menu(self, menu):

        choice = menu()

        while not choice.isdigit():
            if not choice.isdigit():
                print('неверный параметр')

            choice = menu()

        return int(choice)

    def __main_menu(self):
        return input("""
        1 - обновить базу
        2 - указать день
        3 - выход
        """)

    def __compare_menu(self):
        return input("""
        за какой день нужно узнать? (1-7)
        """)


View().cli()
