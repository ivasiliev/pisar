import random
from openpyxl import Workbook

file_name = "personnel_data_massive.xlsx"

surnames = ["Петров", "Крикунов", "Лещенко", "Исаев", "Кораблев", "Курбатов", "Магомедов", "Козлов", "Кошкин", "Ягудин",
            "Божко", "Сурков", "Щипачев", "Пархоменко", "Гладков", "Тюряев", "Васильев", "Монастырский", "Брежнев",
            "Шарапов", "Косенко", "Даутов", "Скрипалев", "Калинин", "Жуков", "Уткин", "Лебедев", "Конев", "Рублев"]
names = ["Иван", "Петр", "Николай", "Илья", "Евгений", "Егор", "Валерий", "Алексей", "Александр", "Михаил", "Дмитрий",
         "Анатолий", "Владимир", "Игорь", "Олег", "Глеб"]
second_names = ["Иванович", "Петрович", "Николаевич", "Ильич", "Евгеньевич", "Егорович", "Валерьевич", "Алексеевич",
                "Александрович", "Дмитриевич", "Анатольевич", "Владимирович", "Игоревич", "Олегович"]
ranks = ["рядовой", "сержант", "младший лейтенант", "лейтенант", "старший лейтенант", "капитан"]
positions = ["стрелок", "гранатометчик", "пулеметчик", "радист"]
sheet_titles = ["№ п/п", "Подразделение", "Рота", "Взвод", "Отделение", "Воинская должность",
                "Воинское звание фактическое", "ФИО", "Дата рождения"]

max_persons_count = 2000
max_company_count = 2
max_platoon_count = 3
max_squad_count = 4

min_year_birth = 1965
max_year_birth = 2003

def get_random(arr):
	return arr[random.randint(0, len(arr) - 1)]


if __name__ == '__main__':
	wb = Workbook()
	sheet = wb.worksheets[0]
	sheet.title = "ШДС"
	for x in range(1, len(sheet_titles) + 1):
		sheet.cell(row=1, column=x, value=sheet_titles[x - 1])

	current_person_id = 0
	random.seed()
	print(f"Генерация {max_persons_count} военнослужащих...")
	while current_person_id < max_persons_count:
		current_person_id = current_person_id + 1

		company = random.randint(1, max_company_count)
		platoon = random.randint(1, max_platoon_count)
		squad = random.randint(1, max_squad_count)

		rank = get_random(ranks)
		position = get_random(positions)

		surname = get_random(surnames)
		name = get_random(names)
		second_name = get_random(second_names)
		full_name = f"{surname} {name} {second_name}"

		day = random.randint(1, 25)
		month = random.randint(1, 12)
		year = random.randint(min_year_birth, max_year_birth)
		date_birth = f"{day}.{month}.{year}"

		values_to_add = [str(current_person_id), "", str(company), str(platoon), str(squad), position, rank, full_name, date_birth]

		for col_ind in range(0, len(values_to_add)):
			sheet.cell(row=current_person_id + 1, column=col_ind + 1, value=values_to_add[col_ind])

		if current_person_id % 50 == 0:
			print(f" Обработано {current_person_id} записей...")
	file_to_save = f"c:\\pisar_data\\{file_name}"
	wb.save(file_to_save)
	print(f"Файл сохранен: {file_to_save}")
