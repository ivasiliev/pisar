from templateprocessor.replacement_unit import ReplacementUnit


class RuSoldPlaceOfBirth(ReplacementUnit):
	def replace(self, actual_placeholder, text):
		return self.replace_from_report_settings(text, "place_of_birth")
