import datetime

from helpers.log_helper import log


class PerformanceHelper:
	def __init__(self):
		self.time_start = None

	def start(self):
		self.time_start = datetime.datetime.now()

	def stop_and_print(self):
		if self.time_start is None:
			return
		time_finish = datetime.datetime.now()
		delta = time_finish - self.time_start
		log(f"Операция заняла {delta}")
