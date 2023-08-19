class DocumentPrototype:
	def get_name(self):
		return ""

	def get_name_for_file(self):
		return ""

	def render(self):
		pass

	def is_utility(self):
		return False

	def __init__(self, data_model):
		self.data_model = data_model

	def get_pers_storage(self):
		return self.data_model["pers_storage"]
