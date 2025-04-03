from helpers.log_helper import log
from templateprocessor.replacement_unit import ReplacementUnit

# TODO
class RuSoldCitizenship(ReplacementUnit):
	def replace(self, actual_placeholder, text):
		rep_settings = self.get_report_settings()
		reg_office = rep_settings["registration_office"]
		log(f"{self.placeholder} заменен на {reg_office}")
		return text.replace(self.placeholder, reg_office)