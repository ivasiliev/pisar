# ДОКУМЕНТ
# СЛУЖЕБНАЯ ХАРАКТЕРИСТИКА
from docx.shared import Mm

from classes.document_in_report import DocumentInReport
from classes.paragraph_settings import ParagraphSettings


class DocPerformanceCharacteristics(DocumentInReport):
	def get_name(self):
		return "Служебная характеристика"

	def get_name_for_file(self):
		return "Служебная характеристика.docx"

	def render(self):
		self.add_paragraph("СЛУЖЕБНАЯ ХАРАКТЕРИСТИКА", self.bold_center_settings)
		paragraph_settings = ParagraphSettings()
		paragraph_settings.left_indent = Mm(60)
		self.add_paragraph(
			"на пулеметчика 3 стрелкового отделения 3 стрелкового взвода 5 стрелковой роты2 стрелкового батальона войсковой части 42600  гвардии рядового Иванова Ивана Иванович 26 июня 1997 года рождения, русского, образование среднее, в ВС ДНР с 2022 года.",
			paragraph_settings)
		self.add_empty_paragraphs(2)
		
