from batches.batch_prototype import BatchPrototype
from documents.doc_act_explanation_impossible import DocActExplanationImpossible
from documents.doc_approval_sheet_official_proceeding import ApprovalSheetOfficialProceeding
from documents.doc_official_proceeding import DocOfficialProceeding
from documents.doc_official_proceeding_order import DocOfficialProceedingOrder
from documents.doc_official_proceeding_protocol import DocOfficialProceedingProtocol
from documents.doc_performance_characteristics import DocPerformanceCharacteristics
from documents.doc_soldier_hr_info import DocSoldierHrCard


class BatchOfficialProceeding(BatchPrototype):
	def get_name(self):
		return "Грубый Дисциплинарный Проступок (группа документов)"

	def render(self):
		self.clear_docs()
		self.add_document(DocOfficialProceeding(self.data_model))
		self.add_document(DocOfficialProceedingProtocol(self.data_model))
		# self.add_document(DocActCopyImpossible(self.data_model))
		self.add_document(DocActExplanationImpossible(self.data_model))
		self.add_document(DocPerformanceCharacteristics(self.data_model))
		self.add_document(DocSoldierHrCard(self.data_model))
		self.add_document(DocOfficialProceedingOrder(self.data_model))
		self.add_document(ApprovalSheetOfficialProceeding(self.data_model))

		super().render()
