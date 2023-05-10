from docx import Document
from docx.shared import Mm
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

from classes.paragraph_settings import ParagraphSettings


class DocumentInReport:

	def __init__(self, data_model):
		self.data_model = data_model
		self.pages = []
		self.word_document = Document()
		style = self.word_document.styles['Normal']
		font = style.font
		font.name = 'Times New Roman'
		font.size = Pt(14)

	def get_name(self):
		return ""

	def get_name_for_file(self):
		return ""

	# creates MS Word document
	def render(self):
		# for page in self.pages:
		# 	page.render(self.word_document)
		self.apply_default_settings()

	# performs mapping of a document structure and data
	def prepare(self):
		pass

	def add_paragraph_simple(self, text):
		return self.add_paragraph(text, None)

	def add_paragraph(self, text, paragraph_settings):
		if paragraph_settings is None:
			paragraph_settings = ParagraphSettings()
		if paragraph_settings.has_markup():
			p = self.word_document.add_paragraph()
			runner = p.add_run(text)
			if paragraph_settings.is_bold:
				runner.bold = True

		else:
			p = self.word_document.add_paragraph(text)

		# TODO use style
		pf = p.paragraph_format
		pf.left_indent = Pt(0)
		pf.right_indent = Pt(0)
		pf.space_before = Pt(0)
		pf.space_after = Pt(0)

		# TODO figure out how to use it properly
		if paragraph_settings.align_left:
			p.alignment = 0
		if paragraph_settings.align_center:
			p.alignment = 1
		if paragraph_settings.align_right:
			p.alignment = 2

		# p.style = self.word_document.styles['Normal']
		# run = p.add_run()
		# fnt = run.font
		# fnt.bold = True
		# fnt.name = 'Calibri'  #'Times New Roman'
		# fnt.size = Pt(14)

		return p

	def add_empty_paragraphs(self, how_many_rows):
		num_row = 1
		while num_row <= how_many_rows:
			self.add_paragraph_simple("")
			num_row = num_row + 1

	def apply_default_settings(self):
		sections = self.word_document.sections
		for section in sections:
			section.top_margin = Mm(20)
			section.bottom_margin = Mm(20)  # TODO: 15 mm in original document
			section.left_margin = Mm(30)
			section.right_margin = Mm(10)
			# settings for page as A4
			section.page_height = Mm(297)
			section.page_width = Mm(210)
			section.header_distance = Mm(12.7)
			section.footer_distance = Mm(12.7)
