class BatchPrototype:
	def __init__(self, data_model):
		self.data_model = data_model
		self.docs = []

	def get_name(self):
		return ""

	def add_document(self, doc):
		self.docs.append(doc)

	def render(self):
		for doc in self.docs:
			print(f"{doc.get_name()}...")
			doc.render()

