from helpers.log_helper import log
from templateprocessor.replacement_unit import ReplacementUnit


class RuDateEventShort(ReplacementUnit):
	def replace(self, actual_placeholder, text):
		de = self.get_date_of_event()
		log(f"{self.placeholder} заменен на {de}")
		return text.replace(self.placeholder, de)
