from templateprocessor.replacement_unit import ReplacementUnit


class RuSoldMaritalStatus(ReplacementUnit):
	def replace(self, actual_placeholder, text):
		return self.replace_from_report_settings(text, "marital_status")
