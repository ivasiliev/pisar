from templateprocessor.replacement_unit import ReplacementUnit


class RuDob(ReplacementUnit):
	def replace(self, text):
		s_info = self.get_soldier_info()
		dob = self.get_date_format_1(s_info.get_dob())
		return text.replace(self.placeholder, dob)
