from classes.document_in_report import DocumentInReport


class DocQuestArrival(DocumentInReport):
	def get_name(self):
		return "Анкета прибывшего в зону СВО"

	def get_name_for_file(self):
		return f"{self.get_name()} ({self.get_soldier_info().full_name}).docx"

	def render(self):
		self.add_paragraph("Для служебного пользования", self.align_right_settings)



