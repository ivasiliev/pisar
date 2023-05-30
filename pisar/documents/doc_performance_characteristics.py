# ДОКУМЕНТ
# СЛУЖЕБНАЯ ХАРАКТЕРИСТИКА
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Mm
from docx.shared import Pt

from classes.document_in_report import DocumentInReport
from classes.paragraph_settings import ParagraphSettings


class DocPerformanceCharacteristics(DocumentInReport):
	def get_name(self):
		return "Служебная характеристика"

	def get_name_for_file(self):
		return f"Служебная характеристика ({self.get_soldier_info().full_name}).docx"

	def render(self):
		rep_settings = self.get_report_settings()
		line_spacing = 0.96

		# TODO font 16
		paragraph_settings = self.bold_center_settings
		paragraph_settings.font_size = 16

		p_title = self.add_paragraph("СЛУЖЕБНАЯ ХАРАКТЕРИСТИКА", paragraph_settings)
		p_title.paragraph_format.space_after = Pt(10)

		paragraph_settings = ParagraphSettings()
		paragraph_settings.left_indent = Mm(65)
		paragraph_settings.align_justify = True
		paragraph_settings.line_spacing = line_spacing
		sold_str = self.get_person_full_str(1, False, False, True, True)
		nationality = self.get_word_gent(rep_settings["nationality"])
		education = rep_settings["education"]
		yss = rep_settings["year_service_started"]
		txt = f"на {sold_str}, {nationality}, образование {education}, в ВС ДНР с {yss} года."
		self.add_paragraph(txt, paragraph_settings)

		self.add_empty_paragraphs_spacing(2, line_spacing)

		sold_str = self.get_person_full_str(1, False, False, True, False)
		txt = f"За время прохождения службы в должности {sold_str}, проявил себя неоднозначно, как военнослужащий, требующий контроля со стороны командования при исполнении поставленных задач."
		paragraph_settings = self.ident_align_justify_settings
		paragraph_settings.line_spacing = line_spacing
		self.add_paragraph(txt, self.ident_align_justify_settings)

		txt = "По предметам боевой подготовки показал удовлетворительные знания. При несении службы показал себя как " \
		      "не самый дисциплинированный военнослужащий. Ранее был несколько раз уличён в нежелании грамотно, " \
		      "четко, а также своевременно выполнять поставленные задачи. Однако стоит отметить, что подобное " \
		      "происходило не на постоянной основе, хоть и является закономерностью."
		self.add_paragraph(txt, paragraph_settings)

		txt = "Данный военнослужащий, пользуется средним авторитетом среди сослуживцев и командования, служебные " \
		      "отношения средние. С начальством не пререкается, однако на замечания реагирует не всегда, что при этом " \
		      "приводит к неправильным выводам."
		self.add_paragraph(txt, paragraph_settings)

		txt = "На практике полученные знания применить не старается. На здоровье жалоб не было, физически развит " \
		      "удовлетворительно, имеет высокую работоспособность. Трудности военной службы переносит терпимо. В " \
		      "полном объеме владеет профессиональными знаниями, но овладеть новыми знаниями не стремится."
		self.add_paragraph(txt, paragraph_settings)

		self.add_empty_paragraphs_spacing(1, line_spacing)

		s_info = self.get_soldier_info()
		commander_company_info = s_info.company_commander
		c_name = "[ФИО РОТНОГО КОМАНДИРА]"
		c_rank = "[ЗВАНИЕ РОТНОГО КОМАНДИРА]"
		c_position = "[ДОЛЖНОСТЬ РОТНОГО КОМАНДИРА]"
		if len(commander_company_info) > 0:
			c_name = self.get_person_name_short_format_1(commander_company_info["name"])
			c_rank = commander_company_info["rank"]
			if rep_settings["is_guard"]:
				c_rank = "гвардии " + c_rank
			c_position = commander_company_info["position"]

		par_set_bold = self.bold_center_settings
		par_set_bold.line_spacing = line_spacing
		par_set_right = self.bold_right_settings
		par_set_right.line_spacing = line_spacing
		self.add_paragraph(c_position.upper(), par_set_bold)
		self.add_paragraph(c_rank, par_set_bold)
		self.add_paragraph(c_name, par_set_right)
		self.add_empty_paragraphs_spacing(1, line_spacing)

		self.add_commander(rep_settings["commander_2_level"], par_set_bold, par_set_right)
		self.add_empty_paragraphs_spacing(1, line_spacing)

		self.add_paragraph("С характеристикой ознакомлен, согласен:", self.align_justify_settings)
		self.add_empty_paragraphs_spacing(1, line_spacing)

		comm3 = rep_settings["commander_3_level"]
		comm3_pos = comm3["position"]
		comm3_pos = comm3_pos + " " + rep_settings["military_unit"]
		comm3["position"] = comm3_pos
		self.add_commander(comm3, par_set_bold, par_set_right)
		self.add_empty_paragraphs_spacing(1, line_spacing)

		self.add_paragraph("«___» _________ 2023 г.", self.bold_justify_settings)

		super().render()

	def add_commander(self, commander_info, par_set_bold, par_set_right):
		c_name = self.get_person_name_short_format_1(commander_info["name"])
		c_rank = commander_info["rank"]
		if self.get_report_settings()["is_guard"]:
			c_rank = "гвардии " + c_rank
		c_position = commander_info["position"]
		self.add_paragraph(c_position.upper(), self.bold_center_settings)
		self.add_paragraph(c_rank, self.bold_center_settings)
		self.add_paragraph(c_name, self.bold_right_settings)
