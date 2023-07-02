from documents.doc_administrative_investigation_order import DocAdministrativeInvestigationOrder


class DocAdministrativeInvestigationOrderCopy(DocAdministrativeInvestigationOrder):
	def get_name(self):
		return "Приказ Копия"

	def get_name_for_file(self):
		return f"Приказ_Копия_СОЧ ({self.get_soldier_info().full_name}).docx"

	def copy_text(self):
		self.add_paragraph("КОПИЯ", self.align_right_settings)
		self.add_empty_paragraphs(1)

	def copy_correct_text(self):
		self.add_empty_paragraphs(1)
		clerk = self.get_commander_generic("clerk", "ДЕЛОПРОИЗВОДИТЕЛЯ", 0, True)
		self.add_paragraph(f"Копия верна: {clerk['position']}", self.bold_center_settings)
		self.add_paragraph(clerk["rank"], self.bold_center_settings)
		self.add_paragraph(clerk["name"], self.bold_right_settings)

