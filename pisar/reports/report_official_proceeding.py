from classes.report import Report
from documents.doc_official_proceeding import DocOfficialProceeding


class ReportOfficialProceeding(Report):
	def __init__(self):
		super().__init__()
		self.documents.append(DocOfficialProceeding(None))

