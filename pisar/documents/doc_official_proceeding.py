# ДОКУМЕНТ
# СЛУЖЕБНОЕ РАЗБИРАТЕЛЬСТВО по факту грубого дисциплинарного проступка
from classes.pers_full_name_settings import PersFullNameSettings
from documents.investigation_prototype import InvestigationPrototype


class DocOfficialProceeding(InvestigationPrototype):
	def get_name(self):
		return "Служебное разбирательство по факту грубого дисциплинарного проступка"

	def get_name_for_file(self):
		return f"Служебное_Разбирательство_ГДП ({self.get_soldier_info().full_name}).docx"

	def render(self, custom_margins=None):
		self.doc_title = "СЛУЖЕБНОЕ РАЗБИРАТЕЛЬСТВО"
		self.doc_about = "По факту грубого дисциплинарного проступка, совершенного"

		self.inventory_caption = "служебного разбирательства"
		si = f"{self.get_person_rank(self.get_soldier_info().rank, 2)} {self.get_person_name_declension(self.get_person_name_short_format_1(self.get_soldier_info().full_name), 2)}"
		rows_content = ["Протокол о грубом дисциплинарном проступке", f"Акт о невозможности дачи объяснений {si}", "Служебная характеристика", "Справка по форме ГУК МО РФ от 04.12.2006 г.", "Заключение служебного разбирательства"]
		self.add_inventory_list(rows_content)

		self.report1_action = "отсутствовал на месте несения службы более 4 (четырех) часов, служебные обязанности не выполняет"
		self.report1_request = ""  # "проведение служебного разбирательства по данному факту"

		self.report3_conclusion = "отсутствует на службе без уважительных причин, не уведомив об этом вышестоящее командование"

		self.conclusion_materials = "служебного разбирательства"
		self.conclusion_fact = "грубого дисциплинарного проступка"
		self.conclusion_action_performed = "служебное разбирательство по факту грубого дисциплинарного проступка, совершенного"
		self.conclusion_p2_action = "отсутствовал в месте несения военной службы без уважительных причин более 4 (четырех) часов подряд в течение установленного ежедневного служебного времени, тем самым совершил грубый дисциплинарный проступок"
		self.conclusion_punishment = "отсутствовал в месте несения военной службы без уважительных причин более 4 (четырех) часов подряд в течение установленного ежедневного служебного времени, что в соответствии с Приложением 7 к Дисциплинарному уставу Вооруженных Сил Российской Федерации является грубым дисциплинарным проступком"

		settings = PersFullNameSettings(3, False, False, True, False, True, False)
		sold_str = self.get_person_full_str(settings)
		if len(sold_str) > 2:
			sold_str = sold_str[0].upper() + sold_str[1:]
		txt = f"4. {sold_str} за грубый дисциплинарный проступок, отсутствие на месте несения службы без уважительных причин более 4 (четырех) часов подряд в течение установленного ежедневного служебного времени, объявить СТРОГИЙ ВЫГОВОР."
		self.conclusion_punishment_points.append(txt)

		super().render()

