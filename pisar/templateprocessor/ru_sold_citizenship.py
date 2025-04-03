from helpers.log_helper import log
from templateprocessor.replacement_unit import ReplacementUnit


class RuSoldCitizenship(ReplacementUnit):
	def replace(self, actual_placeholder, text):
		rep_settings = self.get_report_settings()
		citizenship = rep_settings["citizenship"]
		log(f"{self.placeholder} заменен на {citizenship}")
		return text.replace(self.placeholder, citizenship)
