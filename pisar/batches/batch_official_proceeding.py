from batches.batch_prototype import BatchPrototype
from documents.doc_act_copy_impossible import DocActCopyImpossible
from documents.doc_act_explanation_impossible import DocActExplanationImpossible
from documents.doc_official_proceeding import DocOfficialProceeding
from documents.doc_performance_characteristics import DocPerformanceCharacteristics
from documents.doc_official_proceeding_protocol import DocOfficialProceedingProtocol


class BatchOfficialProceeding(BatchPrototype):
	def get_name(self):
		return "Грубый Дисциплинарный Проступок (группа документов)"

	def render(self):
		self.clear_docs()
		self.add_document(DocOfficialProceeding(self.data_model))
		self.add_document(DocOfficialProceedingProtocol(self.data_model))
		self.add_document(DocActCopyImpossible(self.data_model))
		self.add_document(DocActExplanationImpossible(self.data_model))
		self.add_document(DocPerformanceCharacteristics(self.data_model))

		super().render()
