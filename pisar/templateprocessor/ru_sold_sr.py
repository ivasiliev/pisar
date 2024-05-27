from helpers.log_helper import log
from helpers.text_helper import replace_with_glue, get_words_declension
from templateprocessor.replacement_unit import ReplacementUnit


class RuSoldSr(ReplacementUnit):
	def replace(self, actual_placeholder, text):
		declension = self.extract_declension(actual_placeholder)
		if declension is None:
			return text
		sr = self.get_soldier_address(declension)
		log(f"{actual_placeholder} заменен на {sr}")
		return text.replace(actual_placeholder, sr)

	def get_soldier_address(self, declension_type):
		s_info = self.get_soldier_info()
		sq = replace_with_glue(get_words_declension(self.get_morph(), s_info.squad, declension_type).strip())
		pl = replace_with_glue(get_words_declension(self.get_morph(), s_info.platoon, declension_type).strip())
		cm = replace_with_glue(get_words_declension(self.get_morph(), s_info.company, declension_type).strip())
		return f"{sq} {pl} {cm}"
