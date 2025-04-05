from templateprocessor.replacement_unit import ReplacementUnit


class RuSoldSiblings(ReplacementUnit):
	def replace(self, actual_placeholder, text):
		return self.replace_from_report_settings(text, "siblings_name")
