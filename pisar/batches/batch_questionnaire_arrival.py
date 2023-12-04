from batches.batch_prototype import BatchPrototype
from documents.doc_questionnaire_arrival import DocQuestArrival


class BatchQuestArrival(BatchPrototype):
	def get_name(self):
		doc = DocQuestArrival(self.data_model)
		return doc.get_name()

	def render(self):
		self.add_document(DocQuestArrival(self.data_model))
		super().render()

