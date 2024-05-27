from helpers.log_helper import log
from helpers.text_helper import replace_with_glue, get_month_string
from templateprocessor.replacement_unit import ReplacementUnit


class RuDob(ReplacementUnit):
	def replace(self, actual_placeholder, text):
		s_info = self.get_soldier_info()
		dob = self.get_date_format_1(s_info.get_dob())
		log(f"{self.placeholder} заменен на {dob}")
		return text.replace(self.placeholder, dob)

	# TODO put in helper
	def get_date_format_1(self, date_str):
		tokens = date_str.split(".")
		if len(tokens) != 3:
			return date_str
		# print(f"Не удалось определить формат даты {date_str}")
		d = int(tokens[0])
		m = int(tokens[1])
		y = int(tokens[2])
		return replace_with_glue(f"{d} {get_month_string(m)} {y} года")
