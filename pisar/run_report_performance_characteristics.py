from classes.personnel_storage import PersonnelStorage
from documents.doc_performance_characteristics import DocPerformanceCharacteristics

if __name__ == '__main__':
	print("Писарь начинает работу")
	pers_storage = PersonnelStorage()
	pers_storage.load_personnel_list_from_file("\\data\\personnel-demo.xlsx")
	settings = None
	report = DocPerformanceCharacteristics(None)
	report.word_document.sa
	report.render("c:\\temp\\report1\\")