from pytrovich.enums import Case, Gender, NamePart

from classes.document_in_report import MODEL_MORPHOLOGY_FOR_NAMES
from helpers.log_helper import log
from templateprocessor.replacement_unit import ReplacementUnit


class RuSoldFioShort1(ReplacementUnit):
	def replace(self, actual_placeholder, text):
		declension = self.extract_declension(actual_placeholder)
		if declension is None:
			return text
		s_info = self.get_soldier_info()
		fn = self.get_person_name_declension(self.get_person_name_short_format_1(s_info.full_name), declension)
		log(f"{actual_placeholder} заменен на {fn}")
		return text.replace(actual_placeholder, fn)

	# TODO to helper
	def get_person_name_declension(self, full_name, declension_type):
		if declension_type == 1:
			result = self.get_person_name_gent(full_name)
		else:
			if declension_type == 2:
				result = self.get_person_name_instr(full_name)
			else:
				if declension_type == 3:
					result = self.get_person_name_datv(full_name)
				else:
					result = full_name

		return result

	# TODO to helper
	def get_person_name_gent(self, full_name):
		return self.get_person_name_routines(full_name, Case.GENITIVE)

	def get_person_name_instr(self, full_name):
		return self.get_person_name_routines(full_name, Case.INSTRUMENTAL)

	def get_person_name_datv(self, full_name):
		return self.get_person_name_routines(full_name, Case.DATIVE)

	# TODO to helper
	def get_person_name_routines(self, full_name, cs):
		maker = self.data_model[MODEL_MORPHOLOGY_FOR_NAMES]
		if maker is None:
			log("Внутренняя ошибка. Морфоанализатор для имён не создан.")
			return ""

		if full_name is None or len(full_name) == 0:
			return ""

		name_tokens = full_name.split(" ")
		surname = name_tokens[0]
		first_name = ""
		if len(name_tokens) > 1:
			first_name = name_tokens[1]
		middle_name = ""
		if len(name_tokens) > 2:
			middle_name = name_tokens[2]

		rs = self.get_report_settings()
		gender = Gender.MALE
		if "gender" in rs and rs["gender"].casefold() == "ж":
			gender = Gender.FEMALE

		sn = maker.make(NamePart.LASTNAME, gender, cs, surname)
		fn = maker.make(NamePart.FIRSTNAME, gender, cs, first_name)
		mn = maker.make(NamePart.MIDDLENAME, gender, cs, middle_name)

		return f"{sn} {fn} {mn}".strip()

	# TODO helper
	def get_person_name_short_format_1(self, full_name):
		name_tokens = full_name.split(" ")
		if len(name_tokens) < 2:
			log(f"Не удалось преобразовать в нужный формат: {full_name}")
			return full_name
		surname = name_tokens[0]
		first_name = name_tokens[1]
		return f"{first_name[0]}. {surname}"