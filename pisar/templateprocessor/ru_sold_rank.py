from helpers.log_helper import log
from helpers.text_helper import get_word_declension
from templateprocessor.replacement_unit import ReplacementUnit


class RuSoldRank(ReplacementUnit):
	def replace(self, actual_placeholder, text):
		declension = self.extract_declension(actual_placeholder)
		if declension is None:
			return text
		s_info = self.get_soldier_info()
		r = self.get_person_rank(s_info.rank, declension)
		log(f"{actual_placeholder} заменен на {r}")
		return text.replace(actual_placeholder, r)

	def get_person_rank(self, rnk, declension_type):
		if declension_type != 0:
			rnk = get_word_declension(self.get_morph(), rnk, declension_type)
		if self.get_report_settings()["is_guard"]:
			rnk = "гвардии " + rnk
		return rnk
