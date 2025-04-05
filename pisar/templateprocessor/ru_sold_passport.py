from helpers.log_helper import log
from templateprocessor.replacement_unit import ReplacementUnit


class RuSoldPassport(ReplacementUnit):
	def replace(self, actual_placeholder, text):
		return self.replace_from_report_settings(text, "passport")
