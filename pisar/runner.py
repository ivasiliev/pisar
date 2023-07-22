import json
import os
import sys

from batches.batch_desert_unit import BatchDesertUnit
from batches.batch_mass_hr_info import BatchMassHrInfo
from batches.batch_mass_performance_characteristics import BatchMassPerformanceCharacteristics
from batches.batch_official_proceeding import BatchOfficialProceeding
from classes.document_in_report import MODEL_JSON_OBJECT, MODEL_PERSONNEL_PATH, MODEL_IS_VALID, MODEL_CURRENT_SOLDIER, \
	MODEL_PERSONNEL_DETAILS_PATH
from classes.personnel_storage import PersonnelStorage
from helpers.data_model_helper import create_from_json

OFFICIAL_PROCEEDING_BATCH = "official_proceeding"
DESERT_UNIT_BATCH = "desert_unit"
MASS_HR_INFO_BATCH = "MASS_HR_INFO_BATCH"
MASS_PERFORMANCE_CHARACTERISTICS_BATCH = "MASS_PERFORMANCE_CHARACTERISTICS_BATCH"


def print_commander(commander, title):
	if commander is None or not commander["found"]:
		return
	print(f"{title}: {commander['name']} {commander['rank']} {commander['position']}")


def check_settings_file(full_path, name):
	is_valid = True
	print(f"Файл настроек для {name}={full_path}")
	if not os.path.exists(full_path):
		print(f"Файл настроек для {name} не обнаружен либо недоступен. Проверьте путь, имя файла и его расширение. Выполнение программы прервано.")
		is_valid = False
	else:
		print("Файл настроек обнаружен")
	return is_valid


def run_generation(common_config_file, soldier_config_file, report_type):
	print("Писарь начинает работу")
	s_files = [
		[common_config_file, "войсковой части"]
		, [soldier_config_file, "военнослужащего"]
	]
	for f in s_files:
		if not check_settings_file(f[0], f[1]):
			return

	js_settings = json.load(open(common_config_file, encoding='UTF8'))
	js_settings.update(json.load(open(soldier_config_file, encoding='UTF8')))
	data_model = create_from_json(js_settings)
	if not data_model[MODEL_IS_VALID]:
		print("Файл настроек содержит неверную информацию. Выполнение программы прервано.")
		return

	sold_ids = data_model[MODEL_JSON_OBJECT]["soldier_ids"].split(",")
	soldiers = []
	for sld in sold_ids:
		if "-" in sld:
			tkn = sld.split("-")
			if len(tkn) == 2:
				for i in range(int(tkn[0]), int(tkn[1]) + 1):
					soldiers.append(i)
		else:
			soldiers.append(int(sld))

	if len(soldiers) == 0:
		print(f"Не заданы номера военнослужащих. В настроечном файле в поле 'soldier_ids' внесите их номера из "
		      f"штатного расписания (первый столбец). Выполнение программы прервано.")
	else:
		doc = None
		if report_type == OFFICIAL_PROCEEDING_BATCH:
			doc = BatchOfficialProceeding(data_model)
		if report_type == DESERT_UNIT_BATCH:
			doc = BatchDesertUnit(data_model)
		if report_type == MASS_HR_INFO_BATCH:
			doc = BatchMassHrInfo(data_model)
		if report_type == MASS_PERFORMANCE_CHARACTERISTICS_BATCH:
			doc = BatchMassPerformanceCharacteristics(data_model)

		if doc is None:
			print(f"Не удалось определить тип документа. Выполнение программы прервано.")
		else:
			print(f"Тип документа: {doc.get_name()}.")
			pers_storage = PersonnelStorage(data_model)
			if not pers_storage.is_valid:
				print("Неверная структура Штатного расписания/Информации о личном составе. Выполнение программы прервано.")
				return
			for sld in soldiers:
				current_soldier = pers_storage.find_person_by_id(sld)
				if current_soldier is None:
					print(f"Не удалось найти военнослужащего под номером '{str(sld)}'")
					continue

				data_model[MODEL_CURRENT_SOLDIER] = current_soldier
				print(f"Документ для военнослужащего: {current_soldier.full_name}")

				# print_commander(doc.get_commander_company(), "ротный:")
				# print_commander(doc.get_commander_platoon(), "взводный:")

				doc.render()
	print("Писарь завершил работу")


if __name__ == '__main__':
	if len(sys.argv) == 2:
		common_config = "report-settings/common_info.json"
		soldier_config = "report-settings/soldier_info.json"
		run_generation(common_config, soldier_config, sys.argv[1])
