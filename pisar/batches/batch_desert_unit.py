from batches.batch_prototype import BatchPrototype
from documents.doc_desert_unit import DocDesertUnit


class BatchDesertUnit(BatchPrototype):
	def get_name(self):
		return "Самовольное оставление части (группа документов)"

	def render(self):
		self.add_document(DocDesertUnit(self.data_model))

		super().render()

