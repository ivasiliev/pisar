from classes.document_in_report import DocumentInReport


class DocActExplanationImpossible(DocumentInReport):
	def get_name(self):
		return "Акт о невозможности взять объяснения по факту ГДП"

	def get_name_for_file(self):
		return f"{self.get_name()} ({self.get_soldier_info().full_name}).docx"

	def render(self):
		s_info = self.get_soldier_info()
		rep_settings = self.get_report_settings()

