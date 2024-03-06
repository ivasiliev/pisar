import os

from classes.document_in_report import MODEL_OUTPUT_FOLDER, MODEL_JSON_OBJECT
from document_prototype import DocumentPrototype
from datetime import date


class UtilityPrototype(DocumentPrototype):
	def is_utility(self):
		return True

	def get_row_limit(self):
		return self.data_model[MODEL_JSON_OBJECT]["row_limit"]

	def save_workbook(self, wb):
		if self.data_model is not None and self.data_model[MODEL_OUTPUT_FOLDER]:
			full_path_folder = self.data_model[MODEL_OUTPUT_FOLDER]
			full_path = os.path.join(full_path_folder, self.get_name_for_file())
			wb.save(full_path)
			print(f"Создан документ {full_path}.")

	def get_date_string(self, dt=None):
		if dt is None:
			dt = date.today()
		return f"{dt.day}.{dt.month}.{dt.year}"
