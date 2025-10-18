class ExcelDocMetadata:
    def __init__(self, full_path, sheet_name, cols, column_count_to_search):
        self.full_path = full_path
        self.sheet_name = sheet_name
        self.cols = cols
        self.column_count_to_search = column_count_to_search
        self.column_dict = {}

    def get_column_index(self, column_key):
        # first let's try to find a column by its key
        if column_key in self.column_dict:
            return self.column_dict[column_key]

        for col_info in self.cols:
            if col_info.key == column_key:
                return col_info.index
        return None

    # columns is list of ColumnInfo
    def add_columns_in_dict(self, columns):
        self.column_dict.clear()
        for col_info in columns:
            index = self.get_column_index(col_info.key)
            # TODO how to check if a column is not found
            if index is not None:
                self.column_dict[col_info.key] = index

