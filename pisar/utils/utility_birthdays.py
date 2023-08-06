from datetime import date
import datetime

from openpyxl.styles import Font
from openpyxl.workbook import Workbook

from classes.personnel_storage import EXCEL_DOCUMENT_SR
from helpers.text_helper import get_month_string, get_date_str
from utils.utility_prototype import UtilityPrototype


class UtilityBirthday(UtilityPrototype):
	def __init__(self, data_model):
		super().__init__(data_model)
		if "current_date" not in data_model:
			current_date = date.today()
		else:
			current_date = data_model["current_date"]
		self.current_date = current_date
		m = self.current_date.month
		y = self.current_date.year
		m_left = m - 1
		y_left = y
		if m_left < 1:
			m_left = 12
			y_left = y - 1
		m_right = m + 2
		y_right = y
		if m_right > 12:
			m_right = 1
			y_right = y + 1
		self.date_left = datetime.date(y_left, m_left, 1)
		self.date_right = datetime.date(y_right, m_right, 1)

		print(f"Расчёт дней рождения на период [{get_date_str(self.date_left)} - {get_date_str(self.date_right)}]")

	def get_name(self):
		return "Дни рождения"

	def get_name_for_file(self):
		return f"{self.get_name()}-{self.get_date_string(self.current_date)}.xlsx"

	def render(self):
		pers_storage = self.get_pers_storage()
		rl = None
		if self.get_row_limit() > 0:
			rl = self.get_row_limit()
		all_persons = pers_storage.get_all_persons(EXCEL_DOCUMENT_SR, rl)
		persons = []
		for pers in all_persons:
			if pers.dob is None:
				continue
			nd = datetime.date(self.current_date.year, pers.dob.month, pers.dob.day)
			if self.date_left <= nd <= self.date_right:
				diff = nd - self.current_date
				pers.age = diff.days
				persons.append(pers)

		print(f"Найдено {len(persons)} человек(а)")
		persons.sort(key=lambda x: x.age, reverse=False)

		wb = Workbook()
		ws = wb.active
		ws.title = "Дни рождения"
		f_bold = Font(bold=True)
		ws["A1"].font = f_bold
		ws["B1"].font = f_bold
		ws["C1"].font = f_bold
		ws["D1"].font = f_bold

		ws["A1"] = "ФИО"
		ws["B1"] = "День рождения"
		ws["C1"] = "Исполняется"
		ws["D1"] = "Должность"

		ws.column_dimensions["A"].width = 60
		ws.column_dimensions["B"].width = 30
		ws.column_dimensions["C"].width = 20
		ws.column_dimensions["D"].width = 30

		current_year = date.today().year

		num_row = 2
		for pers in persons:
			age = current_year - pers.dob.year
			ws.cell(row=num_row, column=1, value=pers.full_name)
			ws.cell(row=num_row, column=2, value=f"{pers.dob.day} {get_month_string(pers.dob.month)}")
			ws.cell(row=num_row, column=3, value=age)
			ws.cell(row=num_row, column=4, value=pers.position)
			num_row = num_row + 1

		self.save_workbook(wb)

		super().render()
