from classes.report import Report
from documents.doc_official_proceeding import DocOfficialProceeding


class ReportOfficialProceeding(Report):
	def __init__(self, personnel_storage, settings):
		super().__init__(personnel_storage, settings)
		self.documents.append(DocOfficialProceeding(None))

