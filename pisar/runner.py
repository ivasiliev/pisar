import json
import os
import sys

from batches.batch_official_proceeding import BatchOfficialProceeding
from classes.document_in_report import MODEL_JSON_OBJECT, MODEL_PERSONNEL_PATH, MODEL_IS_VALID, MODEL_CURRENT_SOLDIER
from classes.personnel_storage import PersonnelStorage
from documents.doc_act_copy_impossible import DocActCopyImpossible
from documents.doc_act_explanation_impossible import DocActExplanationImpossible
from documents.doc_official_proceeding import DocOfficialProceeding
from documents.doc_order_official_proceeding import DocOrderOfficialProceeding
from documents.doc_performance_characteristics import DocPerformanceCharacteristics
from helpers.data_model_helper import create_from_json


def run_generation(settings_full_path):
	print("Писарь начинает работу")
	print(f"Файл настроек={settings_full_path}")
	if not os.path.exists(settings_full_path):
		print(f"Файл настроек не обнаружен либо недоступен. Выполнение программы прервано.")
	else:
		print("Файл настроек обнаружен")

	js_settings = json.load(open(settings_full_path, encoding='UTF8'))
	data_model = create_from_json(js_settings)
	if not data_model[MODEL_IS_VALID]:
		print("Файл настроек содержит неверную информацию. Выполнение программы прервано.")
		sys.exit()

	soldiers = data_model[MODEL_JSON_OBJECT]["soldier_ids"].split(",")
	if len(soldiers) == 0:
		print(f"Не заданы номера военнослужащих. В настроечном файле в поле 'soldier_ids' внесите их номера из "
		      f"штатного расписания (первый столбец). Выполнение программы прервано.")
	else:
		# we define type of generation via settings file name
		settings_filename = os.path.basename(settings_full_path)
		settings_key = os.path.splitext(settings_filename)[0]
		# we can have a single document generation or batch generation
		doc = None

		if settings_key.startswith("batch"):
			if settings_key == "batch_official_proceeding":
				doc = BatchOfficialProceeding(data_model)
			pass
		else:
			if settings_key == "order_official_proceeding":
				doc = DocOrderOfficialProceeding(data_model)
			else:
				if settings_key == "official_proceeding":
					doc = DocOfficialProceeding(data_model)
				else:
					if settings_key == "performance_characteristics":
						doc = DocPerformanceCharacteristics(data_model)
					else:
						if settings_key == "explanation_impossible":
							doc = DocActExplanationImpossible(data_model)
						else:
							if settings_key == "copy_impossible":
								doc = DocActCopyImpossible(data_model)

		if doc is None:
			print(f"Не удалось определить тип документа. Выполнение программы прервано.")
		else:
			print(f"Тип документа: {doc.get_name()}.")
			pers_storage = PersonnelStorage(data_model[MODEL_PERSONNEL_PATH])
			for sld in soldiers:
				current_soldier = pers_storage.find_person_by_id(int(sld))
				if current_soldier is None:
					print(f"Не удалось найти военнослужащего под номером '{str(sld)}'")
					continue

				data_model[MODEL_CURRENT_SOLDIER] = current_soldier
				print(f"Документ для военнослужащего: {current_soldier.full_name}")

				doc.render()
	print("Писарь завершил работу")


if __name__ == '__main__':
	run_generation(str(sys.argv[1]))
