import datetime


class Person:
	def __init__(self):
		self.company = ""
		self.platoon = ""
		self.squad = ""
		self.position = ""
		self.full_name = ""
		self.dob = None

	# proper format dd.mm.yyyy (d.m as well)
	def set_dob(self, dob_str):
		tokens = dob_str.split(".")
		if len(tokens) != 3:
			print(f"Ошибка при разборе даты {dob_str}")
			return
		self.dob = datetime.datetime(int(tokens[2]), int(tokens[1]), int(tokens[0]))
