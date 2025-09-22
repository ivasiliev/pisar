

class UtilitySrSqlGeneration(UtilityPrototype):
    def get_name(self):
        return "Генерация SQL-кода для импорта ШР в БД"

    def render(self):

        # проходит по всем записям ШР
        # каждого человека записывает в PEOPLE
        # каждого человека записывает в SR
        # набор полей с должностями для каждого человека записывает в POSITION_DICT (может быть несколько строчек с одинаковыми должностями)

        inserts: List[str] = []

        pers_storage = self.get_pers_storage()
        persons_sr_limited = pers_storage.get_all_persons(EXCEL_DOCUMENT_SR, rl)