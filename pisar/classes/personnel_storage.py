import openpyxl

from classes.column_info import ColumnInfo
from classes.document_in_report import MODEL_JSON_OBJECT, MODEL_PERSONNEL_PATH, MODEL_PERSONNEL_DETAILS_PATH
from classes.excel_doc_metadata import ExcelDocMetadata
from classes.person import Person
from helpers.file_helper import get_file_size_info
from helpers.log_helper import log
from helpers.performance_helper import PerformanceHelper
from helpers.text_helper import not_empty

# Штатное расписание (ШР)
EXCEL_DOCUMENT_SR = 0
# Личный состав (ЛС)
EXCEL_DOCUMENT_LS = 1
COLUMN_UNIQUE_KEY = "COLUMN_UNIQUE"
COLUMN_FULL_NAME = "COLUMN_FULL_NAME"
COLUMN_DOB = "COLUMN_DOB"
COLUMN_PHONE = "COLUMN_PHONE"
COLUMN_HEIGHT = "COLUMN_HEIGHT"
COLUMN_WEIGHT = "COLUMN_WEIGHT"
COLUMN_SIGNS = "COLUMN_SIGNS"
COLUMN_TATOO = "COLUMN_TATOO"
COLUMN_ADDITIONAL_ATTRIBUTES = "COLUMN_ADDITIONAL_ATTRIBUTES"
COLUMN_HABITS = "COLUMN_HABITS"
COLUMN_PERSONAL_PERKS = "COLUMN_PERSONAL_PERKS"
COLUMN_RANK = "COLUMN_RANK"
COLUMN_POSITION = "COLUMN_POSITION"
# passports
COLUMN_PASS_DNR = "COLUMN_PASS_DNR"
COLUMN_PASS_DNR_ISSUED = "COLUMN_PASS_DNR_ISSUED"
COLUMN_PASS_RF = "COLUMN_PASS_RF"
COLUMN_PASS_RF_ISSUED = "COLUMN_PASS_RF_ISSUED"
COLUMN_PASS_FOREIGN = "COLUMN_PASS_FOREIGN"
COLUMN_PASS_UKR = "COLUMN_PASS_UKR"
# relatives
COLUMN_FATHER_NAME = "COLUMN_FATHER_NAME"
COLUMN_MOTHER_NAME = "COLUMN_MOTHER_NAME"
COLUMN_SIBLINGS_NAME = "COLUMN_SIBLINGS_NAME"
COLUMN_SPOUSE_NAME = "COLUMN_SPOUSE_NAME"
COLUMN_FATHER_ADDRESS = "COLUMN_FATHER_ADDRESS"
COLUMN_MOTHER_ADDRESS = "COLUMN_MOTHER_ADDRESS"
COLUMN_SIBLINGS_ADDRESS = "COLUMN_SIBLINGS_ADDRESS"
COLUMN_SPOUSE_ADDRESS = "COLUMN_SPOUSE_ADDRESS"
COLUMN_FATHER_PHONE = "COLUMN_FATHER_PHONE"
COLUMN_MOTHER_PHONE = "COLUMN_MOTHER_PHONE"
COLUMN_SIBLINGS_PHONE = "COLUMN_SIBLINGS_PHONE"
COLUMN_SPOUSE_PHONE = "COLUMN_SPOUSE_PHONE"


class PersonnelStorage:
	def __init__(self, data_model):
		# TODO to app_settings?
		self.personnel_excel_sheet_name = "ШДС"
		self.personnel_details_excel_sheet_name = "ЛС"
		self.data_model = data_model
		self.personnel_list_full_path = data_model[MODEL_PERSONNEL_PATH]
		self.personnel_details_full_path = data_model[MODEL_PERSONNEL_DETAILS_PATH]

		# TODO calculate it automatically
		self.MAX_COLUMNS_COUNT = 150
		self.is_valid = True

		self.excel_docs = [
			self.create_metadata_for_pers_list(self.personnel_list_full_path)
			,
			self.create_metadata_for_pers_details(self.personnel_details_full_path)
		]

		for md in self.excel_docs:
			workbook = openpyxl.load_workbook(md.full_path)
			log(f"--- Сведения о файле Excel {md.full_path} ---")
			log(f"Размер: {get_file_size_info(md.full_path)}")
			log(f"Всего листов: {len(workbook.sheetnames)}")
			log("Список листов:")
			log(workbook.sheetnames)
			log("------------------------------")
			if md.sheet_name not in workbook.sheetnames:
				log(
					f"В Excel-документе отсутствует лист '{md.sheet_name}'.")
				self.is_valid = False
			else:
				sh = workbook[md.sheet_name]
				# analyze headers
				for row in sh.iter_rows(min_row=1, min_col=1, max_row=1, max_col=md.column_count_to_search):
					for caption_cell in row:
						col_str = str(caption_cell.value).casefold()
						# firstly check exact match
						found = False
						for col_info in md.cols:
							if col_str == col_info.get_name():
								col_info.index = caption_cell.col_idx
								found = True
								break
						if not found:
							# not exact match
							for col_info in md.cols:
								if col_info.index > -1:
									continue
								if col_str.startswith(col_info.get_name()):
									col_info.index = caption_cell.col_idx
									break
				# validation
				for col_info in md.cols:
					if not col_info.is_found():
						log(f"Столбец '{col_info.get_name()}' не найден!")
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
		log("Поиск военнослужащего в ШР. Пожалуйста, подождите...")
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
					log(f"Обработано {iteration_count_to_find_person} строк...")
				break
			if person_row is not None:
				person = self.create_person_from_row(pers_list_excel_doc, person_row)
				break

		log(f"Количество итераций для поиска военнослужащего: {iteration_count_to_find_person}")
		performance.stop_and_print()

		# check on mandatory fields
		if person is not None and person.unique is None:
			log(f"Не задан личный номер для {person.full_name}! Продолжение работы невозможно.")
			person = None

		# let's find info in the auxiliary Excel document and replace Report Info about him
		if person is not None:
			log(
				f"Поиск военнослужащего личный номер {person.unique} в файле Информация о личном составе. Пожалуйста, подождите...")
			performance = PerformanceHelper()
			performance.start()
			iteration_count_to_find_person = 0
			count_for_report = 50
			col_unique = pers_details_excel_doc.get_column_index(COLUMN_UNIQUE_KEY)
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
						log(f"Обработано {iteration_count_to_find_person} строк...")
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
						, ["phone", COLUMN_PHONE]
						, ["height", COLUMN_HEIGHT]
						, ["weight", COLUMN_WEIGHT]
						, ["signs", COLUMN_SIGNS]
						, ["tatoo", COLUMN_TATOO]
						, ["habits", COLUMN_HABITS]
						, ["rank", COLUMN_RANK]
						, ["position", COLUMN_POSITION]
						, ["additional_attributes", COLUMN_ADDITIONAL_ATTRIBUTES]
						, ["personal_perks", COLUMN_PERSONAL_PERKS]
						# passports
						, ["pass_dnr", COLUMN_PASS_DNR]
						, ["pass_dnr_issued", COLUMN_PASS_DNR_ISSUED]
						, ["pass_rf", COLUMN_PASS_RF]
						, ["pass_rf_issued", COLUMN_PASS_RF_ISSUED]
						, ["pass_foreign", COLUMN_PASS_FOREIGN]
						, ["pass_ukr", COLUMN_PASS_UKR]
						# relatives
						, ["father_name", COLUMN_FATHER_NAME]
						, ["mother_name", COLUMN_MOTHER_NAME]
						, ["siblings_name", COLUMN_SIBLINGS_NAME]
						, ["spouse_name", COLUMN_SPOUSE_NAME]
						, ["father_address", COLUMN_FATHER_ADDRESS]
						, ["mother_address", COLUMN_MOTHER_ADDRESS]
						, ["siblings_address", COLUMN_SIBLINGS_ADDRESS]
						, ["spouse_address", COLUMN_SPOUSE_ADDRESS]
						, ["father_phone", COLUMN_FATHER_PHONE]
						, ["mother_phone", COLUMN_MOTHER_PHONE]
						, ["siblings_phone", COLUMN_SIBLINGS_PHONE]
						, ["spouse_phone", COLUMN_SPOUSE_PHONE]
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

					# select passport by priority
					# паспорт ДНР, паспорт РФ, паспорт Украины
					dm["passport"] = ""
					if not_empty(dm["pass_rf"]):
						dm["passport"] = f"паспорт РФ {dm['pass_rf']} {dm['pass_rf_issued']}"
					else:
						if not_empty(dm["pass_dnr"]):
							dm["passport"] = f"паспорт ДНР {dm['pass_dnr']} {dm['pass_dnr_issued']}"
						else:
							if not_empty(dm["pass_dnr"]):
								dm["passport"] = f"паспорт Украины {dm['pass_ukr']}"
					log(f"Количество итераций для поиска военнослужащего: {iteration_count_to_find_person}")
					performance.stop_and_print()
					break

		return person

	def find_value_in_row_by_index(self, row, index):
		result = ""
		for cell in row:
			if cell.col_idx == index:
				result = cell.value
				break
		if result is None:
			result = ""
		return result

	def create_metadata_for_pers_list(self, full_path):
		cols = [
			ColumnInfo("COLUMN_COMPANY", "рота")
			, ColumnInfo("COLUMN_PLATOON", "взвод")
			, ColumnInfo("COLUMN_SQUAD", "отделение")
			, ColumnInfo(COLUMN_POSITION, "воинская должность")
			, ColumnInfo(COLUMN_RANK, "воинское звание фактическое")
			, ColumnInfo(COLUMN_FULL_NAME, "фио")
			, ColumnInfo(COLUMN_DOB, "дата рождения")
			, ColumnInfo(COLUMN_UNIQUE_KEY, "личный номер")
		]

		return ExcelDocMetadata(full_path, self.personnel_excel_sheet_name, cols, 200)

	def create_metadata_for_pers_details(self, full_path):
		cols = [
			ColumnInfo(COLUMN_UNIQUE_KEY, "личный номер")
			, ColumnInfo(COLUMN_RANK, "в/звание")
			, ColumnInfo(COLUMN_POSITION, "в/должность")
			, ColumnInfo(COLUMN_FULL_NAME, "фио")
			, ColumnInfo(COLUMN_DOB, "дата рождения")
			, ColumnInfo("COLUMN_NATIONALITY", "национальность")
			, ColumnInfo("COLUMN_GENDER", "пол")
			, ColumnInfo("COLUMN_EDUCATION", "тип образования")
			, ColumnInfo("COLUMN_GRADUATION_PLACE", "учреждение(год окончания)")
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
			, ColumnInfo("COLUMN_CRIMINAL_STATUS", "наличие судимостей(погашены/нет)")
			, ColumnInfo(COLUMN_PHONE, "номер телефона")
			, ColumnInfo(COLUMN_HEIGHT, "рост")
			, ColumnInfo(COLUMN_WEIGHT, "вес")
			, ColumnInfo(COLUMN_SIGNS, "особые приметы")
			, ColumnInfo(COLUMN_TATOO, "татуировки")
			, ColumnInfo(COLUMN_ADDITIONAL_ATTRIBUTES, "описание дополнительных элементов")
			, ColumnInfo(COLUMN_PERSONAL_PERKS, "индивидуальные отличительные признаки")
			, ColumnInfo(COLUMN_HABITS, "увлечения")
			# passports
			, ColumnInfo(COLUMN_PASS_DNR, "Паспорт ДНР")
			, ColumnInfo(COLUMN_PASS_DNR_ISSUED, "Кем выдан")
			, ColumnInfo(COLUMN_PASS_RF, "Паспорт РФ")
			, ColumnInfo(COLUMN_PASS_RF_ISSUED, "Кем выдан2")
			, ColumnInfo(COLUMN_PASS_FOREIGN, "Загранпаспорт")
			, ColumnInfo(COLUMN_PASS_UKR, "Паспорт Украины")
			# relatives
			, ColumnInfo(COLUMN_FATHER_NAME, "фио отца, дата рождения")
			, ColumnInfo(COLUMN_MOTHER_NAME, "фио матери, дата рождения")
			, ColumnInfo(COLUMN_SIBLINGS_NAME, "фио братьев/сестер, дата рождения")
			, ColumnInfo(COLUMN_SPOUSE_NAME, "фио жены/мужа, дата рождения")
			, ColumnInfo(COLUMN_FATHER_ADDRESS, "Адрес проживания отца")
			, ColumnInfo(COLUMN_MOTHER_ADDRESS, "Адрес проживания матери")
			, ColumnInfo(COLUMN_SIBLINGS_ADDRESS, "Адрес проживания братьев/сестер")
			, ColumnInfo(COLUMN_SPOUSE_ADDRESS, "Адрес проживания жены/мужа")
			, ColumnInfo(COLUMN_FATHER_PHONE, "Номер телефона отца")
			, ColumnInfo(COLUMN_MOTHER_PHONE, "Номер телефона матери")
			, ColumnInfo(COLUMN_SIBLINGS_PHONE, "Номер телефона братьев/сестер")
			, ColumnInfo(COLUMN_SPOUSE_PHONE, "Номер телефона жены/мужа")
		]

		return ExcelDocMetadata(full_path, self.personnel_details_excel_sheet_name, cols, 200)

	# what_file=0 (ШР),what_file=1 (ЛС)
	def get_all_persons(self, what_file, row_limit=None):
		all_rows = self.read_excel_file(what_file, row_limit)
		all_persons = []
		excel_doc = self.excel_docs[what_file]
		for row in all_rows:
			all_persons.append(self.create_person_from_row(excel_doc, row))

		return all_persons

	def create_person_from_row(self, excel_doc, person_row):
		col_company = excel_doc.get_column_index("COLUMN_COMPANY")
		col_platoon = excel_doc.get_column_index("COLUMN_PLATOON")
		col_squad = excel_doc.get_column_index("COLUMN_SQUAD")
		col_position = excel_doc.get_column_index(COLUMN_POSITION)
		col_rank = excel_doc.get_column_index(COLUMN_RANK)
		col_full_name = excel_doc.get_column_index(COLUMN_FULL_NAME)
		col_dob = excel_doc.get_column_index(COLUMN_DOB)
		col_unique = excel_doc.get_column_index(COLUMN_UNIQUE_KEY)
		col_phone = excel_doc.get_column_index(COLUMN_PHONE)

		person = Person()
		# TODO this is incorrect because ID_SR and ID_LS are different values
		person.id_sr = self.find_value_in_row_by_index(person_row, 1)
		person.company = self.find_value_in_row_by_index(person_row, col_company)
		person.platoon = self.find_value_in_row_by_index(person_row, col_platoon)
		person.squad = self.find_value_in_row_by_index(person_row, col_squad)
		person.position = self.find_value_in_row_by_index(person_row, col_position)
		person.rank = self.find_value_in_row_by_index(person_row, col_rank)
		person.full_name = self.find_value_in_row_by_index(person_row, col_full_name)
		person.set_dob(self.find_value_in_row_by_index(person_row, col_dob))
		person.unique = self.find_value_in_row_by_index(person_row, col_unique)
		person.phone = self.find_value_in_row_by_index(person_row, col_phone)

		# normalization of a soldier name
		if person.full_name is not None:
			person.full_name = person.full_name.title()

		if person.position is not None:
			person.position = person.position.lower()
		else:
			person.position = ""
		if person.rank is not None:
			person.rank = person.rank.lower()
		else:
			person.rank = ""

		return person

	# what_file=0 (ШР),what_file=1 (ЛС)
	def read_excel_file(self, what_file, row_limit=None):
		excel_doc = self.excel_docs[what_file]
		# this id must be at the first column of the personnel list Excel file
		workbook = openpyxl.load_workbook(excel_doc.full_path)
		sh = workbook[excel_doc.sheet_name]

		# TODO
		# if None in indexes:
		#	print(f"Не удалось определить индексы столбцов! Выполнение программы прервано.")
		#	return

		performance = PerformanceHelper()
		performance.start()
		iteration_count = 0
		count_for_report = 50
		log("Просмотр списка военнослужащих. Пожалуйста, подождите...")
		max_row_value = 2001
		if row_limit is not None:
			max_row_value = row_limit
		all_rows = []
		for row in sh.iter_rows(min_row=2, min_col=1, max_row=max_row_value, max_col=self.MAX_COLUMNS_COUNT):
			if row[0].value is None:
				break
			all_rows.append(row)

			iteration_count = iteration_count + 1
			if iteration_count % count_for_report == 0:
				log(f"Обработано {iteration_count} строк...")

		log(f"Количество итераций для просмотра списка: {iteration_count}")
		log(f"Обнаружено военнослужащих: {len(all_rows)}")
		performance.stop_and_print()

		return all_rows

	def read_excel_header(self, what_file):
		excel_doc = self.excel_docs[what_file]
		# this id must be at the first column of the personnel list Excel file
		workbook = openpyxl.load_workbook(excel_doc.full_path)
		sh = workbook[excel_doc.sheet_name]
		row_header = None
		for row in sh.iter_rows(min_row=1, min_col=1, max_row=1, max_col=self.MAX_COLUMNS_COUNT):
			row_header = row
			break

		return row_header
