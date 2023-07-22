from batches.batch_prototype import BatchPrototype
from documents.doc_soldier_hr_info import DocSoldierHrCard


class BatchMassHrInfo(BatchPrototype):
	def get_name(self):
		return "Справка (массовая генерация)"

	def render(self):
		self.subfolder_name = self.get_name()
		self.add_document(DocSoldierHrCard(self.data_model))
		super().render()
