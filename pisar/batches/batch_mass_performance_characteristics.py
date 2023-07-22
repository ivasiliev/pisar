from batches.batch_prototype import BatchPrototype
from documents.doc_performance_characteristics import DocPerformanceCharacteristics


class BatchMassPerformanceCharacteristics(BatchPrototype):
	def get_name(self):
		return "Служебная характеристика (массовая генерация)"

	def render(self):
		self.subfolder_name = self.get_name()
		self.add_document(DocPerformanceCharacteristics(self.data_model))
		super().render()
