from pathlib import Path

from classes.personnel_storage import EXCEL_DOCUMENT_SR
from helpers.log_helper import log
from utils.utility_prototype import UtilityPrototype


class UtilitySrSqlGeneration(UtilityPrototype):
    def __init__(self, data_model):
        super().__init__(data_model)

    def get_name(self):
        return "Генерация SQL для импорта ШР в БД"

    def parse_full_simple(self, full: str):
        if full is None:
            return '', '', ''
        tokens = full.strip().split()
        if not tokens:
            return '', '', ''
        surname = tokens[0] if len(tokens) >= 1 else ''
        name = tokens[1] if len(tokens) >= 2 else ''
        father = ' '.join(tokens[2:]) if len(tokens) >= 3 else ''
        return surname, name, father

    def render(self):

        # проходит по всем записям ШР
        # каждого человека записывает в PEOPLE
        # каждого человека записывает в SR
        # набор полей с должностями для каждого человека записывает в POSITION_DICT (может быть несколько строчек с одинаковыми должностями)

        inserts = ["BEGIN TRY", "BEGIN TRANSACTION;"]

        null= "NULL"
        output_file = "c:\\pisar_output\\sr.sql"

        pers_storage = self.get_pers_storage()
        persons_sr = pers_storage.get_all_persons(EXCEL_DOCUMENT_SR)

        log(f"Количество людей в ШР (без ограничений): {len(persons_sr)}")

        id_entity = 1
        for pers in persons_sr:
            if pers.full_name is  None:
                log(f"ШР. Строка {id_entity} содержит пустое ФИО. Выполнение программы прервано.")
                return

            surname, name, father_name = self.parse_full_simple(pers.full_name)

            if surname is None or name is None:
                log(f"ШР. Строка {id_entity}, пустые фамилия и имя. Это обязательные поля. Выполнение программы прервано.")
                return

            if pers.dob is None:
                dob = null
            else:
                dob = f"{pers.dob.isoformat()}"

            if pers.unique is None:
                log(f"ШР. Строка {id_entity} содержит пустой Личный номер. Выполнение программы прервано.")
                return

            if pers.full_position_name is None or pers.short_position_name is None or pers.position_name is None or pers.unit is None or pers.unit2 is None or pers.platoon is None or pers.squad is None or pers.military_position is None:
                log(f"ШР. Строка {id_entity}, все поля касательно должностей являются обязательными. Выполнение программы прервано.")
                return


            # PEOPLE

            # TODO define gender
            insert_people = f"INSERT INTO PEOPLE (ID, [SURNAME], [NAME], FATHER_NAME, [DOB], GENDER) VALUES ({str(id_entity)}, '{surname}', '{name}', '{father_name}', {dob}, 0);"
            inserts.append(insert_people)

            # POSITION_LIST
            insert_position = f"INSERT INTO PEOPLE (ID, [POSITION_FULL], [POSITION_SHORT], [POSITION], [UNIT1],	[UNIT2], [PLATOON],	[SQUAD], [MILITARY_POSITION]) VALUES ({str(id_entity)}, '{surname}', '{name}', '{father_name}', {dob}, 0);"
            inserts.append(insert_position)

            # SR


            id_entity = id_entity + 1


        # finalize script
        inserts.append("COMMIT TRANSACTION;")
        inserts.append("END TRY;")
        inserts.append("BEGIN CATCH")
        inserts.append("IF @@TRANCOUNT > 0")
        inserts.append("ROLLBACK TRANSACTION;")
        inserts.append("THROW;")
        inserts.append("END CATCH;")

        out_path = Path(output_file)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text("\n".join(inserts) + ("\n" if inserts else ""), encoding="utf-8")

