import tkinter as tk
import os
from tkinter import filedialog
from tkinter import messagebox as msgbox
from tkinter.ttk import Checkbutton

import code_parser as parser
import reporter as rp

def make_check():
    make_report_button.configure(state="disable")
    file = filedialog.askopenfile(initialdir="/", title="Select image", filetypes=(("CPP files", "*.cpp"), (
    "HPP files", "*.hpp"), ("All files", "*.*")))
    if file is None:
        return
    else:
        file_path = file.name
        global file_name
        file_name = os.path.basename(file_path).split('.')[0]
    try:
        file = open(file_path, "r")
        text_file = file.read()
        parser.get_string(text_file, 1)
        global errors
        if unused_var.get() == 1:
            errors[UNUSED_TYPE] = parser.find_unused_names()
        if incorrect_n_var.get() == 1:
            errors[INC_N_TYPE] = parser.find_incorrect_names()
        if incorrect_d_var.get() == 1:
            errors[INC_D_TYPES] = parser.find_incorrect_directives()
        if brackets_var.get() == 1:
            errors[UNP_BRACKETS_TYPE] = parser.check_brackets_pairing()
        make_report_button.configure(state="normal")
    except AttributeError:
        print("File error")


def make_report():
    reporter.create_book()
    reporter.insert_value("A1", value=f"Отчет по файлу исходного кода {file_name}")
    reporter.insert_value("A2", value="Тип")
    reporter.insert_value("B2", value="Содержание")
    reporter.insert_value("C2", value="Статус")
    global errors
    item_num = 3
    for item in errors[UNUSED_TYPE]:
        reporter.insert_value("A" + str(item_num), value=UNUSED_TYPE)
        reporter.insert_value("B" + str(item_num), value=item)
        reporter.insert_value("C" + str(item_num), value="Обнаружена")
        item_num += 1
    for item in errors[INC_N_TYPE]:
        reporter.insert_value("A" + str(item_num), value=INC_N_TYPE)
        reporter.insert_value("B" + str(item_num), value=item)
        reporter.insert_value("C" + str(item_num), value="Обнаружена")
        item_num += 1
    for item in errors[INC_D_TYPES]:
        reporter.insert_value("A" + str(item_num), value=INC_D_TYPES)
        reporter.insert_value("B" + str(item_num), value=item)
        reporter.insert_value("C" + str(item_num), value="Обнаружена")
        item_num += 1
    for item in errors[UNP_BRACKETS_TYPE]:
        reporter.insert_value("A" + str(item_num), value=UNP_BRACKETS_TYPE)
        reporter.insert_value("B" + str(item_num), value=item)
        reporter.insert_value("C" + str(item_num), value="Обнаружена")
        item_num += 1
    reporter.save_book(file_name, f"D:\\")
    msgbox.showinfo("Информация", "Отчёт создан")

#глобальные переменные
file_name = ""
UNUSED_TYPE = "unused_name"
INC_N_TYPE = "incorrect_name"
INC_D_TYPES = "incorrect_directive"
UNP_BRACKETS_TYPE = "unparentness_brackets"

#объявление переменных для парсера
parser = parser.CodeParser()
errors = {UNUSED_TYPE: [], INC_N_TYPE: [], INC_D_TYPES: [], UNP_BRACKETS_TYPE: []}
#объявление переменных для создателя отчетов
reporter = rp.ExcelReporter()

#создание окна
window = tk.Tk()
window.title("Code Parser")
width = 260
height = 200
x_pos = int(window.winfo_screenwidth() / 2 - width / 2)
y_pos = int(window.winfo_screenheight() / 2 - height / 2)
window.resizable(0, 0)
window.geometry(f"{width}x{height}+{x_pos}+{y_pos}")

unused_var = tk.IntVar()
incorrect_n_var = tk.IntVar()
incorrect_d_var = tk.IntVar()
brackets_var = tk.IntVar()

checkbox_unused_names = Checkbutton(window, text="Неиспользуемые имена", padding=4, variable=unused_var, onvalue=1, offvalue=0)
checkbox_incorrect_names = Checkbutton(window, text="Некорректные имена", padding=4, variable=incorrect_n_var, onvalue=1, offvalue=0)
checkbox_incorrect_directives = Checkbutton(window, text="Некорректные директивы", padding=4, variable=incorrect_d_var, onvalue=1, offvalue=0)
checkbox_brackets_check = Checkbutton(window, text="Парность скобок", padding=4, variable=brackets_var, onvalue=1, offvalue=0)

choose_type_text_label = tk.Label(window, text="Выберите типы проверок", padx=4, pady=4)
choose_file_text_label = tk.Label(window, text="Выберите файл исходного кода", padx=4, pady=4)
make_report_button = tk.Button(window, text="Отчёт", command=make_report, padx=4, pady=4, state="disabled")
browse_button = tk.Button(window, text="Обзор...", command=make_check, padx=4, pady=4)

choose_type_text_label.grid(column=0, row=0, sticky="W")
checkbox_brackets_check.grid(column=0, row=1, sticky="W")
checkbox_unused_names.grid(column=0, row=2, sticky="W")
checkbox_incorrect_names.grid(column=0, row=3, sticky="W")
checkbox_incorrect_directives.grid(column=0, row=4, sticky="W")
choose_file_text_label.grid(column=0, row=5)
browse_button.grid(column=1, row=5)
make_report_button.grid(columnspan=2, row=6)

window.mainloop()








