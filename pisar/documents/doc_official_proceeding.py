# ДОКУМЕНТ
# СЛУЖЕБНОЕ РАЗБИРАТЕЛЬСТВО по факту грубого дисциплинарного проступка
from classes.document_in_report import DocumentInReport


class DocOfficialProceeding(DocumentInReport):
	def get_name(self):
		return "Служебное разбирательство по факту грубого дисциплинарного проступка"

	def get_name_for_file(self):
		return "Служебное_Разбирательство_ГДП_СОЧ.docx"

	def render(self):
		self.render_page_title()

	def render_page_title(self):
		num_row = 1
		while num_row <= 16:
			self.add_paragraph("")
			num_row = num_row + 1
		self.add_paragraph("СЛУЖЕБНОЕ РАЗБИРАТЕЛЬСТВО")


