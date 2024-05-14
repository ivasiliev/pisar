from document_prototype import DocumentPrototype
from helpers.log_helper import log


class BatchPrototype(DocumentPrototype):
	def __init__(self, data_model):
		super().__init__(data_model)
		self.data_model = data_model
		# these documents to be rendered for each soldier
		self.docs = []
		# these documents to be rendered once
		self.singletons = []
		self.singletons_executed = False
		self.subfolder_name = None

	def get_name(self):
		return ""

	def add_document(self, doc):
		self.docs.append(doc)

	def add_singleton(self, doc):
		self.singletons.append(doc)

	def render(self):
		for doc in self.docs:
			doc.subfolder_name = self.subfolder_name
			log(f"{doc.get_name()}...")
			doc.render()
		if not self.singletons_executed:
			for doc in self.singletons:
				doc.subfolder_name = self.subfolder_name
				log(f"{doc.get_name()}...")
				doc.render()
			self.singletons_executed = True

	def get_commander_platoon(self):
		if len(self.docs) == 0:
			return None
		return self.docs[0].get_commander_platoon_full_str(0)

	def get_commander_company(self):
		if len(self.docs) == 0:
			return None
		return self.docs[0].get_commander_company_full_str(0)

	def clear_docs(self):
		self.docs = []
		self.singletons = []
