from templateprocessor.replacement_unit import ReplacementUnit


class RuSoldSpouse(ReplacementUnit):
	def replace(self, actual_placeholder, text):
		return self.replace_from_report_settings(text, "spouse_name")
