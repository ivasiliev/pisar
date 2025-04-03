from helpers.log_helper import log
from templateprocessor.replacement_unit import ReplacementUnit


class RuSoldMother(ReplacementUnit):
	def replace(self, actual_placeholder, text):
		rep_settings = self.get_report_settings()
		mother_name = rep_settings["mother_name"]
		if len(mother_name) == 0:
			mother_name = " "
		log(f"{self.placeholder} заменен на {mother_name}")
		return text.replace(self.placeholder, mother_name)
