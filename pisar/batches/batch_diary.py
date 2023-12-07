from batches.batch_prototype import BatchPrototype
from documents.doc_diary_birthdays import DocDiaryBirthdays
from documents.doc_diary_soldier_info import DocDiarySoldierInfo
from documents.doc_diary_violation_discipline import DocDiaryViolationDiscipline


class BatchDiary(BatchPrototype):
	def get_name(self):
		return "Дневник психолого-педагогических наблюдений (группа документов)"

	def render(self):
		self.clear_docs()
		self.subfolder_name = self.get_name()

		self.add_document(DocDiarySoldierInfo(self.data_model))

		self.add_singleton(DocDiaryBirthdays(self.data_model))
		self.add_singleton(DocDiaryViolationDiscipline(self.data_model))
		super().render()

