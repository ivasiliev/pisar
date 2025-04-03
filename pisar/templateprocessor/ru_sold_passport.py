from helpers.log_helper import log
from templateprocessor.replacement_unit import ReplacementUnit


class RuSoldPassport(ReplacementUnit):
	def replace(self, actual_placeholder, text):
		rep_settings = self.get_report_settings()
		passport = rep_settings["passport"]
		log(f"{self.placeholder} заменен на {passport}")
		return text.replace(self.placeholder, passport)
