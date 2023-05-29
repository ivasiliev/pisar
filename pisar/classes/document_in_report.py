import os

from docx import Document
from docx.shared import Mm
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from pytrovich.enums import NamePart, Gender, Case

from classes.paragraph_settings import ParagraphSettings
from classes.personnel_storage import PersonnelStorage

MODEL_PERSONNEL_PATH = "personnel_path"
MODEL_OUTPUT_FOLDER = "output_folder"
MODEL_PERSONS = "persons"
MODEL_MORPHOLOGY = "morphology"
MODEL_JSON_OBJECT = "json_settings"
# TODO set a better name
MODEL_NAME_MORPHOLOGY = "petrovich"
MODEL_IS_VALID = "is_valid"
MODEL_CURRENT_SOLDIER = "current_soldier"


class DocumentInReport:

	def __init__(self, data_model):
		self.data_model = data_model
		self.pages = []
		self.word_document = Document()
		style = self.word_document.styles['Normal']
		font = style.font
		font.name = 'Times New Roman'
		font.size = Pt(14)
		# predefined styles
		self.bold_center_settings = ParagraphSettings()
		self.bold_center_settings.is_bold = True
		self.bold_center_settings.align_center = True

		self.align_left_settings = ParagraphSettings()
		self.align_left_settings.align_left = True

		self.align_right_settings = ParagraphSettings()
		self.align_right_settings.align_right = True

		self.align_center_settings = ParagraphSettings()
		self.align_center_settings.align_center = True

		self.align_justify_settings = ParagraphSettings()
		self.align_justify_settings.align_justify = True

		self.ident_align_justify_settings = ParagraphSettings()
		self.ident_align_justify_settings.align_justify = True
		self.ident_align_justify_settings.first_line_indent = Mm(12.5)

		self.personnel_info = None
		if self.data_model is not None and self.data_model[MODEL_PERSONNEL_PATH] is not None:
			self.personnel_info = PersonnelStorage(self.data_model[MODEL_PERSONNEL_PATH])

	def get_name(self):
		return ""

	def get_name_for_file(self):
		return ""

	# creates MS Word document
	def render(self):
		self.apply_default_settings()
		if self.data_model is not None and self.data_model[MODEL_OUTPUT_FOLDER]:
			full_path_folder = self.data_model[MODEL_OUTPUT_FOLDER]
			if not os.path.exists(full_path_folder):
				os.makedirs(full_path_folder)
			full_path = os.path.join(full_path_folder, self.get_name_for_file())
			self.word_document.save(full_path)
			print(f"Создан документ {full_path}.")

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

		if paragraph_settings.align_left:
			p.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
		if paragraph_settings.align_center:
			p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
		if paragraph_settings.align_right:
			p.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
		if paragraph_settings.align_justify:
			p.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY

		if paragraph_settings.first_line_indent > 0:
			pf.first_line_indent = paragraph_settings.first_line_indent

		if paragraph_settings.left_indent > 0:
			pf.left_indent = paragraph_settings.left_indent

		if paragraph_settings.right_indent > 0:
			pf.right_indent = paragraph_settings.right_indent

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
			section.bottom_margin = Mm(20)  # 15 mm in original document
			section.left_margin = Mm(30)
			section.right_margin = Mm(10)
			# settings for page as A4
			section.page_height = Mm(297)
			section.page_width = Mm(210)
			section.header_distance = Mm(12.7)
			section.footer_distance = Mm(12.7)

	def set_column_width(self, table, index, size):
		for cell in table.columns[index].cells:
			cell.width = Mm(size)

	def add_table(self, row_count, captions, rows_data):
		table = self.word_document.add_table(rows=row_count, cols=len(captions))
		table.style = 'Table Grid'
		table.allow_autofit = False
		table.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
		# TODO set columns width
		# TODO put table in the center and set margins 0;0
		# process header
		hdr_cells = table.rows[0].cells
		num_column = 0
		for caption in captions:
			hdr_cells[num_column].text = caption
			num_column = num_column + 1

		# set column width
		self.set_column_width(table, 0, 10)
		self.set_column_width(table, 1, 140)
		self.set_column_width(table, 2, 20)

		# process rows
		num_row = 1
		for row in rows_data:
			cells = table.rows[num_row].cells
			cells[0].text = str(num_row)
			cells[1].text = row
			cells[2].text = ""
			num_row = num_row + 1

	def add_paragraph_left_right(self, left_text, right_text):
		table = self.word_document.add_table(rows=1, cols=2)
		table.alignment = WD_TABLE_ALIGNMENT.CENTER
		cells = table.rows[0].cells
		p0 = cells[0].add_paragraph(left_text)
		p0.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
		p1 = cells[1].add_paragraph(right_text)
		p1.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT

	def get_soldier_info(self):
		return self.data_model[MODEL_CURRENT_SOLDIER]

	def get_report_settings(self):
		return self.data_model[MODEL_JSON_OBJECT]

	def get_person_name_routines(self, full_name, cs):
		maker = self.data_model[MODEL_NAME_MORPHOLOGY]
		if maker is None:
			print("Внутренняя ошибка. Морфоанализатор для имён не создан.")
			return ""

		name_tokens = full_name.split(" ")
		surname = name_tokens[0]
		first_name = name_tokens[1]
		middle_name = ""
		if len(name_tokens) > 2:
			middle_name = name_tokens[2]

		sn = maker.make(NamePart.FIRSTNAME, Gender.MALE, cs, surname)
		fn = maker.make(NamePart.FIRSTNAME, Gender.MALE, cs, first_name)
		mn = maker.make(NamePart.MIDDLENAME, Gender.MALE, cs, middle_name)

		return f"{sn} {fn} {mn}".strip()

	def get_person_name_gent(self, full_name):
		return self.get_person_name_routines(full_name, Case.GENITIVE)

	def get_person_name_instr(self, full_name):
		return self.get_person_name_routines(full_name, Case.INSTRUMENTAL)

	def get_person_name_datv(self, full_name):
		return self.get_person_name_routines(full_name, Case.DATIVE)

	def get_person_name_declension(self, full_name, declension_type):
		if declension_type == 1:
			result = self.get_person_name_gent(full_name)
		else:
			if declension_type == 2:
				result = self.get_person_name_instr(full_name)
			else:
				if declension_type == 3:
					result = self.get_person_name_datv(full_name)
				else:
					result = full_name

		return result

	def get_word_gent(self, wrd):
		return self.get_word_routines(wrd, "gent")

	def get_word_ablt(self, wrd):
		return self.get_word_routines(wrd, "ablt")

	def get_word_datv(self, wrd):
		return self.get_word_routines(wrd, "datv")

	def get_word_declension(self, wrd, declension_type):
		if declension_type == 1:
			result = self.get_word_gent(wrd)
		else:
			if declension_type == 2:
				result = self.get_word_ablt(wrd)
			else:
				if declension_type == 3:
					result = self.get_word_datv(wrd)
				else:
					result = wrd

		return result

	def get_word_routines(self, wrd, grm):
		morph = self.data_model[MODEL_MORPHOLOGY]
		if morph is None:
			print("Внутренняя ошибка. Морфоанализатор не создан.")
			return ""
		parsed = morph.parse(wrd)[0]
		gent_text = parsed.inflect({grm})
		return gent_text.word

	# format = Петров Алексей Сергеевич -> А. Петров
	def get_person_name_short_format_1(self, full_name):
		name_tokens = full_name.split(" ")
		if len(name_tokens) < 2:
			print(f"Не удалось преобразовать в нужный формат: {full_name}")
		surname = name_tokens[0]
		first_name = name_tokens[1]
		return f"{first_name[0]}. {surname}"

	# format = 16-04-2023/16.04.2023 -> 16 апреля 2023 года
	def get_date_format_1(self, date_str):
		tokens = date_str.split("-")
		if len(tokens) < 3:
			tokens = date_str.split(".")
		if len(tokens) != 3:
			print(f"Не удалось определить формат даты {date_str}")
		months = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"]
		d = int(tokens[0])
		m = int(tokens[1])
		y = int(tokens[2])
		return f"{d} {months[m-1]} {y} года"

