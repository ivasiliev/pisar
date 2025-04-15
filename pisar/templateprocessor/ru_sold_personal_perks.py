from templateprocessor.replacement_unit import ReplacementUnit


class RuSoldPersonalPerks(ReplacementUnit):
	def replace(self, actual_placeholder, text):
		return self.replace_from_report_settings(text, "personal_perks")
