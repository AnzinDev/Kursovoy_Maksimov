import tkinter as tk
from tkinter.ttk import Checkbutton


class WindowManager:
    unused_var = None
    incorrect_n_var = None
    incorrect_d_var = None
    brackets_var = None
    checkbox_unused_names = None
    checkbox_incorrect_names = None
    checkbox_incorrect_directives = None
    checkbox_brackets_check = None
    choose_type_text_label = None
    choose_file_text_label = None
    make_report_button = None
    browse_button = None

    def __init__(self, window_name, window_width, window_height):
        self.__name = window_name
        self.__width = window_width
        self.__height = window_height
        self.__x_pos = 0
        self.__y_pos = 0
        self.__window = None

    def create_window(self, make_report, make_check, on_close): #тут лучше переписать на именнованные параметры, чтобы передавать любое количество
        self.__window = tk.Tk()  # в этом методе создаются все элементы окна
        self.__window.title(self.__name)
        self.__window.resizable(0, 0)
        self.__x_pos = int(self.__window.winfo_screenwidth() / 2 - self.__width / 2)
        self.__y_pos = int(self.__window.winfo_screenheight() / 2 - self.__height / 2)
        self.__window.geometry(f"{self.__width}x{self.__height}+{self.__x_pos}+{self.__y_pos}")
        self.__window.protocol("WM_DELETE_WINDOW", on_close)

        self.unused_var = tk.IntVar()
        self.incorrect_n_var = tk.IntVar()
        self.incorrect_d_var = tk.IntVar()
        self.brackets_var = tk.IntVar()

        self.checkbox_unused_names = Checkbutton(self.__window, text="Неиспользуемые имена", padding=4, variable=self.unused_var,
                                            onvalue=1,
                                            offvalue=0)
        self.checkbox_incorrect_names = Checkbutton(self.__window, text="Некорректные имена", padding=4, variable=self.incorrect_n_var,
                                               onvalue=1, offvalue=0)
        self.checkbox_incorrect_directives = Checkbutton(self.__window, text="Некорректные директивы", padding=4,
                                                    variable=self.incorrect_d_var,
                                                    onvalue=1, offvalue=0)
        self.checkbox_brackets_check = Checkbutton(self.__window, text="Парность скобок", padding=4, variable=self.brackets_var,
                                              onvalue=1,
                                              offvalue=0)

        self.choose_type_text_label = tk.Label(self.__window, text="Выберите типы проверок", padx=4, pady=4)
        self.choose_file_text_label = tk.Label(self.__window, text="Выберите файл исходного кода", padx=4, pady=4)
        self.make_report_button = tk.Button(self.__window, text="Отчёт", command=make_report, padx=4, pady=4, state="disabled")
        self.browse_button = tk.Button(self.__window, text="Обзор...", command=make_check, padx=4, pady=4)

        self.choose_type_text_label.grid(column=0, row=0, sticky="W")
        self.checkbox_brackets_check.grid(column=0, row=1, sticky="W")
        self.checkbox_unused_names.grid(column=0, row=2, sticky="W")
        self.checkbox_incorrect_names.grid(column=0, row=3, sticky="W")
        self.checkbox_incorrect_directives.grid(column=0, row=4, sticky="W")
        self.choose_file_text_label.grid(column=0, row=5)
        self.browse_button.grid(column=1, row=5)
        self.make_report_button.grid(columnspan=2, row=6)

    def mainloop(self):
        self.__window.mainloop()  # главный цикл приложения

    def close_window(self):
        self.__window.destroy()  # закрытие окна

