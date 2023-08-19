from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Pt

from classes.document_in_report import DocumentInReport
from classes.paragraph_settings import ParagraphSettings
from classes.personnel_storage import EXCEL_DOCUMENT_LS


class DocDiaryViolationDiscipline(DocumentInReport):
	def get_name(self):
		return "Нарушение воинской дисциплины"

	def get_name_for_file(self):
		return f"{self.get_name()}.docx"

	def render(self):
		f_12_left = ParagraphSettings()
		f_12_left.align_left = True
		f_12_left.font_size = Pt(12)

		f_caption = ParagraphSettings()
		f_caption.font_size = Pt(10)

		self.add_paragraph("3) Учет грубых нарушений воинской дисциплины", f_12_left)
		table_settings = {"cols_width": None, "ps": f_caption, "alignment": WD_PARAGRAPH_ALIGNMENT.LEFT,
		                  "font_size": Pt(10)}
		row_data = []
		pers_storage = self.get_pers_storage()
		all_persons = pers_storage.get_all_persons(EXCEL_DOCUMENT_LS)
		for pers in all_persons:
			pass

		captions = ["Воинское звание, фамилия, имя, отчество", "Дата совершения, вид грубого дисциплинарного проступка", "Характер проступка, причины и обстоятельства", "Принятые меры"]
		self.add_table(captions, row_data, table_settings)
		self.word_document.add_page_break()

		super().render()