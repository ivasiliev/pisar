from helpers.log_helper import log
from templateprocessor.replacement_unit import ReplacementUnit


class RuSoldSpouse(ReplacementUnit):
	def replace(self, actual_placeholder, text):
		rep_settings = self.get_report_settings()
		spouse_name = rep_settings["spouse_name"]
		if len(spouse_name) == 0:
			spouse_name = " "
		log(f"{self.placeholder} заменен на {spouse_name}")
		return text.replace(self.placeholder, spouse_name)
