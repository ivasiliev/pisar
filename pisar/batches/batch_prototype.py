class BatchPrototype:
	def __init__(self, data_model):
		self.data_model = data_model
		self.docs = []
		self.subfolder_name = None

	def get_name(self):
		return ""

	def add_document(self, doc):
		self.docs.append(doc)

	def render(self):
		for doc in self.docs:
			doc.subfolder_name = self.subfolder_name
			print(f"{doc.get_name()}...")
			doc.render()

	def get_commander_platoon(self):
		if len(self.docs) == 0:
			return None
		return self.docs[0].get_commander_platoon_full_str(0)

	def get_commander_company(self):
		if len(self.docs) == 0:
			return None
		return self.docs[0].get_commander_company_full_str(0)

