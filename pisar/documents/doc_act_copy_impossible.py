from classes.pers_full_name_settings import PersFullNameSettings
from documents.act_prototype import ActPrototype, ACT_TITLE, ACT_TEXT


class DocActCopyImpossible(ActPrototype):
	def get_name(self):
		return "Акт о невозможности получения копии протокола"

	def get_name_for_file(self):
		return f"{self.get_name()} ({self.get_soldier_info().full_name}).docx"

	def render(self):
		self.data_model[ACT_TITLE] = "о невозможности получения копии протокола о грубом дисциплинарном проступке"
		settings = PersFullNameSettings(2, False, False, True, False, False, False)
		sold_str = self.get_person_full_str(settings)
		self.data_model[ACT_TEXT] = f"Нижеподписавшиеся должностные лица войсковой части {self.get_military_unit()} составили настоящий акт по факту невозможности получения копии протокола о грубом дисциплинарном проступке {sold_str}."
		super().render()
