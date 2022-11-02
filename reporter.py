import openpyxl as ex
import datetime as dt


class ExcelReporter:
    report_book = None
    DEFAULT_SHEET_NAME = "Отчёт"

    def create_book(self):
        self.report_book = ex.Workbook()
        self.report_book.create_sheet(self.DEFAULT_SHEET_NAME, index=0)
        self.report_book.remove(self.report_book["Sheet"])

    def insert_value(self, cell_name, value, sheet_name=None):
        if sheet_name is None:
            sn = self.DEFAULT_SHEET_NAME
        else:
            sn = sheet_name
        sheet = self.report_book[sn]
        cell = sheet[cell_name]
        cell.value = value

    def save_book(self, prg_name, base_path=""):
        now = dt.datetime.now()
        curr_data = now.strftime("%d-%m-%Y %H.%M.%S")
        self.report_book.save(f"{base_path}Отчёт {prg_name} {curr_data}.xlsx")
