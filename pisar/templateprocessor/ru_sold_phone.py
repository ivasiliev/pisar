from helpers.log_helper import log
from templateprocessor.replacement_unit import ReplacementUnit


class RuSoldPhone(ReplacementUnit):
	def replace(self, actual_placeholder, text):
		rep_settings = self.get_report_settings()
		phone = rep_settings["phone"]
		log(f"{self.placeholder} заменен на {phone}")
		return text.replace(self.placeholder, phone)
