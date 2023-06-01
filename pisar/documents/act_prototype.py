from docx.shared import Mm

from classes.document_in_report import DocumentInReport
from classes.paragraph_settings import ParagraphSettings

ACT_TITLE = "act_title"
ACT_TEXT = "act_text"


# base class for Acts. Don't use it directly.
class ActPrototype(DocumentInReport):
	def render(self):
		rep_settings = self.get_report_settings()

		paragraph_settings = ParagraphSettings()
		paragraph_settings.left_indent = Mm(115)
		paragraph_settings.is_bold = True
		self.add_paragraph("УТВЕРЖДАЮ", paragraph_settings)
		self.add_paragraph(f"Командир войсковой части {rep_settings['military_unit']}", self.bold_right_settings)

		paragraph_settings = ParagraphSettings()
		paragraph_settings.right_indent = Mm(31)
		paragraph_settings.align_right = True
		paragraph_settings.is_bold = True
		comm_3 = rep_settings["commander_3_level"]
		self.add_paragraph(self.get_person_rank(comm_3["rank"], 0), paragraph_settings)
		self.add_paragraph(self.get_person_name_short_format_1(comm_3["name"]), self.bold_right_settings)
		self.add_empty_paragraphs(1)
		self.add_paragraph("«___»____________2023 г.", self.bold_right_settings)
		self.add_empty_paragraphs(3)
		self.add_paragraph("АКТ", self.bold_center_settings)
		self.add_paragraph(self.data_model[ACT_TITLE], self.bold_center_settings)
		self.add_empty_paragraphs(1)

		self.add_paragraph(self.data_model[ACT_TEXT], self.ident_align_justify_settings)
		self.add_empty_paragraphs(2)
		self.add_paragraph("«___»____________2023 г.", self.align_left_settings)
		self.add_empty_paragraphs(2)

		self.print_commander(rep_settings["commander_2_level"])
		self.add_empty_paragraphs(2)
		self.print_commander(rep_settings["commander_1_level"])
		self.add_empty_paragraphs(1)

		comm_company = self.get_commander_company()
		self.print_commander_routines(comm_company["name"], comm_company["rank"], comm_company["position"])

		super().render()

	def print_commander(self, comm):
		self.print_commander_routines(self.get_person_name_short_format_1(comm["name"]),
		                              self.get_person_rank(comm["rank"], 0), comm["position"])

	def print_commander_routines(self, c_name, c_rank, c_position):
		self.add_paragraph(c_position, self.align_center_settings)
		self.add_paragraph(c_rank, self.align_center_settings)
		self.add_paragraph(c_name, self.align_right_settings)
