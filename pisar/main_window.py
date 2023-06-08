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
