class ColumnInfo:
	def __init__(self, key, title):
		self.key = key
		self.title = title
		self.index = -1

	def get_name(self):
		return self.title.casefold()

	def is_found(self):
		return self.index > -1
