import os

from docx import Document

from classes.document_in_report import MODEL_OUTPUT_FOLDER, MODEL_CURRENT_SOLDIER
from helpers.log_helper import log
from templateprocessor.ru_dob import RuDob
from templateprocessor.ru_sold_fio import RuSoldFio
from templateprocessor.ru_sold_position import RuSoldPosition
from templateprocessor.ru_sold_rank import RuSoldRank
from templateprocessor.ru_sold_sr import RuSoldSr

MODEL_BOX_FOLDER = "box_path"


class TemplateProcessor:
    def __init__(self, data_model, pers_storage):
        self.data_model = data_model
        self.pers_storage = pers_storage
        self.box_folder = self.data_model[MODEL_BOX_FOLDER]
        self.output_folder = os.path.join(self.data_model[MODEL_OUTPUT_FOLDER], "box")
        self.replacements = self.get_replacements()

    def process(self):
        if not os.path.exists(self.box_folder):
            os.makedirs(self.box_folder)
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        log(f"Каталог с исходными документами: {self.box_folder}")
        log(f"Результаты здесь: {self.output_folder}")
        for file_name in os.listdir(self.box_folder):
            if not file_name.endswith(".docx"):
                continue
            full_path_input = os.path.join(self.box_folder, file_name)
            s_info = self.data_model[MODEL_CURRENT_SOLDIER]
            fn = file_name.replace(".docx", "") + f" ({s_info.full_name}).docx"
            full_path_output = os.path.join(self.output_folder, fn)
            self.process_document(full_path_input, full_path_output)

    def process_document(self, full_path_input, full_path_output):
        f = open(full_path_input, "rb")
        document = Document(f)
        f.close()

        for paragraph in document.paragraphs:
            if len(paragraph.runs) < 2:
                continue

            # merge runs, prepare them for replacement operations
            run_anchor = None
            for index in range(1, len(paragraph.runs)):
                # on start
                if run_anchor is None:
                    run_anchor = paragraph.runs[index - 1]
                run_this = paragraph.runs[index]
                if len(run_this.text) == 0:
                    continue

                if run_this.bold == run_anchor.bold and run_this.italic == run_anchor.italic and run_this.underline == run_anchor.underline:
                    # merge them
                    run_anchor.text = run_anchor.text + run_this.text
                    run_this.clear()
                else:
                    run_anchor = paragraph.runs[index]

            # replacement routines
            for run in paragraph.runs:
                ln = len(str(run.text))
                if ln > 0:
                    replacement_result = self.replace_all_placeholders(run.text)
                    if replacement_result != run.text:
                        run.text = replacement_result

        document.save(full_path_output)
        log(f"Документ сохранен: {full_path_output}")

    def replace_all_placeholders(self, run_text):
        current_text = ""
        has_changed = True
        while has_changed:
            for repl in self.replacements:
                if len(current_text) == 0:
                    current_text = run_text
                repl_text = repl.find(current_text)
                has_changed = len(repl_text) > 0
                if has_changed:
                    current_text = repl_text

        return current_text

    def get_replacements(self):
        result = []
        result.append(RuDob(self.data_model, self.pers_storage, "{СОЛД-ДР-ПОЛН}"))
        result.append(RuSoldFio(self.data_model, self.pers_storage, "{СОЛД-ФИО;"))
        result.append(RuSoldRank(self.data_model, self.pers_storage, "{СОЛД-ЗВАНИЕ;"))
        result.append(RuSoldSr(self.data_model, self.pers_storage, "{СОЛД-ШР;"))
        result.append(RuSoldPosition(self.data_model, self.pers_storage, "{СОЛД-ДОЛЖНОСТЬ;"))
        return result
