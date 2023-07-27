import os

from classes.document_in_report import MODEL_OUTPUT_FOLDER
from document_prototype import DocumentPrototype


class UtilityPrototype(DocumentPrototype):
	def is_utility(self):
		return True

	def get_pers_storage(self):
		return self.data_model["pers_storage"]

	def save_workbook(self, wb):
		if self.data_model is not None and self.data_model[MODEL_OUTPUT_FOLDER]:
			full_path_folder = self.data_model[MODEL_OUTPUT_FOLDER]
			full_path = os.path.join(full_path_folder, self.get_name_for_file())
			wb.save(full_path)
			print(f"Создан документ {full_path}.")


