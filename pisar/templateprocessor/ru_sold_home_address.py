from helpers.log_helper import log
from templateprocessor.replacement_unit import ReplacementUnit


class RuSoldHomeAddress(ReplacementUnit):
	def replace(self, actual_placeholder, text):
		rep_settings = self.get_report_settings()
		home_address = rep_settings["home_address"]
		if len(home_address) == 0:
			home_address = " "
		log(f"{self.placeholder} заменен на {home_address}")
		return text.replace(self.placeholder, home_address)