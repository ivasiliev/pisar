from datetime import date
import datetime

from openpyxl.styles import Font
from openpyxl.workbook import Workbook

from utils.utility_prototype import UtilityPrototype


class UtilityBirthday(UtilityPrototype):
	def __init__(self, data_model):
		super().__init__(data_model)
		if "current_date" not in data_model:
			current_date = date.today()
		else:
			current_date = data_model["current_date"]
		self.current_date = current_date
		self.in_days = 30
		print(f"Расчёт дней рождения в ближайшие {self.in_days} дней от даты {self.current_date}")

	def get_name(self):
		return "Дни рождения"

	def get_name_for_file(self):
		return f"{self.get_name()}.xlsx"

	def render(self):
		pers_storage = self.get_pers_storage()
		all_persons = pers_storage.get_all_persons(0, 10)
		persons = []
		for pers in all_persons:
			nd = datetime.date(self.current_date.year, pers.dob.month, pers.dob.day)
			diff = nd - self.current_date
			if 0 < diff.days <= self.in_days:
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

		ws["A1"] = "ФИО"
		ws["B1"] = "День рождения"
		# c3 = ws["C1"] = "Личный номер"
		# c3.font = f_bold

		ws.column_dimensions["A"].width = 60
		ws.column_dimensions["B"].width = 30

		num_row = 2
		for pers in persons:
			ws.cell(row=num_row, column=1, value=pers.full_name)
			ws.cell(row=num_row, column=2, value=f"{pers.dob.day}.{pers.dob.month}")
			# ws.cell(row=num_row, column=3, value=pers.unique)
			num_row = num_row + 1

		self.save_workbook(wb)

		super().render()
