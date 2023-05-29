# create data model with settings from Settings json file
import os

import pymorphy2
from pytrovich.maker import PetrovichDeclinationMaker

from classes.document_in_report import MODEL_PERSONNEL_PATH, MODEL_OUTPUT_FOLDER, MODEL_MORPHOLOGY, \
	MODEL_JSON_OBJECT, MODEL_NAME_MORPHOLOGY, MODEL_IS_VALID


def create_from_json(js_settings):
	morph = pymorphy2.MorphAnalyzer()
	maker = PetrovichDeclinationMaker()

	data_model = {
		MODEL_PERSONNEL_PATH: js_settings["personnel_path"]
		, MODEL_OUTPUT_FOLDER: js_settings["output_path"]
		, MODEL_MORPHOLOGY: morph
		, MODEL_JSON_OBJECT: js_settings
		, MODEL_NAME_MORPHOLOGY: maker
		, MODEL_IS_VALID: True
	}

	if not os.path.exists(data_model[MODEL_PERSONNEL_PATH]):
		print(f"Файл штатного расписания отсутствует или недоступен: '{data_model[MODEL_PERSONNEL_PATH]}'")
		data_model[MODEL_IS_VALID] = False

	return data_model
