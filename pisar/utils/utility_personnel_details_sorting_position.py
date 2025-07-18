from datetime import date

from openpyxl.workbook import Workbook

from classes.personnel_storage import EXCEL_DOCUMENT_SR, EXCEL_DOCUMENT_LS
from helpers.log_helper import log
from utils.utility_prototype import UtilityPrototype


class UtilityPersonnelDetailsSortingPosition(UtilityPrototype):
	def __init__(self, data_model):
		super().__init__(data_model)

	def get_name(self):
		return "Сортировка ЛС по порядку должностей"

	def get_name_for_file(self):
		current_date = date.today()
		return f"{self.get_name()}-{self.get_date_string(current_date)}.xlsx"

	def render(self):
		pers_storage = self.get_pers_storage()
		pers_storage.read_positions()
		persons_ls = pers_storage.get_all_persons(EXCEL_DOCUMENT_LS)
		ls_hash, ls_empty_unique = self.prepare_hash_list(persons_ls)

		# reading LS document
		all_ls_rows = pers_storage.read_excel_file(EXCEL_DOCUMENT_LS)
		log(f"Количество в ЛС: {len(persons_ls)}; Всего строк в ЛС: {len(all_ls_rows)};")
		log(f"Количество людей с пустыми номерами должностей в ЛС: {len(ls_empty_unique)};")
		new_ls_rows = []
		# header of LS document
		row_header = pers_storage.read_excel_header(EXCEL_DOCUMENT_LS)

		# rows rearranged according SR (they exist in SR)
		used_ls_indexes = []

		# create new LS document based on number of positions
		# we don't know the total number of positions in advance, so, just go for as many of them as possible
		number_position = 1
		while number_position in ls_hash:
			index_in_ls = ls_hash[number_position]
			row_in_ls = all_ls_rows[index_in_ls]
			new_ls_rows.append(row_in_ls)
			used_ls_indexes.append(index_in_ls)
			number_position = number_position + 1

		log(f"Сведено ЛС > ШР {len(used_ls_indexes)} человек(а)")

		new_ls_rows.insert(0, row_header)
		list_of_rows = self.convert_rows_to_lists(new_ls_rows)

		# save re-ordered rows in a new Excel file
		wb = Workbook()
		ws = wb.active
		ws.title = "ЛС после сортировки"
		for row in list_of_rows:
			ws.append(row)

		self.save_workbook(wb)
		super().render()

	def convert_rows_to_lists(self, rows):
		all_rows = []
		for row in rows:
			row_list = []
			for cell in row:
				row_list.append(cell.value)
			all_rows.append(row_list)
		return all_rows

	def prepare_hash_list(self, pers_list):
		index = -1
		result = {}
		empty_unique = []
		for p in pers_list:
			index = index + 1
			# hash is id_sr , means number
			hsh = p.id_sr
			if hsh is None:
				log(f"Не задан номер должности для для имени '{p.full_name}'; личный номер='{p.get_unique()}'; номер строки={index};")
				empty_unique.append(index)
			else:
				result[hsh] = index
		return result, empty_unique
