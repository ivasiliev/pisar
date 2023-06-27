# ДОКУМЕНТ
# СЛУЖЕБНОЕ РАЗБИРАТЕЛЬСТВО по факту грубого дисциплинарного проступка
from classes.pers_full_name_settings import PersFullNameSettings
from documents.investigation_prototype import InvestigationPrototype


class DocOfficialProceeding(InvestigationPrototype):
	def get_name(self):
		return "Служебное разбирательство по факту грубого дисциплинарного проступка"

	def get_name_for_file(self):
		return f"Служебное_Разбирательство_ГДП ({self.get_soldier_info().full_name}).docx"

	def render(self):
		self.doc_title = "СЛУЖЕБНОЕ РАЗБИРАТЕЛЬСТВО"
		self.doc_about = "по факту грубого дисциплинарного проступка"

		self.inventory_caption = "служебного разбирательства"
		self.inventory_list.append("Протокол о грубом дисциплинарном проступке")
		self.inventory_list.append("Акт о невозможности получения копии протокола о грубом дисциплинарном проступке")
		self.inventory_list.append("Акт о невозможности взять объяснение по факту действий совершенных военнослужащим, в которых усматривается преступление против военной службы")
		self.inventory_list.append("Служебная характеристика")
		self.inventory_list.append("Заключение служебного разбирательства")

		self.report1_action = "отсутствовал на месте несения службы более 4 (четырех) часов, служебные обязанности не выполняет"
		self.report1_request = "проведение служебного разбирательства по данному факту"

		self.report3_conclusion = "отсутствует на службе без уважительных причин, не уведомив об этом вышестоящее командование"

		self.conclusion_materials = "служебного разбирательства"
		self.conclusion_fact = "грубого дисциплинарного проступка"
		self.conclusion_action_performed = "служебное разбирательство по факту грубого дисциплинарного проступка"
		self.conclusion_p2_action = "отсутствовал в месте несения военной службы без уважительных причин более 4 (четырех) часов подряд в течение установленного ежедневного служебного времени, тем самым совершил грубый дисциплинарный проступок"
		self.conclusion_punishment = "отсутствовал в месте несения военной службы без уважительных причин более 4 (четырех) часов подряд в течение установленного ежедневного служебного времени, что в соответствии с Приложением 7 к Дисциплинарному уставу Вооруженных Сил Российской Федерации является грубым дисциплинарным проступком"

		settings = PersFullNameSettings(1, False, False, True, False, True, False)
		sold_str = self.get_person_full_str(settings)
		if len(sold_str) > 2:
			sold_str = sold_str[0].upper() + sold_str[1:]
		txt = f"3. {sold_str} за грубый дисциплинарный проступок самовольное оставление места несения службы более 4 (четырех) часов, ПРЕДУПРЕДИТЬ О НЕПОЛНОМ СЛУЖЕБНОМ СООТВЕТСТВИИ."
		self.conclusion_punishment_points.append(txt)

		super().render()

