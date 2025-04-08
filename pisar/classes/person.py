import datetime
import hashlib

from helpers.log_helper import log


class Person:
	def __init__(self):
		self.id_sr = ""  # id в ШР (первый столбец)
		self.company = ""  # рота
		self.platoon = ""  # взвод
		self.squad = ""  # отделение
		self.position = ""  # должность, например, пулеметчик
		self.rank = ""  # звание, например, рядовой
		self.full_name = ""
		self.dob = None  # дата рождения
		self.company_commander = {}  # командир роты
		self.unique = ""  # личный номер (по нему сводятся данные между документами Excel)
		self.phone = ""
		self.age = 0

	# proper format dd.mm.yyyy (d.m as well)
	def set_dob(self, dob_str):
		if dob_str is None:
			return
		if isinstance(dob_str, datetime.datetime):
			self.dob = dob_str
		else:
			if len(dob_str) == 0:
				return
			tokens = dob_str.split(".")
			err_str = f"Ошибка при разборе даты {dob_str}. Правильный формат 'ДД.ММ.ГГГГ'. Проверьте столбец с датами рождения!"
			if len(tokens) != 3:
				log(err_str)
				return
			try:
				self.dob = datetime.datetime(int(tokens[2]), int(tokens[1]), int(tokens[0]))
			except:
				log(err_str)

	def get_dob(self):
		if self.dob is None:
			return "[ВСТАВЬТЕ ДАТУ РОЖДЕНИЯ]"
		else:
			d = str(self.dob.day)
			if len(d) < 2:
				d = f"0{d}"
			m = str(self.dob.month)
			if len(m) < 2:
				m = f"0{m}"
			return f"{d}.{m}.{self.dob.year}"

	def get_hash(self):
		un = None
		try:
			v = self.get_unique()
			if len(v) > 0:
				un = self.unique
			if un is None:
				if self.full_name is not None:
					v = str(self.full_name)
					if len(v) > 0:
						un = self.full_name
			if un is not None:
				un = int(hashlib.md5(un.encode("utf-8")).hexdigest(), 16)
		except:
			log("Exception! Can't define hash for this person")
		if un is None:
			log("Can't define hash for this person")
		return un

	def get_unique(self):
		if self.unique is None:
			return ""
		else:
			return str(self.unique)

	def get_unique_is_not_empty(self):
		return len(self.get_unique()) > 0
