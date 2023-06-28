from batches.batch_prototype import BatchPrototype
from documents.doc_administrative_investigation import DocAdministrativeInvestigation
from documents.doc_administrative_investigation_order import DocAdministrativeInvestigationOrder
from documents.doc_administrative_investigation_order_copy import DocAdministrativeInvestigationOrderCopy
from documents.doc_approval_sheet import DocApprovalSheet
from documents.doc_letter_parents import DocLetterParents
from documents.doc_orientation import DocOrientation


class BatchDesertUnit(BatchPrototype):
	def get_name(self):
		return "Самовольное оставление части (группа документов)"

	def render(self):
		self.add_document(DocAdministrativeInvestigation(self.data_model))
		self.add_document(DocApprovalSheet(self.data_model))
		self.add_document(DocLetterParents(self.data_model))
		self.add_document(DocOrientation(self.data_model))
		self.add_document(DocAdministrativeInvestigationOrder(self.data_model))
		self.add_document(DocAdministrativeInvestigationOrderCopy(self.data_model))

		super().render()

