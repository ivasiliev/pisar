from datetime import date

from openpyxl.workbook import Workbook

from classes.personnel_storage import EXCEL_DOCUMENT_SR, EXCEL_DOCUMENT_LS
from helpers.log_helper import log
from utils.utility_prototype import UtilityPrototype


class UtilityPersonnelDetailsSorting(UtilityPrototype):
	def __init__(self, data_model):
		super().__init__(data_model)

	def get_name(self):
		return "Сортировка ЛС по порядку в ШР"

	def get_name_for_file(self):
		current_date = date.today()
		return f"{self.get_name()}-{self.get_date_string(current_date)}.xlsx"

	def render(self):
		pers_storage = self.get_pers_storage()
		# prepare hashes for search
		persons_sr = pers_storage.get_all_persons(EXCEL_DOCUMENT_SR)
		persons_ls = pers_storage.get_all_persons(EXCEL_DOCUMENT_LS)
		sr_hash, sr_empty_unique = self.prepare_hash_list(persons_sr)
		ls_hash, ls_empty_unique = self.prepare_hash_list(persons_ls)
		# reading LS document
		all_ls_rows = pers_storage.read_excel_file(EXCEL_DOCUMENT_LS)
		log(f"Количество в ШР: {len(persons_sr)}; Количество в ЛС: {len(persons_ls)}; Всего строк в ЛС: {len(all_ls_rows)};")
		log(f"Количество людей с пустыми личными номерами в ШР: {len(sr_empty_unique)};")
		log(f"Количество людей с пустыми личными номерами в ЛС: {len(ls_empty_unique)};")
		new_ls_rows = []
		# header of LS document
		row_header = pers_storage.read_excel_header(EXCEL_DOCUMENT_LS)

		# rows rearranged according SR (they exist in SR)
		used_ls_indexes = []

		# create new LS document based on SR rows order
		for sr_hash_item in sr_hash:
			# skip persons that doesn't exist in LS
			if sr_hash_item not in ls_hash:
				continue
			index_in_ls = ls_hash[sr_hash_item]
			row_in_ls = all_ls_rows[index_in_ls]
			new_ls_rows.append(row_in_ls)
			used_ls_indexes.append(index_in_ls)
		log(f"Сведено ЛС > ШР {len(used_ls_indexes)} человек(а)")

		# put all rows from LS that weren't touched by sorting in the end of the document
		if len(used_ls_indexes) < len(all_ls_rows):
			added_persons = 0
			log(f"Добавляем остальных людей из ЛС, которых не было в ШР ({len(used_ls_indexes)} < {len(all_ls_rows)})")
			index = -1
			for r in all_ls_rows:
				index = index + 1
				if index not in used_ls_indexes:
					new_ls_rows.append(r)
					added_persons = added_persons + 1
			log(f"Добавлено людей: {added_persons}")

		# check that all rows are onboarded
		if len(new_ls_rows) != len(all_ls_rows):
			log("Внутренняя ошибка. Не все строки перемещены в новый документ.")
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

	def prepare_hash_list(self, pers_list):
		index = -1
		result = {}
		empty_unique = []
		for p in pers_list:
			index = index + 1
			hsh = p.get_hash()
			if hsh is None:
				log(f"Не могу определить hash для имени '{p.full_name}'; личный номер='{p.get_unique()}'; номер строки={index};")
				empty_unique.append(index)
			else:
				result[hsh] = index
		return result, empty_unique

	def convert_rows_to_lists(self, rows):
		all_rows = []
		for row in rows:
			row_list = []
			for cell in row:
				row_list.append(cell.value)
			all_rows.append(row_list)
		return all_rows
