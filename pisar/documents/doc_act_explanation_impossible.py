from documents.act_prototype import ActPrototype, ACT_TITLE, ACT_TEXT


class DocActExplanationImpossible(ActPrototype):
	def get_name(self):
		return "Акт о невозможности взять объяснения по факту ГДП"

	def get_name_for_file(self):
		return f"{self.get_name()} ({self.get_soldier_info().full_name}).docx"

	def render(self):
		self.data_model[ACT_TITLE] = "о невозможности взять объяснения по факту действий совершенных военнослужащим, " \
		                             "в которых усматривается преступления против военной службы."
		sold_str = self.get_person_full_str(0, False, False, True, False, False, False)
		self.data_model[ACT_TEXT] = f"Мы, нижеподписавшиеся, составили настоящий акт о том, что {sold_str} не может дать объяснения и не подписал составленный протокол о грубом дисциплинарном проступке, а также не получил копию по причине своего отсутствия."
		super().render()
