import json
import os
import subprocess
import sys
from pathlib import Path

import PySimpleGUI as sg

from classes.run_info import RunInfo

current_path = Path(os.getcwd())
print(f"current path={current_path}")
root_path = current_path.parent.absolute()
print(f"root path={root_path}")

gui_path = os.path.join(root_path, "gui")
documents_path = os.path.join(root_path, "documents")
batches_path = os.path.join(root_path, "batches")
helpers_path = os.path.join(root_path, "helpers")
sys.path.append(gui_path)
sys.path.append(documents_path)
sys.path.append(batches_path)
sys.path.append(helpers_path)

from runner import run_generation, OFFICIAL_PROCEEDING_BATCH, DESERT_UNIT_BATCH, MASS_HR_INFO_BATCH, \
	MASS_PERFORMANCE_CHARACTERISTICS_BATCH, UTILITY_BIRTHDAYS, UTILITY_PERSONNEL_DETAILS_CHECK, \
	UTILITY_PERSONNEL_DETAILS_SORTING, DIARY, QUEST_ARRIVAL


# 0 -- pointer, 1 -- clock
def set_cursor(ctrl_name, cursor_type):
	curs_name = "arrow"
	if cursor_type == 1:
		curs_name = "circle"
	window[ctrl_name].set_cursor(curs_name)


def get_full_path(filename):
	folders_to_search = [
		current_path
		, root_path
		, os.path.join(current_path, "install")
		, os.path.join(root_path, "install")
	]
	for fld in folders_to_search:
		result = os.path.join(fld, filename)
		if os.path.exists(result):
			return result
	print(f"Не удалось обнаружить файл: {filename}")
	return None


def read_app_config():
	# app can be run in different ways
	a_path = get_full_path("app_settings.json")
	if a_path is None:
		print("Не обнаружен файл настроек для приложения. Выполнение программы прекращено.")
		sys.exit()
	return json.load(open(a_path, encoding='UTF8'))


# check app settings
app_settings = read_app_config()
app_version = app_settings["app_version"]
app_release_date = app_settings["app_release_date"]

sg.theme('DarkGreen5')

update_button_key = "update_app_button"
edit_common_settings_key = "edit_common_settings_button"
edit_soldier_settings_key = "edit_soldier_settings_button"

common_config_file = "c:\\pisar_data\\common_info.json"
soldier_config_file = "c:\\pisar_data\\soldier_info.json"

group_official_proceeding = RunInfo()
group_official_proceeding.group_number = 0
group_official_proceeding.group_text = "Служебное разбирательство по факту грубого дисциплинарного проступка"
group_official_proceeding.batch_name = OFFICIAL_PROCEEDING_BATCH
group_official_proceeding.docs_list = []

group_desert_unit = RunInfo()
group_desert_unit.group_number = 1
group_desert_unit.group_text = "Служебное разбирательство по факту cамовольного оставления части"
group_desert_unit.batch_name = DESERT_UNIT_BATCH
group_desert_unit.docs_list = []

group_mass_hr_info_unit = RunInfo()
group_mass_hr_info_unit.group_number = 2
group_mass_hr_info_unit.group_text = "Массовая генерация документа 'Справка'"
group_mass_hr_info_unit.batch_name = MASS_HR_INFO_BATCH
group_mass_hr_info_unit.docs_list = []

group_mass_perf_char_unit = RunInfo()
group_mass_perf_char_unit.group_number = 3
group_mass_perf_char_unit.group_text = "Массовая генерация документа 'Служебная характеристика'"
group_mass_perf_char_unit.batch_name = MASS_PERFORMANCE_CHARACTERISTICS_BATCH
group_mass_perf_char_unit.docs_list = []

group_utils_birthdays = RunInfo()
group_utils_birthdays.group_number = 4
group_utils_birthdays.group_text = "Утилита 'Дни рождения'"
group_utils_birthdays.batch_name = UTILITY_BIRTHDAYS
group_utils_birthdays.docs_list = []

group_utils_pers_det_check = RunInfo()
group_utils_pers_det_check.group_number = 5
group_utils_pers_det_check.group_text = "Утилита 'Сверка ШР и ЛС'"
group_utils_pers_det_check.batch_name = UTILITY_PERSONNEL_DETAILS_CHECK
group_utils_pers_det_check.docs_list = []

group_utils_pers_det_sorting = RunInfo()
group_utils_pers_det_sorting.group_number = 6
group_utils_pers_det_sorting.group_text = "Утилита 'Сортировка ЛС согласно порядку в ШР'"
group_utils_pers_det_sorting.batch_name = UTILITY_PERSONNEL_DETAILS_SORTING
group_utils_pers_det_sorting.docs_list = []

group_diary = RunInfo()
group_diary.group_number = 7
group_diary.group_text = "Дневник психолого-педагогических наблюдений"
group_diary.batch_name = DIARY
group_diary.docs_list = []

group_quest_arrival = RunInfo()
group_quest_arrival.group_number = 8
group_quest_arrival.group_text = "Анкета прибывшего в зону СВО"
group_quest_arrival.batch_name = QUEST_ARRIVAL
group_quest_arrival.docs_list = []

batch_groups = [group_official_proceeding, group_desert_unit, group_mass_hr_info_unit, group_mass_perf_char_unit,
                group_utils_birthdays, group_utils_pers_det_check, group_utils_pers_det_sorting, group_diary,
                group_quest_arrival]

layout = [
	[sg.Button(key=update_button_key, button_text="Обновить программу"),
	 sg.Button(key=edit_common_settings_key, button_text="Войсковая часть"),
	 sg.Button(key=edit_soldier_settings_key, button_text="Военнослужащий")
	 ],
	[sg.VPush()]
]

for grp in batch_groups:
	# , size=(700, 160)
	layout.append([sg.Frame("", grp.create_ui())])

window = sg.Window(f"Писарь   {app_version} | {app_release_date}", layout)

while True:
	event, values = window.read()
	if event == sg.WIN_CLOSED:
		break
	if event == update_button_key:
		full_path_update = get_full_path("update.bat")
		if full_path_update is None:
			print(f"Не удалось найти запускаемый файл для обновлений.")
		else:
			print(f"Updater: {full_path_update}")
			# full_path_run = os.path.join(current_path, "install", "pisar.bat")
			set_cursor(update_button_key, 1)
			subprocess.call([full_path_update])

			# if version changed, need to re-run app
			app_settings = read_app_config()
			print("Приложение обновлено. Требуется перезапуск!")
			# if app_settings["app_version"] != app_version:
			#	print("Требуется перезапуск!")
			# TODO
			# subprocess.Popen([full_path_run])
			# sys.exit()
			# break

			set_cursor(update_button_key, 0)
	if event == edit_common_settings_key:
		subprocess.call(["notepad", common_config_file])
	if event == edit_soldier_settings_key:
		subprocess.call(["notepad", soldier_config_file])
	if event.endswith("_run"):
		gr_num = int(event.replace("report_", "").replace("_run", ""))
		gr = batch_groups[gr_num]
		set_cursor(event, 1)
		run_generation(common_config_file, soldier_config_file, gr.batch_name)
		set_cursor(event, 0)

window.close()
