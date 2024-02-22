from classes.pers_full_name_settings import PersFullNameSettings
from documents.act_prototype import ActPrototype, ACT_TITLE, ACT_TEXT


class DocActExplanationImpossible(ActPrototype):
	def get_name(self):
		return "Акт о невозможности взять объяснения по факту ГДП"

	def get_name_for_file(self):
		return f"{self.get_name()} ({self.get_soldier_info().full_name}).docx"

	def render(self):
		self.data_model[ACT_TITLE] = "о невозможности взять объяснения по факту действий совершенных военнослужащим, " \
		                             "в которых усматривается преступления против военной службы."
		settings = PersFullNameSettings(2, False, False, True, False, False, False)
		sold_str = self.get_person_full_str(settings)
		self.data_model[ACT_TEXT] = f"Нижеподписавшиеся должностные лица войсковой части {self.get_military_unit()} составили настоящий акт о невозможности дачи объяснений по факту самовольного оставления воинской части {sold_str}, в связи с его отсутствием."
		super().render()
