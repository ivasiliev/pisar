import json
import os
import sys

from classes.document_in_report import MODEL_JSON_OBJECT, MODEL_PERSONNEL_PATH, MODEL_IS_VALID, MODEL_CURRENT_SOLDIER
from classes.personnel_storage import PersonnelStorage
from documents.doc_official_proceeding import DocOfficialProceeding
from helpers.data_model_helper import create_from_json

if __name__ == '__main__':
	print("Писарь начинает работу")
	settings_full_path = str(sys.argv[1])
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
		pers_storage = PersonnelStorage(data_model[MODEL_PERSONNEL_PATH])
		for sld in soldiers:
			current_soldier = pers_storage.find_person_by_id(int(sld))
			if current_soldier is None:
				print(f"Не удалось найти военнослужащего под номером '{str(sld)}'")
				continue

			data_model[MODEL_CURRENT_SOLDIER] = current_soldier
			print(f"Документ для военнослужащего: {current_soldier.full_name}")
			if len(current_soldier.company_commander) > 0:
				c_name = current_soldier.company_commander["name"]
				c_position = current_soldier.company_commander["position"]
				# TODO add rank
				print(f"Ротный командир: {c_name} ({c_position})")
			else:
				print(f"Командир не обнаружен в штатном расписании для {current_soldier.company} роты! В документе "
				      f"заполните эту информацию вручную.")
			doc = DocOfficialProceeding(data_model)
			doc.render()
	print("Писарь завершил работу")
