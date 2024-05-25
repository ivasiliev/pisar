from classes.document_in_report import MODEL_CURRENT_SOLDIER
from helpers.text_helper import replace_with_glue, get_month_string


class ReplacementUnit:
    def __init__(self, data_model, pers_storage, placeholder):
        self.data_model = data_model
        self.pers_storage = pers_storage
        self.placeholder = placeholder

    def get_soldier_info(self):
        return self.data_model[MODEL_CURRENT_SOLDIER]

    def find(self, text):
        result = ""
        if self.placeholder in text:
            # TODO find first occurrence and replace it only
            result = self.replace(text)
        return result

    def replace(self, text):
        pass

    # TODO put in helper
    def get_date_format_1(self, date_str):
        tokens = date_str.split(".")
        if len(tokens) != 3:
            return date_str
        # print(f"Не удалось определить формат даты {date_str}")
        d = int(tokens[0])
        m = int(tokens[1])
        y = int(tokens[2])
        return replace_with_glue(f"{d} {get_month_string(m)} {y} года")
