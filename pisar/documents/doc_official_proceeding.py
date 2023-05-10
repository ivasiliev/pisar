# ДОКУМЕНТ
# СЛУЖЕБНОЕ РАЗБИРАТЕЛЬСТВО по факту грубого дисциплинарного проступка
from classes.document_in_report import DocumentInReport
from classes.paragraph_settings import ParagraphSettings


class DocOfficialProceeding(DocumentInReport):
	def get_name(self):
		return "Служебное разбирательство по факту грубого дисциплинарного проступка"

	def get_name_for_file(self):
		return "Служебное_Разбирательство_ГДП_СОЧ.docx"

	def render(self):
		self.render_page_title()
		super().render()

	def render_page_title(self):
		bold_center_settings = ParagraphSettings()
		bold_center_settings.is_bold = True
		bold_center_settings.align_center = True

		align_right_settings = ParagraphSettings()
		align_right_settings.align_right = True

		self.add_empty_paragraphs(14)
		self.add_paragraph("СЛУЖЕБНОЕ РАЗБИРАТЕЛЬСТВО", bold_center_settings)
		self.add_empty_paragraphs(1)
		self.add_paragraph("по факту грубого дисциплинарного проступка", bold_center_settings)
		self.add_paragraph(
			"военнослужащим 2 стрелкового батальона войсковой части 42600 гвардии рядовым Ивановым Иваном Ивановичем",
			bold_center_settings)
		self.add_empty_paragraphs(18)
		self.add_paragraph("Начато «     » _________ 2023 г.", align_right_settings)
		self.add_paragraph("Окончено «     » _________ 2023 г.", align_right_settings)
