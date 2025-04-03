from helpers.log_helper import log
from templateprocessor.replacement_unit import ReplacementUnit


class RuSoldSiblings(ReplacementUnit):
	def replace(self, actual_placeholder, text):
		rep_settings = self.get_report_settings()
		siblings_name = rep_settings["siblings_name"]
		if len(siblings_name) == 0:
			siblings_name = " "
		log(f"{self.placeholder} заменен на {siblings_name}")
		return text.replace(self.placeholder, siblings_name)
