import openpyxl

from classes.person import Person


class PersonnelStorage:
	# full_path = xlsx file
	def __init__(self, full_path):
		self.storage = None
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

		workbook = openpyxl.load_workbook(self.personnel_list_full_path)
		sh = workbook.active  # TODO use sheet #0

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

	def find_person_by_id(self, id_person):
		id_person_str = str(id_person)
		# this id must be at the first column of the personnel list Excel file
		workbook = openpyxl.load_workbook(self.personnel_list_full_path)
		sh = workbook.active  # TODO use sheet #0
		indexes = [self.COLUMN_COMPANY, self.COLUMN_PLATOON, self.COLUMN_SQUAD, self.COLUMN_POSITION,
		           self.COLUMN_FULL_NAME, self.COLUMN_DOB]
		person = Person()
		# analyze headers
		for row in sh.iter_rows(min_row=2, min_col=1, max_row=2000, max_col=max(indexes) + 1):
			person_row = None
			for cell in row:
				if cell.col_idx > 1:
					continue
				if cell.value is None:
					break
				if str(cell.value) == id_person_str:
					person_row = row
					break
			if person_row is not None:
				person.company = self.find_value_in_row_by_index(person_row, self.COLUMN_COMPANY)
				person.platoon = self.find_value_in_row_by_index(person_row, self.COLUMN_PLATOON)
				person.squad = self.find_value_in_row_by_index(person_row, self.COLUMN_SQUAD)
				person.position = self.find_value_in_row_by_index(person_row, self.COLUMN_POSITION)
				person.rank = self.find_value_in_row_by_index(person_row, self.COLUMN_RANK)
				person.full_name = self.find_value_in_row_by_index(person_row, self.COLUMN_FULL_NAME)
				person.set_dob(self.find_value_in_row_by_index(person_row, self.COLUMN_DOB))

				person.position = person.position.lower()
				person.rank = person.rank.lower()

				break
		if person is not None:
			# search for company commander
			for row in sh.iter_rows(min_row=2, min_col=1, max_row=2000, max_col=max(indexes) + 1):
				commander_name = None
				commander_rank = None
				commander_position = None
				company_found = False
				commander_row_found = False
				for cell in row:
					if cell.value is None:
						continue
					cv = str(cell.value)
					cvl = cv.lower()
					if cell.col_idx == self.COLUMN_COMPANY and int(cv) == int(person.company):
						company_found = True
						continue
					if company_found and cell.col_idx == self.COLUMN_POSITION:
						# if "командир" in cvl and "рот" in cvl:
						if "командир" in cvl:
							commander_row_found = True
					if commander_row_found:
						if cell.col_idx == self.COLUMN_RANK:
							commander_rank = cvl
						else:
							if cell.col_idx == self.COLUMN_POSITION:
								commander_position = cv
							else:
								if cell.col_idx == self.COLUMN_FULL_NAME:
									commander_name = cv
				if commander_rank is not None and commander_position is not None and commander_name is not None:
					person.company_commander = {"name": commander_name, "rank": commander_rank, "position": commander_position, "company": int(person.company)}
					break

		return person

	def find_value_in_row_by_index(self, row, index):
		for cell in row:
			if cell.col_idx == index:
				return cell.value
		return None
