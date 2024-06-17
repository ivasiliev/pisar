from helpers.log_helper import log
from templateprocessor.replacement_unit import ReplacementUnit


class RuDobShort(ReplacementUnit):
	def replace(self, actual_placeholder, text):
		s_info = self.get_soldier_info()
		dob = f"{s_info.get_dob()} г.р."
		log(f"{self.placeholder} заменен на {dob}")
		return text.replace(self.placeholder, dob)
