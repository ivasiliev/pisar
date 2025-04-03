from helpers.log_helper import log
from templateprocessor.replacement_unit import ReplacementUnit


class RuSoldHomeAddressReal(ReplacementUnit):
	def replace(self, actual_placeholder, text):
		rep_settings = self.get_report_settings()
		home_address_real = rep_settings["home_address_real"]
		log(f"{self.placeholder} заменен на {home_address_real}")
		return text.replace(self.placeholder, home_address_real)
