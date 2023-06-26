import json
import os
import subprocess
import sys
from pathlib import Path

import PySimpleGUI as sg

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

from runner import run_generation


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

# button_text_report_settings = "Настройки"
button_text_report_run = "Запуск"

update_button_key = "update_app_button"
edit_common_settings_key = "edit_common_settings_button"
edit_soldier_settings_key = "edit_soldier_settings_button"

common_config_file = "c:\\pisar_data\\common_info.json"
soldier_config_file = "c:\\pisar_data\\soldier_info.json"

rep1_text1 = sg.Text("Служебное разбирательство по факту грубого дисциплинарного проступка",
                     font=("Helvetica", 12, "bold"))
# rep1_button_settings = sg.Button(key="report1_settings", button_text=button_text_report_settings)
rep1_button_run = sg.Button(key="report1_run", button_text=button_text_report_run)

rep1_layer1 = [rep1_text1, rep1_button_run]  # rep1_button_settings

docs_list = ["Служебное разбирательство (сам документ)",
             "Протокол о ГДП",
             "Акт о невозможности получения копии протокола о ГДП", "Акт о невозможности взять объяснение",
             "Служебная характеристика"]

rep1_layer2 = []
for dc in docs_list:
	rep1_layer2.append([sg.Text(f"* {dc}")])
col_content = [[sg.Text(f"* {docs_list[0]}")]]
cl = sg.Column(rep1_layer2)

layout = [
	[sg.Button(key=update_button_key, button_text="Обновить программу"),
	 sg.Button(key=edit_common_settings_key, button_text="Воинская часть"),
	 sg.Button(key=edit_soldier_settings_key, button_text="Военнослужащий")
	 ],
	[sg.VPush()],
	[sg.Frame("", [rep1_layer1, [cl]])]
]

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
	if event == "report1_run":
		# full_path = os.path.join(root_path, "report-settings", "batch_official_proceeding.json")
		set_cursor("report1_run", 1)
		run_generation(common_config_file, soldier_config_file, "official_proceeding")
		set_cursor("report1_run", 0)

window.close()
