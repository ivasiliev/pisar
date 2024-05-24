import os

from docx import Document

from classes.document_in_report import MODEL_JSON_OBJECT, MODEL_OUTPUT_FOLDER
from helpers.log_helper import log

MODEL_BOX_FOLDER = "box_path"


class TemplateProcessor:
    def __init__(self, data_model, pers_storage):
        self.data_model = data_model
        self.pers_storage = pers_storage
        self.box_folder = self.data_model[MODEL_JSON_OBJECT][MODEL_BOX_FOLDER]
        self.output_folder = os.path.join(self.data_model[MODEL_JSON_OBJECT][MODEL_OUTPUT_FOLDER], "box")

    def process(self):
        if not os.path.exists(self.box_folder):
            os.makedirs(self.box_folder)
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        log(f"Входный каталог: {self.box_folder}")
        log(f"Результаты здесь: {self.output_folder}")
        for full_path in os.listdir(self.box_folder):
            if not full_path.endswith(".docx"):
                continue
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
                if replacement_result is not None:
                    run.text = replacement_result

    def replace_placeholder(self, run_text):
        while True:
            was_replacement = False
            #if

        result = None
        return result
