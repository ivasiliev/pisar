from docx.shared import Mm

from classes.document_in_report import DocumentInReport
from classes.paragraph_settings import ParagraphSettings


class DocOfficialProceedingOrder(DocumentInReport):
	def get_name(self):
		return "Приказ командира войсковой части"

	def get_name_for_file(self):
		return f"{self.get_name()} ({self.get_soldier_info().full_name}).docx"

	def render(self):
		s_info = self.get_soldier_info()
		rep_settings = self.get_report_settings()
		military_unit = rep_settings["military_unit"]
		date_of_event = self.get_date_format_1(rep_settings["date_of_event"])

		self.add_paragraph("Для служебного пользования", self.align_right_settings)

		paragraph_settings = ParagraphSettings()
		paragraph_settings.align_right = True
		paragraph_settings.right_indent = Mm(7.5)
		self.add_paragraph("Экз. №____", paragraph_settings)
		self.add_empty_paragraphs(1)

		self.add_paragraph("П Р И К А З", self.bold_title)
		self.add_paragraph(f"КОМАНДИРА ВОЙСКОВОЙ ЧАСТИ {military_unit}", self.bold_center_settings)
		self.add_paragraph("«___» _________ 2023 г.  № ___", self.align_center_settings)
		self.add_paragraph("г. Донецк", self.align_center_settings)
		self.add_empty_paragraphs(1)

		self.add_paragraph("По факту грубого дисциплинарного проступка", self.bold_center_settings)
		paragraph_settings = ParagraphSettings()
		paragraph_settings.is_bold = True
		paragraph_settings.is_underline = True
		paragraph_settings.align_center = True

		# TODO this can be in base class
		rnk = self.get_person_rank(s_info.rank, 2)
		nm = self.get_person_name_declension(s_info.full_name, 2)
		self.add_paragraph(f"{rnk} {nm}", paragraph_settings)
		self.add_empty_paragraphs(2)

		# TODO set line spacing = 0.95
		txt = f"Несмотря на меры, принимаемые командованием войсковой части {military_unit} по профилактике нарушения воинской дисциплины, направленные на укрепление правопорядка, сплочения воинских коллективов, создания в них здоровой морально–психологической обстановки, способствующих успешному выполнению поставленных задач, проведение профилактической работы по недопущению подобных случаев, среди военнослужащих продолжает иметь место случаи уклонения от исполнения обязанностей военной службы."
		self.add_paragraph(txt, self.ident_align_justify_settings)

		sold_str = self.get_person_full_str(0, False, False, True, False, True, False)
		txt = f"{date_of_event} {sold_str} самовольно покинул расположение части не уведомив вышестоящее командование."
		self.add_paragraph(txt, self.ident_align_justify_settings)

		rnk = self.get_person_rank(s_info.rank, 1)
		nm = self.get_person_name_declension(s_info.full_name, 1)
		txt = f"Проведенные розыскные мероприятия, опрос сослуживцев, поиск в лечебных учреждениях, военных комендатурах, а также отделениях полиции {rnk} {nm} результата не дали, установить причины отсутствия военнослужащего, а также его местонахождение не удалось."
		self.add_paragraph(txt, self.ident_align_justify_settings)

		self.add_paragraph("Причинами данного правонарушения явились:", self.ident_align_justify_settings)

		txt = "невыполнение требований статьи 144, 145 Устава Внутренней Службы Вооруженных Сил Российской Федерации в " \
		      "части, касающейся воспитания, поддержания воинской дисциплины, морально-психологического состояния " \
		      "личного состава в роте, а также в части касающееся знаний деловых "

		commander_company_text = self.get_commander_company_full_str(2)
		txt = txt + f"и морально-психологических качеств и особенностей всех военнослужащих роты, постоянного " \
		            f"проведения с ними индивидуальной работы по воинскому воспитанию {commander_company_text};"

		self.add_paragraph(txt, self.ident_align_justify_settings)

		sold_str = self.get_person_full_str(1, False, False, True, False, True, False)
		txt = f"невыполнение требований статьи 160, 161 Устава Внутренней Службы Вооруженных Сил Российской Федерации в части, касающейся точного и своевременного исполнения возложенных на него обязанностей, поставленных задач и личная недисциплинированность {sold_str}."
		self.add_paragraph(txt, self.ident_align_justify_settings)

		rnk = self.get_person_rank(s_info.rank, 0)
		nm = self.get_person_name_declension(s_info.full_name, 0)
		p1 = self.add_paragraph(
			f"Исходя из материала служебного разбирательства следует, что {rnk} {nm} "
			"самовольно покинул расположение части, за что в соответствии со статьей «337» "
			"Уголовного кодекса Российской Федерации предусматривается уголовная ответственность, "
			"на основании вышеизложенного ", self.ident_align_justify_settings)
		runner = p1.add_run("ПРИКАЗЫВАЮ:")
		runner.bold = True

		commander_company_text = self.get_commander_company_full_str(3)
		txt = "за невыполнение требований статьи 144, 145 Устава Внутренней Службы Вооруженных Сил Российской " \
		       "Федерации в части, касающейся воспитания, поддержания воинской дисциплины, морально–психологического " \
		       "состояния личного состава в роте, а также в части касающееся знаний деловых и морально–психологических " \
		       "качеств и особенностей всех военнослужащих роты, постоянного проведения с ними индивидуальной работы " \
		       "по воинскому воспитанию, строго указать на УПУЩЕНИЕ ПО СЛУЖБЕ."
		self.add_paragraph(f"1. {commander_company_text} {txt}", self.ident_align_justify_settings)

		sold_str = self.get_person_full_str(3, False, False, True, False, True, False)
		txt = f"2. {sold_str} за грубый дисциплинарный проступок самовольное оставление части более 4 (четырех) часов, объявить СТРОГИЙ ВЫГОВОР."
		self.add_paragraph(txt, self.ident_align_justify_settings)
		self.add_empty_paragraphs(1)

		# TODO this code is SIMILAR in Performance_Characteristics

		line_spacing = 0.96
		par_set_center = ParagraphSettings()
		par_set_center.is_bold = True
		par_set_center.align_center = True
		par_set_center.line_spacing = line_spacing

		par_set_right = ParagraphSettings()
		par_set_right.align_right = True
		par_set_right.is_bold = True
		par_set_right.line_spacing = line_spacing

		self.add_commander(rep_settings["commander_4_level"], military_unit, par_set_center, par_set_right)
		self.add_empty_paragraphs(2)
		self.add_commander(rep_settings["commander_3_level"], military_unit, par_set_center, par_set_right)

		super().render()

	def add_commander(self, commander_info, military_unit, par_set_center, par_set_right):
		c_name = self.get_person_name_short_format_1(commander_info["name"])
		c_rank = commander_info["rank"]
		if self.get_report_settings()["is_guard"]:
			c_rank = "гвардии " + c_rank
		c_position = commander_info["position"] + " " + military_unit
		self.add_paragraph(c_position.upper(), self.bold_center_settings)
		self.add_paragraph(c_rank, par_set_center)
		self.add_paragraph(c_name, par_set_right)
