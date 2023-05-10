from docx import Document


class DocumentInReport:

	def __init__(self, data_model):
		self.data_model = data_model
		self.pages = []
		self.word_document = Document()
		pass

	def get_name(self):
		return ""

	def get_name_for_file(self):
		return ""

	# creates MS Word document
	def render(self):
		for page in self.pages:
			page.render(self.word_document)

	# performs mapping of a document structure and data
	def prepare(self):
		pass

	def add_paragraph(self, text):
		return self.word_document.add_paragraph(text)
