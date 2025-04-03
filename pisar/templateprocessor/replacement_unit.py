from classes.document_in_report import MODEL_CURRENT_SOLDIER, MODEL_JSON_OBJECT, MODEL_MORPHOLOGY
from helpers.log_helper import log


class ReplacementUnit:
    def __init__(self, data_model, pers_storage, placeholder):
        self.data_model = data_model
        self.pers_storage = pers_storage
        self.placeholder = placeholder

    def get_soldier_info(self):
        return self.data_model[MODEL_CURRENT_SOLDIER]

    def get_report_settings(self):
        return self.data_model[MODEL_JSON_OBJECT]

    def find(self, text):
        current_text = ""
        # падежи Именительный, Родительный, Творительный
        suffixes = ["И", "Р", "Т"]
        placeholders_to_check = []
        if self.placeholder.endswith("}"):
            placeholders_to_check.append(self.placeholder)
        else:
            for suffix in suffixes:
                placeholders_to_check.append(f"{self.placeholder}{suffix}}}")

        for placeholder in placeholders_to_check:
            if placeholder in text:
                if len(current_text) == 0:
                    current_text = text
                # here is actually replaces text
                current_text = self.replace(placeholder, current_text)

        # returns updated string
        return current_text

    def replace(self, actual_placeholder, text):
        pass

    def extract_declension(self, actual_placeholder):
        tokens = actual_placeholder.split(";")
        if len(tokens) != 2:
            log(f"placeholder {actual_placeholder} is incorrect")
            return None
        declension_str = tokens[1].replace("}", "").strip().upper()
        if len(declension_str) != 1:
            log(f"can't define declension_str ({tokens[1]})")
            return None
        result = -1
        if declension_str == "И":
            result = 0
        if declension_str == "Р":
            result = 1
        if declension_str == "Т":
            result = 2
        if result == -1:
            log(f"can't define declension ({declension_str})")
            return None
        else:
            return result

    def get_morph(self):
        return self.data_model[MODEL_MORPHOLOGY]

    def get_date_of_event(self):
        return self.get_report_settings_by_name("date_of_event")

    # TODO to helper
    def get_report_settings_by_name(self, name):
        rep_settings = self.get_report_settings()
        if name in rep_settings:
            return rep_settings[name]
        else:
            return ""
