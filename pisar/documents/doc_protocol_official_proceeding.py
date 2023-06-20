from classes.document_in_report import DocumentInReport


class DocProtocolOfficialProceeding(DocumentInReport):
	def get_name(self):
		return "Протокол по факту грубого дисциплинарного проступка"

	def get_name_for_file(self):
		return f"Протокол ГДП ({self.get_soldier_info().full_name}).docx"

	def render(self):
		self.add_paragraph("ПРОТОКОЛ", self.bold_center_settings)
		self.add_paragraph("О ГРУБОМ ДИСЦИПЛИНАРНОМ ПРОСТУПКЕ", self.bold_center_settings)
		runs = self.add_paragraph_left_right("«     » _________ 2023 г.", "населенный пункт г.Донецк")
		runs[1].underline = True


		super().render()
