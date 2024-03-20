# ДОКУМЕНТ
# АДМИНИСТРАТИВНОЕ РАССЛЕДОВАНИЕ по факту самовольного оставления части
from classes.pers_full_name_settings import PersFullNameSettings
from documents.investigation_prototype import InvestigationPrototype


class DocAdministrativeInvestigation(InvestigationPrototype):
	def get_name(self):
		return "Административное расследование по факту самовольного оставления части"

	def get_name_for_file(self):
		return f"Административное расследование_СОЧ ({self.get_soldier_info().full_name}).docx"

	def render(self, custom_margins=None):
		self.doc_title = "АДМИНИСТРАТИВНОЕ РАССЛЕДОВАНИЕ"
		self.doc_about = "по факту самовольного оставления части"

		self.inventory_caption = "административного расследования"
		rows_content = ["Служебная характеристика", "Справка по форме ГУК МО РФ от 04.12.2006 г.", f"Письмо командования в/ч {self.get_military_unit()} родителям", "Ориентировка", "Копия паспорта", "Копия служебной карточки", "Заключение административного расследования"]
		self.add_inventory_list(rows_content)

		self.report1_action = "самовольно покинул расположение части, не уведомив вышестоящее командование"
		self.report1_request = "проведение административного расследования по данному факту"

		self.report3_conclusion = "самовольно покинул расположение части, не уведомив вышестоящее командование"

		self.conclusion_p2_letter_to_parents = True
		self.conclusion_materials = "административного расследования"
		self.conclusion_fact = "самовольного оставления части"
		self.conclusion_action_performed = "административное расследование по факту самовольного оставления части"
		self.conclusion_p2_action = "самовольно покинул расположение части, не уведомив вышестоящее командование"

		self.conclusion_punishment = "самовольно покинул расположение части, за что в соответствии со статьей «337» Уголовного кодекса Российской Федерации предусматривается уголовная ответственность"

		settings = PersFullNameSettings(2, False, False, True, False, True, False)
		sold_str = self.get_person_full_str(settings)
		txt = f"3. Передать материалы административного расследования по факту самовольного оставления части {sold_str} в военную прокуратуру г.Донецка для дальнейшего принятия процессуального решения."
		self.conclusion_punishment_points.append(txt)

		settings = PersFullNameSettings(1, False, False, True, False, True, False)
		sold_str = self.get_person_full_str(settings)
		if len(sold_str) > 2:
			sold_str = sold_str[0].upper() + sold_str[1:]
		date_formatted = self.get_date_format_1(self.get_date_of_event())
		txt = f"4. {sold_str} снять с котлового довольствия с {date_formatted}."
		self.conclusion_punishment_points.append(txt)

		txt = f"5. {sold_str} снять с финансового обеспечения с {date_formatted}."
		self.conclusion_punishment_points.append(txt)

		super().render()
