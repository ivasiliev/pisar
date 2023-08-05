import openpyxl

from classes.column_info import ColumnInfo
from classes.document_in_report import MODEL_JSON_OBJECT, MODEL_PERSONNEL_PATH, MODEL_PERSONNEL_DETAILS_PATH
from classes.excel_doc_metadata import ExcelDocMetadata
from classes.person import Person
from helpers.file_helper import get_file_size_info
from helpers.performance_helper import PerformanceHelper


class PersonnelStorage:
	# full_path = xlsx file
	def __init__(self, data_model):
		# self.storage = None
		# TODO to app_settings?
		self.personnel_excel_sheet_name = "ШДС"
		self.personnel_details_excel_sheet_name = "ЛС"
		self.data_model = data_model
		self.personnel_list_full_path = data_model[MODEL_PERSONNEL_PATH]
		self.personnel_details_full_path = data_model[MODEL_PERSONNEL_DETAILS_PATH]
		self.COLUMN_UNIQUE_KEY = "COLUMN_UNIQUE"
		self.COLUMN_FULL_NAME = "COLUMN_FULL_NAME"
		self.COLUMN_DOB = "COLUMN_DOB"
		# TODO calculate it automatically
		self.MAX_COLUMNS_COUNT = 80
		self.is_valid = True

		self.excel_docs = [
			self.create_metadata_for_pers_list(self.personnel_list_full_path)
			, self.create_metadata_for_pers_details(self.personnel_details_full_path)
		]

		for md in self.excel_docs:
			workbook = openpyxl.load_workbook(md.full_path)
			print(f"--- Сведения о файле Excel {md.full_path} ---")
			print(f"Размер: {get_file_size_info(md.full_path)}")
			print(f"Всего листов: {len(workbook.sheetnames)}")
			print("Список листов:")
			print(workbook.sheetnames)
			print("------------------------------")
			if md.sheet_name not in workbook.sheetnames:
				print(
					f"В Excel-документе отсутствует лист '{md.sheet_name}'.")
				self.is_valid = False
			else:
				sh = workbook[md.sheet_name]
				# analyze headers
				for row in sh.iter_rows(min_row=1, min_col=1, max_row=1, max_col=md.column_count_to_search):
					for cell in row:
						col_str = str(cell.value).casefold()
						for col_info in md.cols:
							if col_str == col_info.get_name():
								col_info.index = cell.col_idx
								break
				# validation
				for col_info in md.cols:
					if not col_info.is_found():
						print(f"Столбец '{col_info.get_name()}' не найден!")
						self.is_valid = False

	def find_person_by_id(self, id_person):
		id_person_str = str(id_person)
		pers_list_excel_doc = self.excel_docs[0]
		pers_details_excel_doc = self.excel_docs[1]
		# this id must be at the first column of the personnel list Excel file
		workbook = openpyxl.load_workbook(pers_list_excel_doc.full_path)
		sh = workbook[pers_list_excel_doc.sheet_name]

		performance = PerformanceHelper()
		performance.start()
		person = None
		iteration_count_to_find_person = 0
		count_for_report = 50
		print("Поиск военнослужащего в ШР. Пожалуйста, подождите...")
		for row in sh.iter_rows(min_row=2, min_col=1, max_row=2001, max_col=self.MAX_COLUMNS_COUNT):
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
				person = self.create_person_from_row(pers_list_excel_doc, person_row)
				break

		print(f"Количество итераций для поиска военнослужащего: {iteration_count_to_find_person}")
		performance.stop_and_print()

		# check on mandatory fields
		if person is not None and person.unique is None:
			print(f"Не задан личный номер для {person.full_name}! Продолжение работы невозможно.")
			person = None

		# let's find info in the auxiliary Excel document and replace Report Info about him
		if person is not None:
			print(
				f"Поиск военнослужащего личный номер {person.unique} в файле Информация о личном составе. Пожалуйста, подождите...")
			performance = PerformanceHelper()
			performance.start()
			iteration_count_to_find_person = 0
			count_for_report = 50
			col_unique = pers_details_excel_doc.get_column_index(self.COLUMN_UNIQUE_KEY)
			workbook = openpyxl.load_workbook(pers_details_excel_doc.full_path)
			sh = workbook[pers_details_excel_doc.sheet_name]
			person_row = None
			for row in sh.iter_rows(min_row=2, min_col=1, max_row=2001,
			                        max_col=pers_details_excel_doc.column_count_to_search):
				for cell in row:
					iteration_count_to_find_person = iteration_count_to_find_person + 1
					if cell.col_idx != col_unique:
						continue
					if cell.value is None:
						break
					if str(cell.value) == person.unique:
						person_row = row
						break
					if iteration_count_to_find_person % count_for_report == 0:
						print(f"Обработано {iteration_count_to_find_person} строк...")
					break

				if person_row is not None:
					dm = self.data_model[MODEL_JSON_OBJECT]
					mapping = [
						["nationality", "COLUMN_NATIONALITY"]
						, ["gender", "COLUMN_GENDER"]
						, ["education", "COLUMN_EDUCATION"]
						, ["graduation_place", "COLUMN_GRADUATION_PLACE"]
						, ["specialization", "COLUMN_SPECIALIZATION"]
						, ["occupation", "COLUMN_OCCUPATION"]
						, ["foreign_languages", "COLUMN_FOREIGN_LANGUAGES"]
						, ["awards", "COLUMN_AWARDS"]
						, ["government_authority", "COLUMN_GOVERNMENT_AUTHORITY"]
						, ["foreign_countries_visited", "COLUMN_FOREIGN_COUNTRIES_VISITED"]
						, ["service_started", "COLUMN_SERVICE_STARTED"]
						, ["place_of_birth", "COLUMN_PLACE_OF_BIRTH"]
						, ["home_address", "COLUMN_HOME_ADDRESS"]
						, ["marital_status", "COLUMN_MARITAL_STATUS"]
						, ["criminal_status", "COLUMN_CRIMINAL_STATUS"]
						, ["father_name", "COLUMN_FATHER_NAME"]
						, ["mother_name", "COLUMN_MOTHER_NAME"]
					]

					for m in mapping:
						dm[m[0]] = self.find_value_in_row_by_index(person_row,
						                                           pers_details_excel_doc.get_column_index(m[1]))

					parents_mapping = ["father_name", "mother_name"]
					parents_delimiter = ","
					for p in parents_mapping:
						n = str(dm[p])
						if parents_delimiter in n:
							tokens = n.split(parents_delimiter)
							if len(tokens) >= 2:
								dm[p] = tokens[0]

					dm["passport"] = ""
					passport_key = "COLUMN_PASSPORT_X"
					passport_issued_key = "COLUMN_PASSPORT_ISSUED_X"
					priorities = [
						[2, "паспорт РФ"]
						, [1, "паспорт ДНР"]
						, [3, "паспорт Украины"]
					]
					for pr in priorities:
						p = pr[0]
						key1 = passport_key.replace("X", str(p))
						passport_number = self.find_value_in_row_by_index(person_row,
						                                                  pers_details_excel_doc.get_column_index(key1))
						if passport_number is not None and len(passport_number) > 0:
							key2 = passport_issued_key.replace("X", str(p))
							passport_issued = self.find_value_in_row_by_index(person_row,
							                                                  pers_details_excel_doc.get_column_index(
								                                                  key2))
							dm["passport"] = f"{pr[1]} {passport_number} {passport_issued}"
							break
					print(f"Количество итераций для поиска военнослужащего: {iteration_count_to_find_person}")
					performance.stop_and_print()
					break

		return person

	def find_value_in_row_by_index(self, row, index):
		for cell in row:
			if cell.col_idx == index:
				return cell.value
		return None

	def create_metadata_for_pers_list(self, full_path):
		cols = [ColumnInfo("COLUMN_COMPANY", "рота")
			, ColumnInfo("COLUMN_PLATOON", "взвод")
			, ColumnInfo("COLUMN_SQUAD", "отделение")
			, ColumnInfo("COLUMN_POSITION", "воинская должность")
			, ColumnInfo("COLUMN_RANK", "воинское звание фактическое")
			, ColumnInfo(self.COLUMN_FULL_NAME, "фио")
			, ColumnInfo(self.COLUMN_DOB, "дата рождения")
			, ColumnInfo(self.COLUMN_UNIQUE_KEY, "личный номер")
		        ]

		return ExcelDocMetadata(full_path, self.personnel_excel_sheet_name, cols, 20)

	def create_metadata_for_pers_details(self, full_path):
		cols = [
			ColumnInfo(self.COLUMN_UNIQUE_KEY, "личный номер")
			, ColumnInfo(self.COLUMN_FULL_NAME, "фио")
			, ColumnInfo(self.COLUMN_DOB, "дата рождения")
			, ColumnInfo("COLUMN_NATIONALITY", "национальность")
			, ColumnInfo("COLUMN_GENDER", "пол")
			, ColumnInfo("COLUMN_EDUCATION", "тип образования")
			, ColumnInfo("COLUMN_GRADUATION_PLACE", "учреждение")
			, ColumnInfo("COLUMN_SPECIALIZATION", "профессия")
			, ColumnInfo("COLUMN_OCCUPATION", "места работы")
			, ColumnInfo("COLUMN_FOREIGN_LANGUAGES", "знание иностранных языков")
			, ColumnInfo("COLUMN_AWARDS", "награды")
			, ColumnInfo("COLUMN_GOVERNMENT_AUTHORITY", "является ли депутатом")
			, ColumnInfo("COLUMN_FOREIGN_COUNTRIES_VISITED", "какие страны посещал/посещала")
			, ColumnInfo("COLUMN_SERVICE_STARTED", "дата подписания контракта")
			, ColumnInfo("COLUMN_PLACE_OF_BIRTH", "место рождения")
			, ColumnInfo("COLUMN_HOME_ADDRESS", "адрес прописки")
			, ColumnInfo("COLUMN_MARITAL_STATUS", "семейное положение")
			, ColumnInfo("COLUMN_PASSPORT_1", "паспорт ДНР")
			, ColumnInfo("COLUMN_PASSPORT_ISSUED_1", "кем выдан")
			, ColumnInfo("COLUMN_PASSPORT_2", "паспорт РФ")
			, ColumnInfo("COLUMN_PASSPORT_ISSUED_2", "кем выдан2")
			, ColumnInfo("COLUMN_PASSPORT_3", "паспорт Украины")
			, ColumnInfo("COLUMN_PASSPORT_ISSUED_3", "адресная справка")
			, ColumnInfo("COLUMN_CRIMINAL_STATUS", "наличие судимостей")
			, ColumnInfo("COLUMN_FATHER_NAME", "фио отца, дата рождения")
			, ColumnInfo("COLUMN_MOTHER_NAME", "фио матери, дата рождения")
		]

		return ExcelDocMetadata(full_path, self.personnel_details_excel_sheet_name, cols, 70)

	# what_file=0 (ШР),what_file=1 (ЛС)
	def get_all_persons(self, what_file, row_limit=None):
		excel_doc = self.excel_docs[what_file]
		# this id must be at the first column of the personnel list Excel file
		workbook = openpyxl.load_workbook(excel_doc.full_path)
		sh = workbook[excel_doc.sheet_name]

		# TODO
		#if None in indexes:
		#	print(f"Не удалось определить индексы столбцов! Выполнение программы прервано.")
		#	return

		performance = PerformanceHelper()
		performance.start()
		iteration_count = 0
		count_for_report = 50
		print("Просмотр списка военнослужащих. Пожалуйста, подождите...")
		max_row_value = 2001
		if row_limit is not None:
			max_row_value = row_limit
		all_persons = []
		for row in sh.iter_rows(min_row=2, min_col=1, max_row=max_row_value, max_col=self.MAX_COLUMNS_COUNT):
			if row[0].value is None:
				break
			all_persons.append(self.create_person_from_row(excel_doc, row))

			iteration_count = iteration_count + 1
			if iteration_count % count_for_report == 0:
				print(f"Обработано {iteration_count} строк...")

		print(f"Количество итераций для просмотра списка: {iteration_count}")
		print(f"Обнаружено военнослужащих: {len(all_persons)}")
		performance.stop_and_print()

		return all_persons

	def create_person_from_row(self, excel_doc, person_row):
		col_company = excel_doc.get_column_index("COLUMN_COMPANY")
		col_platoon = excel_doc.get_column_index("COLUMN_PLATOON")
		col_squad = excel_doc.get_column_index("COLUMN_SQUAD")
		col_position = excel_doc.get_column_index("COLUMN_POSITION")
		col_rank = excel_doc.get_column_index("COLUMN_RANK")
		col_full_name = excel_doc.get_column_index(self.COLUMN_FULL_NAME)
		col_dob = excel_doc.get_column_index(self.COLUMN_DOB)
		col_unique = excel_doc.get_column_index(self.COLUMN_UNIQUE_KEY)

		person = Person()
		person.company = self.find_value_in_row_by_index(person_row, col_company)
		person.platoon = self.find_value_in_row_by_index(person_row, col_platoon)
		person.squad = self.find_value_in_row_by_index(person_row, col_squad)
		person.position = self.find_value_in_row_by_index(person_row, col_position)
		person.rank = self.find_value_in_row_by_index(person_row, col_rank)
		person.full_name = self.find_value_in_row_by_index(person_row, col_full_name)
		person.set_dob(self.find_value_in_row_by_index(person_row, col_dob))
		person.unique = self.find_value_in_row_by_index(person_row, col_unique)

		# normalization of a soldier name
		if person.full_name is not None:
			person.full_name = person.full_name.title()

		person.position = person.position.lower()
		person.rank = person.rank.lower()

		return person