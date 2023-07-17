class ExcelDocMetadata:
	def __init__(self, full_path, sheet_name, cols, column_count_to_search):
		self.full_path = full_path
		self.sheet_name = sheet_name
		self.cols = cols
		self.column_count_to_search = column_count_to_search

	def get_column_index(self, column_key):
		for col_info in self.cols:
			if col_info.key == column_key:
				return col_info.index
		return None
