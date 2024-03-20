from batches.batch_prototype import BatchPrototype
from documents.doc_administrative_investigation import DocAdministrativeInvestigation
from documents.doc_administrative_investigation_order import DocAdministrativeInvestigationOrder
from documents.doc_administrative_investigation_order_copy import DocAdministrativeInvestigationOrderCopy
from documents.doc_approval_sheet_desert_unit import DocApprovalSheetDesertUnit
from documents.doc_letter_parents import DocLetterParents
from documents.doc_orientation import DocOrientation
from documents.doc_performance_characteristics import DocPerformanceCharacteristics
from documents.doc_soldier_card import DocSoldierCard
from documents.doc_soldier_hr_info import DocSoldierHrCard


class BatchDesertUnit(BatchPrototype):
	def get_name(self):
		return "Самовольное оставление части (группа документов)"

	def render(self):
		self.clear_docs()
		self.add_document(DocAdministrativeInvestigation(self.data_model))
		self.add_document(DocApprovalSheetDesertUnit(self.data_model))
		self.add_document(DocLetterParents(self.data_model))
		self.add_document(DocOrientation(self.data_model))
		self.add_document(DocAdministrativeInvestigationOrder(self.data_model))
		self.add_document(DocAdministrativeInvestigationOrderCopy(self.data_model))
		self.add_document(DocPerformanceCharacteristics(self.data_model))
		self.add_document(DocSoldierCard(self.data_model))
		self.add_document(DocSoldierHrCard(self.data_model))

		super().render()
