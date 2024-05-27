# create data model with settings from Settings json file
import os

import pymorphy2
from pytrovich.maker import PetrovichDeclinationMaker

from classes.document_in_report import MODEL_PERSONNEL_PATH, MODEL_OUTPUT_FOLDER, MODEL_MORPHOLOGY, \
	MODEL_JSON_OBJECT, MODEL_MORPHOLOGY_FOR_NAMES, MODEL_IS_VALID, MODEL_PERSONNEL_DETAILS_PATH
from helpers.log_helper import log
from templateprocessor.template_processor import MODEL_BOX_FOLDER


def create_from_json(js_settings):
	morph = pymorphy2.MorphAnalyzer()
	maker = PetrovichDeclinationMaker()

	data_model = {
		MODEL_PERSONNEL_PATH: js_settings["personnel_path"]
		, MODEL_PERSONNEL_DETAILS_PATH: js_settings["personnel_details_path"]
		, MODEL_OUTPUT_FOLDER: js_settings["output_path"]
		, MODEL_BOX_FOLDER: js_settings[MODEL_BOX_FOLDER]
		, MODEL_MORPHOLOGY: morph
		, MODEL_JSON_OBJECT: js_settings
		, MODEL_MORPHOLOGY_FOR_NAMES: maker
		, MODEL_IS_VALID: True
	}

	print(f"Используется файл Штатного расписания: {data_model[MODEL_PERSONNEL_PATH]}")
	print(f"Используется файл Информация о личном составе: {data_model[MODEL_PERSONNEL_DETAILS_PATH]}")
	if not os.path.exists(data_model[MODEL_PERSONNEL_PATH]):
		print(f"Файл штатного расписания отсутствует или недоступен: '{data_model[MODEL_PERSONNEL_PATH]}'")
		data_model[MODEL_IS_VALID] = False
	if not os.path.exists(data_model[MODEL_PERSONNEL_DETAILS_PATH]):
		print(f"Файл Информация о личном составе отсутствует или недоступен: '{data_model[MODEL_PERSONNEL_DETAILS_PATH]}'")
		data_model[MODEL_IS_VALID] = False

	return data_model
