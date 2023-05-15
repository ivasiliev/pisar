import os


class Report:
	def __init__(self, personnel_storage, settings):
		self.documents = []
		self.personnel_storage = personnel_storage
		self.settings = settings

	def initialize(self):
		for doc in self.documents:
			doc.prepare()

	# creates a set of documents for the given report and saves them
	# to full_path_folder
	def render(self, full_path_folder):
		if not os.path.exists(full_path_folder):
			os.makedirs(full_path_folder)

		for doc in self.documents:
			print(f"Обработка документа '{doc.get_name()}'...")
			doc.render()
			full_path = os.path.join(full_path_folder, doc.get_name_for_file())
			doc.word_document.save(full_path)
			print(f"Создан документ {full_path}.")

