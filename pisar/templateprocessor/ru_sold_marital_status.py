from helpers.log_helper import log
from templateprocessor.replacement_unit import ReplacementUnit


class RuSoldMaritalStatus(ReplacementUnit):
	def replace(self, actual_placeholder, text):
		rep_settings = self.get_report_settings()
		marital_status = rep_settings["marital_status"]
		if len(marital_status) == 0:
			marital_status = " "
		log(f"{self.placeholder} заменен на {marital_status}")
		return text.replace(self.placeholder, marital_status)