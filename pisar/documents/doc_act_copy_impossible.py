from documents.act_prototype import ActPrototype, ACT_TITLE, ACT_TEXT


class DocActCopyImpossible(ActPrototype):
	def get_name(self):
		return "Акт о невозможности получения копии протокола"

	def get_name_for_file(self):
		return f"{self.get_name()} ({self.get_soldier_info().full_name}).docx"

	def render(self):
		rep_settings = self.get_report_settings()
		self.data_model[ACT_TITLE] = "о невозможности получения копии протокола о грубом дисциплинарном проступке"
		sold_str = self.get_person_full_str(2, False, False, True, False)
		self.data_model[ACT_TEXT] = f"Нижеподписавшиеся должностные лица войсковой части {rep_settings['military_unit']} составили настоящий акт по факту невозможности получения копии протокола о грубом дисциплинарном проступке {sold_str}."
		super().render()
