import json
import os
import sys

import PySimpleGUI as sg
import subprocess
from pathlib import Path
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
				if len(current_soldier.company_commander) > 0:
					c_name = current_soldier.company_commander["name"]
					c_position = current_soldier.company_commander["position"]
					# TODO add rank
					print(f"Ротный командир: {c_name} ({c_position})")
				else:
					print(f"Командир не обнаружен в штатном расписании для {current_soldier.company} роты! В документе "
					      f"заполните эту информацию вручную.")
				doc.render()
	print("Писарь завершил работу")


# 0 -- pointer, 1 -- clock
def set_cursor(ctrl_name, cursor_type):
	curs_name = "arrow"
	if cursor_type == 1:
		curs_name = "circle"
	window[ctrl_name].set_cursor(curs_name)


current_path = Path(os.getcwd())
print(f"current path={current_path}")
root_path = current_path.parent.absolute()
print(f"root path={root_path}")

sg.theme('DarkGreen5')

button_text_report_settings = "Настройки"
button_text_report_run = "Запуск"

update_button_key = "update_app_button"

rep1_text1 = sg.Text("Служебное разбирательство по факту грубого дисциплинарного проступка",
                     font=("Helvetica", 12, "bold"))
rep1_button_settings = sg.Button(key="report1_settings", button_text=button_text_report_settings)
rep1_button_run = sg.Button(key="report1_run", button_text=button_text_report_run)

rep1_layer1 = [rep1_text1, rep1_button_run, rep1_button_settings]

docs_list = ["Служебное разбирательство (сам документ)",
             "Акт о невозможности получения копии протокола о ГДП", "Акт о невозможности взять объяснение",
             "Служебная характеристика"]
rep1_layer2 = []
for dc in docs_list:
	rep1_layer2.append([sg.Text(f"* {dc}")])
col_content = [[sg.Text(f"* {docs_list[0]}")]]
cl = sg.Column(rep1_layer2)

layout = [
	[sg.Button(key=update_button_key, button_text="Обновить программу")],
	[sg.VPush()],
	[sg.Frame("", [rep1_layer1, [cl]])]
]

window = sg.Window("Писарь", layout)

while True:
	event, values = window.read()
	if event == sg.WIN_CLOSED:
		break
	if event == update_button_key:
		full_path = os.path.join(root_path, "install", "update.bat")
		set_cursor(update_button_key, 1)
		subprocess.call([full_path])
		set_cursor(update_button_key, 0)

	if event == "report1_run":
		full_path = os.path.join(root_path, "report-settings", "batch_official_proceeding.json")
		set_cursor("report1_run", 1)
		run_generation(full_path)
		set_cursor("report1_run", 0)

	if event == "report1_settings":
		subprocess.call(["notepad", "c:\\pisar_data\\batch_official_proceeding.json"])


window.close()
