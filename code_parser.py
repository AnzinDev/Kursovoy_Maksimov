import re


class CodeParser:
    ROUND_BRACKETS = ["[(]", "[)]"]
    SQUARE_BRACKETS = ["[\[]", "[\]]"]
    FIGURE_BRACKETS = ["[{]", "[}]"]
    ALL_BRACKETS = ["[(|\[|{]", "[)|\]|}]"]
    REMOVE_EXTRA_SYMBOLS = 1

    def __init__(self):
        self.__string = ""

    def load_from_file(self, path,
                       remove_extras=0):  # можно добавить удаление комментариев для снижения возможности ошбиок в закомментированных частях кода
        with open(path, "r") as file_obj:
            extracted = file_obj.read()
            if remove_extras:  # если нужно, то удаляются переносы строк
                extracted = re.sub(r"(?:\n|\r)", " ", extracted)
            self.__string = extracted
            return extracted

    def get_string(self, string, remove_extras=0):
        if remove_extras:  # если нужно, то удаляются переносы строк
            string = re.sub(r"(?:\n|\r)", " ", string)
        self.__string = string

    def check_brackets_pairing(self):  # проверяется просто парность скобок по их количеству, а не правильность их расстановки
        open_brackets = ["[(]", "[\[]", "[{]"]
        close_brackets = ["[)]", "[\]]", "[}]"]
        brackets_type = ["(", "[", "{"]
        report_list = []
        for i in range(len(open_brackets)):
            m1 = re.findall(open_brackets[i], self.__string)
            m2 = re.findall(close_brackets[i], self.__string)
            if not ((m1 is None and m2 is None) or (len(m1) == len(m2))):
                report_list.append(f"\"{brackets_type[i]}\":{abs(len(m1) - len(m2))}")
        return report_list


    def find_unused_names(
            self):  # возвращает список единожды упомянутых в коде переменных, работает только с правильно именованными переменными, поэтому проверку правильности надо произвести заранее
        custom_names = re.findall("(?:class\s*|struct\s*)([a-zA-Z_][a-zA-Z0-9_]*)\s*{",
                                  self.__string)  # нашли имена типов классов и структур, теперь их надо добавить к поиску
        # alias и typedef не учитываются
        str = ""
        for item in custom_names:
            str += item + "\s*|"
        pattern = ("(?:" + str + "auto\s*|short\s*|long\s*|char\s*|int\s*|float\s*|double\s*|bool\s*|)"
                                 "(?:\s*\**\s*)([a-zA-Z_][a-zA-Z0-9_]*)\s*[\[;,=)]")  # паттерн, учитывающий стандартыне типы, типы классов и структур
        names = re.findall(pattern,
                           self.__string)  # здесь найдены все имена переменных в программе, включая имена классов, структур и стандартных имен С++
        names = list(set(names))  # удаление повторов, так как имена у локальных переменных разных блоков кода могут повотряться
        # теперь пробежимся по всему файлу для каждого имени и найдем, сколько раз оно встречалось в коде, по предположению, если имя встретилось единожды, значит было только объявлено и не использовалось, что и требуется найти
        report = []
        for name in names:
            name_count = re.findall("(?:\s+|\()" + name + "(?:\s+|[-=\[;\)+\*/%^|&])", self.__string)
            if len(name_count) == 1:
                report.append(name)
        return report

    def find_incorrect_names(self):
        custom_names = re.findall("(?:class\s*|struct\s*)([a-zA-Z_][a-zA-Z0-9_]*)\s*{", self.__string)
        str = ""
        for item in custom_names:
            str += item + "\s*|"
        pattern = ("(?:" + str + "auto\s*|short\s*|long\s*|char\s*|int\s*|float\s*|double\s*|bool\s*)"
                                 "(?:\s*\**\s*)([^\*\sa-zA-z_\(\{]\w*)\s*")  # паттерн, учитывающий стандартыне типы, типы классов и структур
        names = re.findall(pattern, self.__string)
        return names

    def find_incorrect_directives(self):
        pattern = '(?:#)([a-zA-z0-9(\)\[\]\}\{\+\=\-\#\$\%\,\.\<\>\^\:\;\`\~]*)\s*'
        correct = ['define', 'elif', 'else', 'endif', 'error', 'if', 'ifdef', 'ifndef', 'import', 'include', 'line',
                   'pragma', 'undef', 'using']
        names = re.findall(pattern, self.__string)
        incorrect = []
        for name in names:
            if name not in correct:
                incorrect.append(name)
        return incorrect
