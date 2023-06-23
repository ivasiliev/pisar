import openpyxl

from classes.person import Person
from helpers.file_helper import get_file_size_info
from helpers.performance_helper import PerformanceHelper


class PersonnelStorage:
	# full_path = xlsx file
	def __init__(self, full_path):
		self.storage = None
		# TODO to app_settings?
		self.personnel_excel_sheet_name = "ШДС"
		self.personnel_list_full_path = full_path
		# рота
		self.COLUMN_COMPANY = -1
		# взвод
		self.COLUMN_PLATOON = -1
		# отделение
		self.COLUMN_SQUAD = -1
		# воинская должность
		self.COLUMN_POSITION = -1
		# звание
		self.COLUMN_RANK = -1
		# ФИО
		self.COLUMN_FULL_NAME = -1
		# дата рождения (dob = date of birth)
		self.COLUMN_DOB = -1
		self.is_valid = True

		workbook = openpyxl.load_workbook(self.personnel_list_full_path)
		print("--- Сведения о файле Excel ---")
		print(f"Размер: {get_file_size_info(self.personnel_list_full_path)}")
		print(f"Всего листов: {len(workbook.sheetnames)}")
		print("Список листов:")
		print(workbook.sheetnames)
		print("------------------------------")
		if self.personnel_excel_sheet_name not in workbook.sheetnames:
			print(
				f"В Excel-документе отсутствует лист '{self.personnel_excel_sheet_name}'. Штатное расписание должно располагаться на этом листе.")
			self.is_valid = False
		else:
			sh = workbook[self.personnel_excel_sheet_name]

			# analyze headers
			for row in sh.iter_rows(min_row=1, min_col=1, max_row=1, max_col=20):
				for cell in row:
					col_str = str(cell.value).casefold()
					if col_str == "рота".casefold():
						self.COLUMN_COMPANY = cell.col_idx
					else:
						if col_str == "взвод".casefold():
							self.COLUMN_PLATOON = cell.col_idx
						else:
							if col_str == "отделение".casefold():
								self.COLUMN_SQUAD = cell.col_idx
							else:
								if col_str == "воинская должность".casefold():
									self.COLUMN_POSITION = cell.col_idx
								else:
									if col_str == "воинское звание фактическое".casefold():
										self.COLUMN_RANK = cell.col_idx
									else:
										if col_str == "фио".casefold():
											self.COLUMN_FULL_NAME = cell.col_idx
										else:
											if col_str == "дата рождения".casefold():
												self.COLUMN_DOB = cell.col_idx

			# validation
			if self.COLUMN_COMPANY == -1:
				print("Столбец 'РОТА' не найден")
			if self.COLUMN_PLATOON == -1:
				print("Столбец 'ВЗВОД' не найден")
			if self.COLUMN_SQUAD == -1:
				print("Столбец 'ОТДЕЛЕНИЕ' не найден")
			if self.COLUMN_POSITION == -1:
				print("Столбец 'ВОИНСКАЯ ДОЛЖНОСТЬ' не найден")
			if self.COLUMN_RANK == -1:
				print("Столбец 'ВОИНСКОЕ ЗВАНИЕ ФАКТИЧЕСКОЕ' не найден")
			if self.COLUMN_FULL_NAME == -1:
				print("Столбец 'ФИО' не найден")
			if self.COLUMN_DOB == -1:
				print("Столбец 'ДАТА РОЖДЕНИЯ' не найден")

			self.is_valid = self.COLUMN_COMPANY > -1 and self.COLUMN_PLATOON > -1 and self.COLUMN_SQUAD > 0 and self.COLUMN_POSITION > -1 and self.COLUMN_RANK > -1 and self.COLUMN_FULL_NAME > -1 and self.COLUMN_DOB > -1

	# print("Штатное расписание прочитано:") print(f"'РОТА'={self.COLUMN_COMPANY}; 'ВЗВОД'={self.COLUMN_PLATOON};
	# 'ОТДЕЛЕНИЕ'={self.COLUMN_SQUAD}; " f"'ВОИНСКАЯ ДОЛЖНОСТЬ'={self.COLUMN_POSITION}; 'ВОИНСКОЕ ЗВАНИЕ
	# ФАКТИЧЕСКОЕ'={self.COLUMN_RANK}; 'ФИО'={self.COLUMN_FULL_NAME}; 'ДАТА РОЖДЕНИЯ'={self.COLUMN_DOB};")

	def find_person_by_id(self, id_person):
		id_person_str = str(id_person)
		# this id must be at the first column of the personnel list Excel file
		workbook = openpyxl.load_workbook(self.personnel_list_full_path)
		sh = workbook[self.personnel_excel_sheet_name]
		indexes = [self.COLUMN_COMPANY, self.COLUMN_PLATOON, self.COLUMN_SQUAD, self.COLUMN_POSITION, self.COLUMN_RANK,
		           self.COLUMN_FULL_NAME, self.COLUMN_DOB]

		performance = PerformanceHelper()
		performance.start()
		person = None
		iteration_count_to_find_person = 0
		count_for_report = 50
		print("Поиск военнослужащего в ШР. Пожалуйста, подождите...")
		for row in sh.iter_rows(min_row=2, min_col=1, max_row=2001, max_col=max(indexes) + 1):
			person_row = None
			for cell in row:
				iteration_count_to_find_person = iteration_count_to_find_person + 1
				if cell.value is None:
					break
				if str(cell.value) == id_person_str:
					person_row = row
					break
				if iteration_count_to_find_person % count_for_report == 0:
					print(f"Обработано {iteration_count_to_find_person} строк...")
				break
			if person_row is not None:
				person = Person()
				person.company = self.find_value_in_row_by_index(person_row, self.COLUMN_COMPANY)
				person.platoon = self.find_value_in_row_by_index(person_row, self.COLUMN_PLATOON)
				person.squad = self.find_value_in_row_by_index(person_row, self.COLUMN_SQUAD)
				person.position = self.find_value_in_row_by_index(person_row, self.COLUMN_POSITION)
				person.rank = self.find_value_in_row_by_index(person_row, self.COLUMN_RANK)
				person.full_name = self.find_value_in_row_by_index(person_row, self.COLUMN_FULL_NAME)
				person.set_dob(self.find_value_in_row_by_index(person_row, self.COLUMN_DOB))

				# normalization of a soldier name
				if person.full_name is not None:
					person.full_name = person.full_name.title()

				person.position = person.position.lower()
				person.rank = person.rank.lower()

				break

		print(f"Количество итераций для поиска военнослужащего: {iteration_count_to_find_person}")
		performance.stop_and_print()
		return person

	def find_value_in_row_by_index(self, row, index):
		for cell in row:
			if cell.col_idx == index:
				return cell.value
		return None



