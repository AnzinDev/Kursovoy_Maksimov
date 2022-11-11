import psycopg2 as sql
from psycopg2 import Error


class PostgreInterface:

    current_prog_key = None
    current_prog_name = None

    def __init__(self, database, user, password, host, port):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.con = None

    def connection(self):  # функция установки соединения с бд
        try:
            self.con = sql.connect(
                database=self.database,  # db name
                user=self.user,  # username
                password=self.password,  # user pass
                host=self.host,  # ip (foreign/local)
                port=self.port  # port
            )
        except (Exception, Error) as error:
            print("Connection failed, error: ", error)
        finally:
            if self.con:
                return self.con

    def __insert_data(self, query):  # attr - список атрибутов, values - строка значений
        con = self.connection()
        cur = con.cursor()
        cur.execute(  # выполенение запроса к бд
            query
        )
        con.commit()  # коммитит изменения в б
        cur.close()  # закрывает общение с бд

    # (prog_name, error_type, error_stat, error_importance, error_content)
    def insert_into_main(self, val):  # инсерт в мейн
        query = "INSERT INTO public.main (prog_name, error_type, error_stat, error_importance, error_content) " \
                "VALUES(" + val + ")"
        self.__insert_data(query)

    def insert_into_prog_name(self, name):  # инсерт в прог нейм
        query = "INSERT INTO public.prog_name (name) VALUES('" + name + "')"
        self.__insert_data(query)

    def insert_into_history(self, val):  # инсерт в хистори. подавать строку вида "name, 8, 5, 0, 8, time"
        query = "INSERT INTO public.history " \
                "(prog_name, unused_name, incorrect_name, incorrect_directive, unpaired_brackets, time) " \
                "VALUES(" + val + ")"
        self.__insert_data(query)  # подумать над названиями атрибутов

    def __select_data(self, query):  # возвращает иннер селект из мейна
        con = self.connection()
        cur = con.cursor()
        cur.execute(
            query
        )
        rows = cur.fetchall()  # возвращает список кортежей
        return rows

    def select_unique_from_main(self, prog_name):  # возварщает данные по определенной программе
        prog_name = "'" + prog_name + "'"  # такой мув нужен, потому что в бд только одинарыне кавычки принимаются
        query = 'SELECT u_id, T.name, type, stat, value, error_content ' \
                'FROM public.main AS P ' \
                'INNER JOIN prog_name AS T ON  P.prog_name = T."key" ' \
                'INNER JOIN error_type ON P.error_type= error_type."key" ' \
                'INNER JOIN error_stat ON P.error_stat = error_stat."key" ' \
                'INNER JOIN error_importance ON P.error_importance = error_importance."key" ' \
                'WHERE t.name = ' + prog_name + ' '
        return self.__select_data(query)

    def select_all_from_main(self):  # возварщает данные по всем программам
        # селект из main сгруппированный по названию программы
        query = 'SELECT u_id, T.name, type, stat, value, error_content ' \
                'FROM public.main AS P ' \
                'INNER JOIN prog_name AS T ON  P.prog_name = T."key" ' \
                'INNER JOIN error_type ON P.error_type = error_type."key" ' \
                'INNER JOIN error_stat ON P.error_stat = error_stat."key" ' \
                'INNER JOIN error_importance ON P.error_importance = error_importance."key" ' \
                'ORDER BY name'
        return self.__select_data(query)

    def get_program_key(self, prog_name):  # возвращает из прог нейм номер программы по ее названию
        query = "SELECT \"key\" " \
                "FROM public.prog_name " \
                "WHERE \"name\" = '" + prog_name + "'"
        return self.__select_data(query)  # тут мб как то обработать, чтобы возвращало сразу число, а не кортеж

    def select_from_history(self,
                            prog_name):  # возвращает данные по определенной программе подается в виде айди (цифра)
        query = 'SELECT history.key, prog_name.name, unused_name, incorrect_name, incorrect_directive, unpaired_brackets, time ' \
                'FROM history ' \
                'INNER JOIN prog_name ON history.prog_name = prog_name."key" ' \
                'WHERE prog_name = ' + str(prog_name) + ' ' \
                                                   'ORDER BY time ASC'
        return self.__select_data(query)

    def select_all(self, table_name):  # пассивный метод (не используется)
        con = self.connection()
        cur = con.cursor()

        cur.execute(
            "SELECT  FROM " + table_name
        )

        # возвращает список кортежей
        rows = cur.fetchall()
        for row in rows:  # идем по списку
            for i in range(len(rows[0])):  # идем по кортежу в списке
                print(row[i], end=' ')
            print()

        con.close()

    def delete_data(self, prog_name):  # удаляем данные из мейн, а после из прог нейм
        con = self.connection()
        cur = con.cursor()
        cur.execute(
            "DELETE FROM main WHERE " + prog_name + " = " + prog_name + ""
                                                                        "DELETE FROM prog_name WHERE " + prog_name + " = " + prog_name + ""
        )
        con.commit()
        con.close()


# метод делит можно сделать на случай. если исправлены все оишбки по программе
# удаляем все записи сначала из мейна, а потом из прог нейм


if __name__ == '__main__':

    SQL = PostgreInterface('test', 'postgres', '1', '127.0.0.1', '5432')
    # SQL.insert_into_history('1, 2, 5, 5, 2, 1333')
    # SQL.insert_into_main("5, 1, 2, 1, '{6}'")
    rows = SQL.get_program_key('barsuk.cpp')
    print(rows)


    # rows = SQL.select_unique_from_main("beawer.cpp")
    # rows = SQL.select_all_from_main()

    def show():
        print("-" * 80)
        for row in rows:  # идем по кортежу
            for i in range(len(rows[0])):  # идем по списку в кортеже
                val = row[i]
                if type(val) == str:
                    print('{:<16}'.format(val.strip()), end='')
                elif val == 'None':
                    print('None', end='')
                else:
                    print('{:<8}'.format(val), end='')
            print()
        print("-" * 80)
        print("Selection done successfully")

# show()
# select_all('error_num')
# select_all('error_stat')
# select_all('error_importance')
# select_all('prog_name')
# select_all('main')
# select_all_inner()


