import datetime
from pathlib import Path

from helpers.log_helper import log
from utils.utility_prototype import UtilityPrototype


class UtilitySrSqlGeneration(UtilityPrototype):
    def __init__(self, data_model):
        super().__init__(data_model)
        self.generation_log_messages = []
        self.null = "NULL"

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

    def log_ex(self, message):
        log(message)
        self.generation_log_messages.append(message)

    def is_none_or_blank(self,s):
        return s is None or s.strip() == ""

    def get_date(self, ds, id_entity):
        if self.is_none_or_blank(ds):
            return self.null
        try:
            dt = datetime.datetime.strptime(ds, "%d.%m.%Y").date()
        except ValueError as e:
            self.log_ex(f"Строка {id_entity} неправильный формат даты '{ds}': должен быть 'ДД.ММ.ГГГГ'. Выполнение программы прервано.")
            raise ValueError(f"Неправильный формат даты '{ds}': должен быть 'ДД.ММ.ГГГГ'") from e
        return f"{dt.isoformat()}"

    def render(self):

        # проходит по всем записям ШР
        # каждого человека записывает в PEOPLE
        # каждого человека записывает в SR
        # набор полей с должностями для каждого человека записывает в POSITION_DICT (может быть несколько строчек с одинаковыми должностями)

        inserts = ["use [pisar]", "GO", "BEGIN TRY", "BEGIN TRANSACTION;"]

        output_file_sql = "c:\\pisar_output\\sr.sql"
        output_file_log = "c:\\pisar_output\\sr-generation.txt"

        # read all the people
        pers_storage = self.get_pers_storage()
        all_persons = pers_storage.load_all_persons_data()
        if all_persons is None:
            return

        self.log_ex(f"Количество людей в ЛС (ограничение строк не применяется): {len(all_persons)}")
        self.log_ex(f"Из них есть в ШР: {len(list(filter(lambda o: o.exists_sr, all_persons)))}")

        # this is a Person object
        for pers in all_persons:

            self.log_ex(f"Читаем информацию на позиции {pers.id_sr}...")
            if pers.full_name is None:
                self.log_ex(f"Строка содержит пустое ФИО. Выполнение программы прервано.")
                return

            surname, name, father_name = self.parse_full_simple(pers.full_name)

            if surname is None or name is None:
                self.log_ex(f"Пустые фамилия и имя. Это обязательные поля. Выполнение программы прервано.")
                return

            if pers.dob is None:
                dob = self.null
            else:
                dob = f"{pers.dob.isoformat()}"

            if pers.unique is None:
                self.log_ex(f"Пустой Личный номер. Выполнение программы прервано.")
                return

            if pers.full_position_name is None or pers.short_position_name is None or pers.position_name is None or pers.unit is None or pers.unit2 is None or pers.platoon is None or pers.squad is None or pers.military_position is None:
                self.log_ex(f"Все столбцы, связанные с должностями, являются обязательными. Выполнение программы прервано.")
                return

            inserts.append("---------------------------------------------------------")

            # it has its own data model object
            dm = pers.data_model

            # PEOPLE

            gender = dm["gender"]
            gender_num = -1
            if gender is None:
                self.log_ex(f"Пустой столбец Пол. Выполнение программы прервано.")
                return
            else:
                if gender.casefold() == "м".casefold():
                    gender_num = 0
                else:
                    if gender.casefold() == "м".casefold():
                        gender_num = 1
            if gender_num == -1:
                self.log_ex(f"Неверное значение для столбца 'Пол' (нужно 'м' или 'ж'). Выполнение программы прервано.")
                return

            # PEOPLE

            insert_people = f"INSERT INTO dbo.PEOPLE (ID, [SURNAME], [NAME], FATHER_NAME, [DOB], GENDER) VALUES ({pers.id_sr}, '{surname}', '{name}', '{father_name}', '{dob}', {gender_num});"
            inserts.append(insert_people)

            # LS

            rank = dm["rank"]
            citizenship = dm["citizenship"]
            nationality = dm["nationality"]
            height = dm["height"]
            weight = dm["weight"]
            education = dm["education"]
            graduation_place = dm["graduation_place"]
            specialization = dm["specialization"]
            occupation = dm["occupation"]
            foreign_languages = dm["foreign_languages"]
            foreign_countries_visited = dm["foreign_countries_visited"]
            awards = dm["awards"]
            # TODO wrong key
            is_deputy = dm["government_authority"]
            service_started_date = self.get_date(dm["service_started"], pers.id_sr)
            signs = dm["signs"]
            tatoo = dm["tatoo"]
            habits = dm["habits"]
            kia_mia_des = dm["status_kia_mia_des"]
            rank_assignment_date = self.get_date(dm["rank_assignment_date"], pers.id_sr)
            oath_date = self.get_date(dm["oath_date"], pers.id_sr)
            oath_type = dm["oath_type"]
            blood_type = dm["blood_type"]
            enrollment_date = self.get_date(dm["enrollment_date"], pers.id_sr)
            serve_vsu_2014 = dm["serve_vsu_2014"]
            incentives = dm["incentives"]
            penalties = dm["penalties"]
            plans_for_future = dm["plans_for_future"]
            contract_date_finish = self.get_date(dm["contract_date_finish"], pers.id_sr)
            bank_account = dm["bank_account"]
            address_memo = dm["address_memo"]
            social_networks = dm["social_networks"]
            family_members_count = dm["family_members_count"]
            children_count = dm["children_count"]
            place_of_birth = dm["place_of_birth"]

            insert_ls = f"INSERT INTO dbo.LS ([PEOPLE_ID],[PERSONAL_NUMBER],[RANK],[STATUS_KIA_MIA_DES_TEXT],[RANK_ASSIGNMENT_DATE],\
                        [OATH_DATE],[NATIONALITY],[CITIZENSHIP],[HEIGHT],[WEIGHT],[BLOOD_GROUP],[OATH_TYPE],[ENROLLMENT_DATE],[SERVE_VSU_2014],[INCENTIVES],\
                        [PENALTIES],[EDUCATION_TYPE],[EDUCATION_DETAILS],[PROFESSION],[PLACE_OF_WORK],[FOREIGN_LANGUAGES],[FOREIGN_COUNTRIES],[AWARDS],\
                        [PLANS_FOR_FUTURE],[CONTRACT_DATE_START],[CONTRACT_DATE_FINISH],[BANK_ACCOUNT],[POB],[ADDRESS_MEMO],[SOCIAL_NETWORKS],[IS_DEPUTY],\
                        [FAMILY_MEMBERS_COUNT],[CHILDREN_COUNT]) VALUES ({pers.id_sr},'{pers.unique}','{rank}','{kia_mia_des}','{rank_assignment_date}','{oath_date}','{nationality}','{citizenship}',{height},{weight},'{blood_type}','{oath_type}','{enrollment_date}','{serve_vsu_2014}','{incentives}','{penalties}','{education}','{graduation_place}','{specialization}','{occupation}','{foreign_languages}','{foreign_countries_visited}','{awards}','{plans_for_future}','{service_started_date}','{contract_date_finish}','{bank_account}','{place_of_birth}','{address_memo}','{social_networks}','{is_deputy}',{family_members_count},{children_count});"

            inserts.append(insert_ls)

            # RELATIVES

            # DOCUMENTS

            # if this person exists in SR

            if pers.exists_sr:

                # POSITION_LIST
                insert_position = f"INSERT INTO [dbo].[POSITION_DICT] (ID, [POSITION_FULL], [POSITION_SHORT], [POSITION], [UNIT1],	[UNIT2], [PLATOON],	[SQUAD], [MILITARY_POSITION]) VALUES ({pers.id_sr}, '{pers.full_position_name}', '{pers.short_position_name}', '{pers.position_name}', '{pers.unit}', '{pers.unit2}', '{pers.platoon}', '{pers.squad}', '{pers.military_position}');"
                inserts.append(insert_position)

                # SR
                insert_sr = f"INSERT INTO dbo.SR (ID, [PEOPLE_ID], [POSITION_ID]) VALUES ({pers.id_sr}, {pers.id_sr}, {pers.id_sr});"
                inserts.append(insert_sr)



        # finalize script
        inserts.append("COMMIT TRANSACTION;")
        inserts.append("END TRY")
        inserts.append("BEGIN CATCH")
        inserts.append("IF @@TRANCOUNT > 0")
        inserts.append("ROLLBACK TRANSACTION;")
        inserts.append("THROW;")
        inserts.append("END CATCH;")

        out_path_sql = Path(output_file_sql)
        out_path_sql.parent.mkdir(parents=True, exist_ok=True)
        out_path_sql.write_text("\n".join(inserts) + ("\n" if inserts else ""), encoding="utf-8")

        out_path_log = Path(output_file_log)
        out_path_log.write_text("\n".join(self.generation_log_messages) + ("\n" if self.generation_log_messages else ""), encoding="utf-8")

        self.log_ex(f"Генерация завершена. Файл SQL сохранён: {output_file_sql}. Журнал событий сохранён: {output_file_log}")
