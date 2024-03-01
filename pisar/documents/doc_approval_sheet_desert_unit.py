from documents.approval_sheet_prototype import ApprovalSheetPrototype


class DocApprovalSheetDesertUnit(ApprovalSheetPrototype):
	def get_name(self):
		return "Лист согласования"

	def get_name_for_file(self):
		return f"Лист согласования_СОЧ ({self.get_soldier_info().full_name}).docx"

	def render(self):
		self.title = "По факту самовольного оставления части"

		super().render()
