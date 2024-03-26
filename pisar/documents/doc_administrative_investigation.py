# ДОКУМЕНТ
# АДМИНИСТРАТИВНОЕ РАССЛЕДОВАНИЕ по факту самовольного оставления части
from classes.pers_full_name_settings import PersFullNameSettings
from documents.investigation_prototype import InvestigationPrototype
from helpers.text_helper import capitalize_first_letter


class DocAdministrativeInvestigation(InvestigationPrototype):
	def get_name(self):
		return "Административное расследование по факту самовольного оставления части"

	def get_name_for_file(self):
		return f"Административное расследование_СОЧ ({self.get_soldier_info().full_name}).docx"

	def get_rank_name(self, declension_type):
		s_info = self.get_soldier_info()
		rank = self.get_person_rank(s_info.rank, declension_type)
		full_name = self.get_person_name_declension(self.get_person_name_short_format_1(s_info.full_name), declension_type)
		return f"{rank} {full_name}"

	def render(self, custom_margins=None):
		sold_str = self.get_rank_name(1)
		sold_str_2 = self.get_rank_name(2)

		self.doc_title = "АДМИНИСТРАТИВНОЕ РАССЛЕДОВАНИЕ"
		self.doc_about = "по факту самовольного оставления части"

		self.inventory_caption = "административного расследования"
		rows_content = [f"Медицинская характеристика на {sold_str}", f"Копия служебной карточки на {sold_str}", f"Служебная характеристика на {sold_str}", "Справка по форме ГУК МО РФ от 04.12.2006 г.", "Копия ведомости закрепления оружия 6 СР", "Копия именного списка для вечерних поверок 6 СР", f"Копия ведомости об ознакомлении со статьями УК РФ {sold_str}", f"Выписки из приказов командира войсковой части {self.get_military_unit()} на {sold_str}", f"Акт о невозможности дачи объяснений {sold_str_2}", f"Копия паспорта {sold_str}", "Заключение служебного разбирательства"]
		self.add_inventory_list(rows_content)

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

	def report1_page(self):
		self.add_paragraph(f"Командиру войсковой части {self.get_military_unit()}", self.align_right_settings)
		self.add_empty_paragraphs(2)
		self.add_paragraph("Рапорт", self.align_center_settings)
		self.add_empty_paragraphs(1)
		settings = PersFullNameSettings(0, False, False, True, False, False, False)
		sold_str = self.get_person_full_str(settings)
		date_str = self.get_date_format_1(self.get_date_of_event())
		self.add_paragraph(f"Настоящим докладываю, что {sold_str} отсутствовал на военной службе {date_str} на утренней поверке 6 стрелковой роты 2 стрелкового батальона, не уведомив при этом вышестоящее командование.", self.ident_align_justify_settings)
		settings = PersFullNameSettings(0, False, False, False, False, False, False, address_required=False)
		sold_str1 = capitalize_first_letter(self.get_person_full_str(settings))
		settings = PersFullNameSettings(1, False, False, False, False, False, False, address_required=False)
		sold_str2 = self.get_person_full_str(settings)
		self.add_paragraph(f"Мной была поставлена задача поисковой группе, которая провела поисковые мероприятия в окрестностях пункта временной дислокации 6 стрелковой роты, а также по адресу прописки, а именно: <АДРЕС ПРОПИСКИ>. {sold_str1} обнаружен не был. Мобильный телефон военнослужащего выключен. В ходе беседы с соседями {sold_str2} получили информацию, что данный военнослужащий по месту прописки не появлялся и где находится им не известно. ", self.ident_align_justify_settings)

		self.add_empty_paragraphs(3)
		self.officer_report_footer("commander_company")
