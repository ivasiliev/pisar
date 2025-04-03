from helpers.log_helper import log
from templateprocessor.replacement_unit import ReplacementUnit


class RuSoldFather(ReplacementUnit):
	def replace(self, actual_placeholder, text):
		rep_settings = self.get_report_settings()
		father_name = rep_settings["father_name"]
		log(f"{self.placeholder} заменен на {father_name}")
		return text.replace(self.placeholder, father_name)
