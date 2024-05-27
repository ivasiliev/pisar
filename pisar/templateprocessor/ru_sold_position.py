from helpers.log_helper import log
from helpers.text_helper import get_word_declension
from templateprocessor.replacement_unit import ReplacementUnit


class RuSoldPosition(ReplacementUnit):
	def replace(self, actual_placeholder, text):
		declension = self.extract_declension(actual_placeholder)
		if declension is None:
			return text
		s_info = self.get_soldier_info()
		sld_position = get_word_declension(self.get_morph(), s_info.position, declension)
		log(f"{actual_placeholder} заменен на {sld_position}")
		return text.replace(actual_placeholder, sld_position)
