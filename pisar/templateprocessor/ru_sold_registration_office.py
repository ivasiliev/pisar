from templateprocessor.replacement_unit import ReplacementUnit


# военкомат, откуда призван военнослужащий
class RuSoldRegistrationOffice(ReplacementUnit):
	def replace(self, actual_placeholder, text):
		return self.replace_from_report_settings(text, "registration_office")
