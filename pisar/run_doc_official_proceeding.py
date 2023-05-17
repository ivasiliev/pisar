from classes.document_in_report import MODEL_PERSONNEL_PATH, MODEL_OUTPUT_FOLDER, MODEL_PERSONS, MODEL_MORPHOLOGY
from documents.doc_official_proceeding import DocOfficialProceeding
import pymorphy2
import sys

if __name__ == '__main__':
	print("Писарь начинает работу")
	

	morph = pymorphy2.MorphAnalyzer()
	data_model = {
		MODEL_PERSONNEL_PATH: "data\\personnel-demo.xlsx"
		, MODEL_OUTPUT_FOLDER: "c:\\temp\\report1\\"
		, MODEL_PERSONS: "2"
		, MODEL_MORPHOLOGY: morph
	}

	doc = DocOfficialProceeding(data_model)
	doc.render()
