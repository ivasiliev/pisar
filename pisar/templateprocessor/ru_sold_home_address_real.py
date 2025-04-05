from templateprocessor.replacement_unit import ReplacementUnit


class RuSoldHomeAddressReal(ReplacementUnit):
	def replace(self, actual_placeholder, text):
		return self.replace_from_report_settings(text, "home_address_real")
