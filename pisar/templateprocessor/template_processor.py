import os

from docx import Document

from classes.document_in_report import MODEL_JSON_OBJECT, MODEL_OUTPUT_FOLDER
from helpers.log_helper import log
from templateprocessor.ru_dob import RuDob

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
            full_path = os.path.join(self.box_folder, file_name)
            self.process_document(full_path)

    def process_document(self, full_path):
        f = open(full_path, "rb")
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
                if len(run.text) == 0:
                    continue
                replacement_result = self.replace_placeholder(run.text)
                if len(replacement_result) > 0:
                    run.text = replacement_result

    def replace_placeholder(self, run_text):
        repl_count = -1
        replacement_result = ""
        while repl_count != 0:
            repl_count = 0
            for repl in self.replacements:
                repl_text = repl.find(run_text)
                repl_count = repl_count + len(repl_text)
                if len(replacement_result) == 0:
                    replacement_result = run_text
                replacement_result = replacement_result.replace(repl_text, run_text)

        return replacement_result

    def get_replacements(self):
        result = []
        result.append(RuDob(self.data_model, self.pers_storage, "{СОЛД-ДР-ПОЛН}"))


        return result
