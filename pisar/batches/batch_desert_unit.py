from batches.batch_prototype import BatchPrototype
from documents.doc_administrative_investigation import DocAdministrativeInvestigation
from documents.doc_approval_sheet import DocApprovalSheet


class BatchDesertUnit(BatchPrototype):
	def get_name(self):
		return "Самовольное оставление части (группа документов)"

	def render(self):
		self.add_document(DocAdministrativeInvestigation(self.data_model))
		self.add_document(DocApprovalSheet(self.data_model))

		super().render()

