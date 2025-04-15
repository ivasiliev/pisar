from templateprocessor.replacement_unit import ReplacementUnit


class RuSoldAdditionalAttributes(ReplacementUnit):
	def replace(self, actual_placeholder, text):
		return self.replace_from_report_settings(text, "additional_attributes")
