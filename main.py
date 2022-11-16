import os
from tkinter import filedialog
from tkinter import messagebox as msgbox
import datetime as dt

# импорт пакетов
import code_parser as parser
import reporter as rp
import window as wm
import data_base_interface as dbi


# функции событий оконного приложения
def make_check():
    root.make_report_button.configure(state="disable")  # деактивация кнопки создания отчета
    file = filedialog.askopenfile(initialdir="/", title="Select image", filetypes=(("CPP files", "*.cpp"), (
        "HPP files", "*.hpp"), ("All files", "*.*")))  # файловый диалог
    if file is None:
        return  # если файл не был выбран, выходим из функции
    else:
        file_path = file.name
        global file_name
        file_name = os.path.basename(file_path).split('.')[0]  # сохранение имени текущей программы из имени файла
        try:
            file = open(file_path, "r")  # открытие файла
            text_file = file.read()  # чтение всего содержимого
            parser.get_string(text_file, remove_extras=1)  # задание содержимого файла в парсер
            global errors_type_content
            errors_type_content = {UNUSED_NAME_TYPE: [], INCORRECT_NAME_TYPE: [], INCORRECT_DIRECTIVE_TYPE: [],
                                   UNPAIRED_BRACKETS_TYPE: []}  # очистка словаря с содержимым ошибок
            # просто проверка файла на ошибки зависимо от того, какие проверки выбраны
            if root.unused_var.get() == 1:
                errors_type_content[UNUSED_NAME_TYPE] = parser.find_unused_names()
            if root.incorrect_n_var.get() == 1:
                errors_type_content[INCORRECT_NAME_TYPE] = parser.find_incorrect_names()
            if root.incorrect_d_var.get() == 1:
                errors_type_content[INCORRECT_DIRECTIVE_TYPE] = parser.find_incorrect_directives()
            if root.brackets_var.get() == 1:
                errors_type_content[UNPAIRED_BRACKETS_TYPE] = parser.check_brackets_pairing()
            db.current_prog_name = file_name
            list_of_keys = db.get_program_key(prog_name=file_name)
            if not list_of_keys:
                db.insert_into_prog_name(name=file_name)
                list_of_keys = db.get_program_key(file_name)
            db.current_prog_key = (list_of_keys[0])[0]
            # по логике должно вернуть назначенный ключ новому файлу, либо если он уже был, вернуть существующий

            global error_key_type
            global error_key_state
            global error_key_importance
            # теперь надо перебрать словарь с ошибками
            for error_type in errors_type_content:
                errors = errors_type_content[error_type]
                for error in errors:
                    string_ = f"{db.current_prog_key}, {error_key_type[error_type]}, {error_key_state[UNFIXED]}, {get_importance_of_error_type(error_type)}, \'{error}\'"
                    db.insert_into_main(string_)
            # в чем теперь смысл мейн таблицы, нужно придумать логику обновления статуса найденной ошибки, раз мы решили, что идем до первой ошибки, это сделать будет трудно
            # потому что если перед ней появится еще ошибка при повторной проверке, то как понять, что с прошлой стало, или если поменялось содержимое той же ошибки, запись о старой останется навсегда нерешенной
            # в то же время, для динамики нужно количество ошибок и его изменение, поэтому туда я засовываю число всех ошибок
            # теперь надо сделать запись в таблицу динамики
            current_timestamp = (dt.datetime.now()).timestamp()
            lenghts = {UNUSED_NAME_TYPE: 0, INCORRECT_NAME_TYPE: 0, INCORRECT_DIRECTIVE_TYPE: 0,
                       UNPAIRED_BRACKETS_TYPE: 0}
            for error_type in lenghts:
                lenghts[error_type] = len(errors_type_content[error_type])
            db.insert_into_history(
                f"{db.current_prog_key}, {lenghts[UNUSED_NAME_TYPE]}, {lenghts[INCORRECT_NAME_TYPE]}, {lenghts[INCORRECT_DIRECTIVE_TYPE]}, {lenghts[UNPAIRED_BRACKETS_TYPE]}, {current_timestamp}"
            )  # а тут проходиться по словарю просто добавляя числа длин по его типу

            msgbox.showinfo("Информация",
                            "Проверка выполнена, база данных обновлена")  # сообщение о выполненной проверке

            root.make_report_button.configure(state="normal")  # активация кнопки создания отчета
        except Exception as e:
            print("Error " + e)


def make_report():
    reporter.create_book(file_name)  # создание новой книги
    # нужно обрезать пробелы в конце строк возвращаемых БД
    error_list = db.select_unique_from_main(db.current_prog_name)
    row_num = 3
    for error in error_list:
        reporter.insert_value("A" + str(row_num), value=(error[2]).rstrip())
        reporter.insert_value("B" + str(row_num), value=(error[5]).rstrip())
        reporter.insert_value("C" + str(row_num), value=(error[3]).rstrip())
        reporter.insert_value("D" + str(row_num), value=(error[4]).rstrip())
        row_num += 1

    history_list = db.select_from_history(db.current_prog_key)
    row_num = 3
    for stamp in history_list:
        reporter.insert_value("F" + str(row_num), value=stamp[2])
        reporter.insert_value("G" + str(row_num), value=stamp[3])
        reporter.insert_value("H" + str(row_num), value=stamp[4])
        reporter.insert_value("I" + str(row_num), value=stamp[5])
        timestamp = dt.datetime.fromtimestamp(stamp[6]).strftime("%Y-%m-%dT%H:%M:%S")
        reporter.insert_value("J" + str(row_num), value=timestamp)
        row_num += 1
    max_row = len(history_list) + 2
    reporter.place_linechart(chart_cell=("F" + str(max_row + 1)), min_col=6, max_col=9, min_row=2, max_row=max_row,
                             chart_name="Динамика", x_axis_name="Время", y_axis_name="Кол-во ошибок")

    base_path = filedialog.askdirectory(title="Выбрать папку сохранения", initialdir="\\", mustexist=True)
    reporter.save_book(file_name, base_path)  # сохранение созданного отчета
    msgbox.showinfo("Информация",
                    "Отчёт создан и сохранен на диск\nпо пути \"" + base_path + "\"")  # сообщение о сохранении отчета


def on_close():  # событие закрытия программы, здесь нужно будет отпустить все открытые файлы и соединения и закрыть программу
    print("Program closed")
    root.close_window()


def get_importance_of_error_type(error_type):
    if error_type != UNUSED_NAME_TYPE:
        return error_key_importance[IMPORTANT]
    else:
        return error_key_importance[UNIMPORTANT]


# точка входа в программу
# глобальные переменные

file_name = ""  # имя текущего файла
UNUSED_NAME_TYPE = "unused_name"  # типы ошибок и их названия
INCORRECT_NAME_TYPE = "incorrect_name"
INCORRECT_DIRECTIVE_TYPE = "incorrect_directive"
UNPAIRED_BRACKETS_TYPE = "unparentness_brackets"

FIXED = "fixed"  # статусы ошибок
UNFIXED = "unfixed"
PENDING = "pending"

IMPORTANT = "important"  # важности ошибок
UNIMPORTANT = "not important"

# объявление переменных для парсера
parser = parser.CodeParser()  # создание экземпляра класса парсера
errors_type_content = {UNUSED_NAME_TYPE: [], INCORRECT_NAME_TYPE: [], INCORRECT_DIRECTIVE_TYPE: [],
                       UNPAIRED_BRACKETS_TYPE: []}  # словарь ошбиок {тип ошибки : список с ошбиками}
error_key_type = {UNUSED_NAME_TYPE: 1, INCORRECT_NAME_TYPE: 2, INCORRECT_DIRECTIVE_TYPE: 3,
                  UNPAIRED_BRACKETS_TYPE: 4}  # словарь соответствия таблице типов ошибок
error_key_state = {FIXED: 1, UNFIXED: 2, PENDING: 3}  # словарь соответствия таблице статусов ошибок
error_key_importance = {IMPORTANT: 1, UNIMPORTANT: 2}  # словарь соответствия таблице важности ошибок
# объявление переменных для создателя отчетов
reporter = rp.ExcelReporter()  # создание экземпляра класса создателя отчетов

# объявление переменных для работы с БД
db = dbi.PostgreInterface('parser', 'postgres', '1', '127.0.0.1', '5432')

# экземпляр класса окна
root = wm.WindowManager(window_name="Code Parser", window_width=260, window_height=200)  # объявление окна
root.create_window(make_check=make_check, make_report=make_report,
                   on_close=on_close)  # создание оконного приложения и всех его элементов
root.mainloop()  # главный цикл оконного приложения
