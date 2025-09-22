from classes.personnel_storage import EXCEL_DOCUMENT_SR
from helpers.log_helper import log
from utils.utility_prototype import UtilityPrototype


class UtilitySrSqlGeneration(UtilityPrototype):
    def __init__(self, data_model):
        super().__init__(data_model)

    def get_name(self):
        return "Генерация SQL для импорта ШР в БД"

    def render(self):

        # проходит по всем записям ШР
        # каждого человека записывает в PEOPLE
        # каждого человека записывает в SR
        # набор полей с должностями для каждого человека записывает в POSITION_DICT (может быть несколько строчек с одинаковыми должностями)

        inserts = ["BEGIN TRY", "BEGIN TRANSACTION;"]

        pers_storage = self.get_pers_storage()
        persons_sr = pers_storage.get_all_persons(EXCEL_DOCUMENT_SR)

        log(f"Количество людей в ШР (без ограничений): {len(persons_sr)}...")

        for pers in persons_sr:
            insert = f"INSERT INTO PEOPLE (ID, FULL_NAME, BIRTH_DATE, GENDER, MARITAL_STATUS, EDUCATION, OCCUPATION, ADDRESS, PHONE, EMAIL) VALUES ('{pers.id}', '{pers.full_name}', '{pers.dob}', '{pers.gender}', '{pers.marital_status}', '{pers.education}', '{pers.occupation}', '{pers.address}', '{pers.phone}', '{pers.email}');"
            inserts.append(insert)



        # finalize script
        inserts.append("COMMIT TRANSACTION;")
        inserts.append("END TRY;")
        inserts.append("BEGIN CATCH")
        inserts.append("IF @@TRANCOUNT > 0")
        inserts.append("ROLLBACK TRANSACTION;")
        inserts.append("THROW;")
        inserts.append("END CATCH;")

