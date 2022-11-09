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

            list_of_keys = db.get_program_key(prog_name=file_name)
            if not list_of_keys:
                db.insert_into_prog_name(name=file_name)
                list_of_keys = db.get_program_key(file_name)
            db.current_prog_key = (list_of_keys[0])[
                0]  # по логике должно вернуть назначенный ключ новому файлу, либо если он уже был, вернуть существующий

            # теперь надо перебрать словарь с ошибками
            for error_type in errors_type_content:
                errors = errors_type_content[error_type]
                for error in errors:
                    db.insert_into_main(
                        f"{db.current_prog_key}, {error_key_type[error_type]}, {error_key_state[error_type]}, {error_key_importance[error_type]}, '{error}'")

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
            # добавление данных об ошибках есть
            root.make_report_button.configure(state="normal")  # активация кнопки создания отчета
        except AttributeError:
            print("File error")


def make_report():
    reporter.create_book(file_name=file_name)  # создание новой книги

    # запрос к БД по данным для текущей проги

    global errors_type_content  # тут потом будет умное, пока что не будет
    item_num = 3
    for item in errors_type_content[UNUSED_NAME_TYPE]:
        reporter.insert_value("A" + str(item_num), value=UNUSED_NAME_TYPE)
        reporter.insert_value("B" + str(item_num), value=item)
        reporter.insert_value("C" + str(item_num), value="Обнаружена")
        item_num += 1
    for item in errors_type_content[INCORRECT_NAME_TYPE]:
        reporter.insert_value("A" + str(item_num), value=INCORRECT_NAME_TYPE)
        reporter.insert_value("B" + str(item_num), value=item)
        reporter.insert_value("C" + str(item_num), value="Обнаружена")
        item_num += 1
    for item in errors_type_content[INCORRECT_DIRECTIVE_TYPE]:
        reporter.insert_value("A" + str(item_num), value=INCORRECT_DIRECTIVE_TYPE)
        reporter.insert_value("B" + str(item_num), value=item)
        reporter.insert_value("C" + str(item_num), value="Обнаружена")
        item_num += 1
    for item in errors_type_content[UNPAIRED_BRACKETS_TYPE]:
        reporter.insert_value("A" + str(item_num), value=UNPAIRED_BRACKETS_TYPE)
        reporter.insert_value("B" + str(item_num), value=item)
        reporter.insert_value("C" + str(item_num), value="Обнаружена")
        item_num += 1
    reporter.save_book(file_name, f"D:\\")  # сохранение созданного отчета
    msgbox.showinfo("Информация", "Отчёт создан")  # сообщение о сохранении отчета


def on_close():  # событие закрытия программы, здесь нужно будет отпустить все открытые файлы и соединения и закрыть программу
    print("Program closed")
    root.close_window()


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
NOT_IMPORTANT = "not important"

# объявление переменных для парсера
parser = parser.CodeParser()  # создание экземпляра класса парсера
errors_type_content = {UNUSED_NAME_TYPE: [], INCORRECT_NAME_TYPE: [], INCORRECT_DIRECTIVE_TYPE: [],
                       UNPAIRED_BRACKETS_TYPE: []}  # словарь ошбиок {тип ошибки : список с ошбиками}
error_key_type = {UNUSED_NAME_TYPE: 1, INCORRECT_NAME_TYPE: 2, INCORRECT_DIRECTIVE_TYPE: 3,
                  UNPAIRED_BRACKETS_TYPE: 4}  # словарь соответствия таблице типов ошибок
error_key_state = {FIXED: 1, UNFIXED: 2, PENDING: 3}  # словарь соответствия таблице статусов ошибок
error_key_importance = {IMPORTANT: 1, NOT_IMPORTANT: 2}  # словарь соответствия таблице важности ошибок
# объявление переменных для создателя отчетов
reporter = rp.ExcelReporter()  # создание экземпляра класса создателя отчетов

# объявление переменных для работы с БД
db = dbi.PostgreInterface('test', 'postgres', '1', '127.0.0.1', '5432')

# экземпляр класса окна
root = wm.WindowManager(window_name="Code Parser", window_width=260, window_height=200)  # объявление окна
root.create_window(make_check=make_check, make_report=make_report,
                   on_close=on_close)  # создание оконного приложения и всех его элементов
root.mainloop()  # главный цикл оконного приложения
