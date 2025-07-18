import json
import os
import sys
import logging
from datetime import datetime

from batches.batch_desert_unit import BatchDesertUnit
from batches.batch_diary import BatchDiary
from batches.batch_mass_hr_info import BatchMassHrInfo
from batches.batch_mass_performance_characteristics import BatchMassPerformanceCharacteristics
from batches.batch_official_proceeding import BatchOfficialProceeding
from batches.batch_questionnaire_arrival import BatchQuestArrival
from classes.document_in_report import MODEL_JSON_OBJECT, MODEL_IS_VALID, MODEL_CURRENT_SOLDIER, MODEL_OUTPUT_FOLDER
from classes.personnel_storage import PersonnelStorage
from helpers.data_model_helper import create_from_json
from helpers.log_helper import log
from templateprocessor.template_processor import TemplateProcessor
from utils.utility_birthdays import UtilityBirthday
from utils.utility_personnel_details_check import UtilityPersonnelDetailsCheck
from utils.utility_personnel_details_sorting import UtilityPersonnelDetailsSorting
from utils.utility_personnel_details_sorting_position import UtilityPersonnelDetailsSortingPosition

OFFICIAL_PROCEEDING_BATCH = "OFFICIAL_PROCEEDING_BATCH"
DESERT_UNIT_BATCH = "DESERT_UNIT_BATCH"
MASS_HR_INFO_BATCH = "MASS_HR_INFO_BATCH"
MASS_PERFORMANCE_CHARACTERISTICS_BATCH = "MASS_PERFORMANCE_CHARACTERISTICS_BATCH"
UTILITY_BIRTHDAYS = "UTILITY_BIRTHDAYS"
UTILITY_PERSONNEL_DETAILS_CHECK = "UTILITY_PERSONNEL_DETAILS_CHECK"
UTILITY_PERSONNEL_DETAILS_SORTING = "UTILITY_PERSONNEL_DETAILS_SORTING"
DIARY = "DIARY"
QUEST_ARRIVAL = "QUEST_ARRIVAL"
BOX_PROCESSING = "BOX_PROCESSING"
# Новая сортировка по должности (по возрастанию). Номер должности это первый столбец.
UTILITY_PERSONNEL_DETAILS_SORTING_POSITION = "UTILITY_PERSONNEL_DETAILS_SORTING_POSITION"


def check_settings_file(full_path, name):
    is_valid = True
    print(f"Файл настроек для {name}={full_path}")
    if not os.path.exists(full_path):
        log(
            f"Файл настроек для {name} не обнаружен либо недоступен. Проверьте путь, имя файла и его расширение. Выполнение программы прервано.")
        is_valid = False
    else:
        log("Файл настроек обнаружен")
    return is_valid


def run_generation(common_config_file, soldier_config_file, report_type):
    print("Писарь начинает работу")
    s_files = [
        [common_config_file, "войсковой части"]
        , [soldier_config_file, "военнослужащего"]
    ]
    for f in s_files:
        if not check_settings_file(f[0], f[1]):
            return

    js_settings = json.load(open(common_config_file, encoding='UTF8'))
    js_settings.update(json.load(open(soldier_config_file, encoding='UTF8')))
    add_fields_json(js_settings)
    data_model = create_from_json(js_settings)
    if not data_model[MODEL_IS_VALID]:
        print("Файл настроек содержит неверную информацию. Выполнение программы прервано.")
        return

    # set up logging
    log_folder_full_path = os.path.join(data_model[MODEL_OUTPUT_FOLDER], "logs")
    if not os.path.exists(log_folder_full_path):
        os.makedirs(log_folder_full_path)
    log_full_path = os.path.join(log_folder_full_path, "log-" + datetime.now().strftime("%d-%m-%Y-%H-%M-%S") + ".txt")
    logger = logging.getLogger("app")
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(log_full_path, encoding='UTF8')
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s] %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    doc = None
    if report_type == OFFICIAL_PROCEEDING_BATCH:
        doc = BatchOfficialProceeding(data_model)
    if report_type == DESERT_UNIT_BATCH:
        doc = BatchDesertUnit(data_model)
    if report_type == MASS_HR_INFO_BATCH:
        doc = BatchMassHrInfo(data_model)
    if report_type == MASS_PERFORMANCE_CHARACTERISTICS_BATCH:
        doc = BatchMassPerformanceCharacteristics(data_model)
    if report_type == UTILITY_BIRTHDAYS:
        doc = UtilityBirthday(data_model)
    if report_type == UTILITY_PERSONNEL_DETAILS_CHECK:
        doc = UtilityPersonnelDetailsCheck(data_model)
    if report_type == UTILITY_PERSONNEL_DETAILS_SORTING:
        doc = UtilityPersonnelDetailsSorting(data_model)
    if report_type == DIARY:
        doc = BatchDiary(data_model)
    if report_type == QUEST_ARRIVAL:
        doc = BatchQuestArrival(data_model)
    if report_type == UTILITY_PERSONNEL_DETAILS_SORTING_POSITION:
        doc = UtilityPersonnelDetailsSortingPosition(data_model)

    pers_storage = PersonnelStorage(data_model)
    if not pers_storage.is_valid:
        log("Неверная структура Штатного расписания/Информации о личном составе. Выполнение программы прервано.")
        return

    is_box = report_type == BOX_PROCESSING

    if doc is None and not is_box:
        log("Не удалось определить тип документа. Выполнение программы прервано.")
        return

    sold_ids = data_model[MODEL_JSON_OBJECT]["soldier_ids"].split(",")
    soldiers = []
    for sld in sold_ids:
        if "-" in sld:
            tkn = sld.split("-")
            if len(tkn) == 2:
                for i in range(int(tkn[0]), int(tkn[1]) + 1):
                    soldiers.append(i)
        else:
            soldiers.append(int(sld))
    if len(soldiers) == 0:
        log(f"Не заданы номера военнослужащих. В настроечном файле в поле 'soldier_ids' внесите их номера из "
            f"штатного расписания (первый столбец). Выполнение программы прервано.")
        return

    if doc is not None:
        doc.data_model["pers_storage"] = pers_storage
        log(f"Выполняется: {doc.get_name()}.")

    if not is_box and doc.is_utility():
        doc.render()
    else:
        for sld in soldiers:
            current_soldier = pers_storage.find_person_by_id(sld)
            if current_soldier is None:
                log(f"Не удалось найти военнослужащего под номером '{str(sld)}'")
                continue

            data_model[MODEL_CURRENT_SOLDIER] = current_soldier
            log(f"Документ для военнослужащего: {current_soldier.full_name}")
            if is_box:
                processor = TemplateProcessor(data_model, pers_storage)
                processor.process()
            else:
                doc.render()

    log("Писарь завершил работу")


def add_fields_json(js):
    fields = ["nationality", "gender", "education", "graduation_place", "specialization", "occupation",
              "foreign_languages", "awards", "government_authority", "foreign_countries_visited", "service_started",
              "place_of_birth", "home_address", "passport", "marital_status", "criminal_status", "father_name",
              "mother_name"]
    for f in fields:
        js[f] = ""

if __name__ == '__main__':
    if len(sys.argv) == 2:
        common_config = "report-settings/common_info.json"
        soldier_config = "report-settings/soldier_info.json"
        run_generation(common_config, soldier_config, sys.argv[1])
