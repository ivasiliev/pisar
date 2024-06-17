from helpers.log_helper import log
from templateprocessor.replacement_unit import ReplacementUnit


class RuSoldUnique(ReplacementUnit):
	def replace(self, actual_placeholder, text):
		s_info = self.get_soldier_info()
		log(f"{self.placeholder} заменен на {s_info.unique}")
		return text.replace(self.placeholder, s_info.unique)
