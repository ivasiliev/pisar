from helpers.log_helper import log
from templateprocessor.replacement_unit import ReplacementUnit


class RuSoldEducation(ReplacementUnit):
	def replace(self, actual_placeholder, text):
		rep_settings = self.get_report_settings()
		education = rep_settings["education"]
		if len(education) == 0:
			education = " "
		log(f"{self.placeholder} заменен на {education}")
		return text.replace(self.placeholder, education)
