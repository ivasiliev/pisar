import PySimpleGUI as sg


class RunInfo:
	def __init__(self):
		self.group_number = -1
		self.group_text = ""
		self.docs_list = []
		self.batch_name = ""

	def create_ui(self):
		if self.group_number == -1:
			return None

		rep_text = sg.Text(self.group_text, font=("Helvetica", 12, "bold"))
		rep_button_run = sg.Button(key=f"report_{self.group_number}_run", button_text="Запуск")
		rep_layer = [rep_text, rep_button_run]

		rep_layer2 = []
		for dc in self.docs_list:
			rep_layer2.append([sg.Text(f"* {dc}")])
		# col_content = [[sg.Text(f"* {self.docs_list[0]}")]]
		cl = sg.Column(rep_layer2)

		return [rep_layer, [cl]]
