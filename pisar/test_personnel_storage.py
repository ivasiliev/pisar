import pymorphy2
from classes.personnel_storage import PersonnelStorage
from pytrovich.enums import NamePart, Gender, Case
from pytrovich.maker import PetrovichDeclinationMaker

if __name__ == '__main__':
	full_path = "data\\personnel-demo.xlsx"
	pers_storage = PersonnelStorage(full_path)
	person = pers_storage.find_person_by_id(1)
	assert person is not None
	print(person.company_commander)

	morph = pymorphy2.MorphAnalyzer()
	print(f"position = {person.position}")
	parsed = morph.parse(person.position)[0]
	gent_text = parsed.inflect({'gent'})
	print(f"gent_text={gent_text.word}")
	datv_text = parsed.inflect({'datv'})
	print(f"datv_text={datv_text.word}")

	nationality = "русский"
	parsed = morph.parse(nationality)[0]
	print(f"datv_text={parsed.inflect({'datv'}).word}")

	commander_text = "временно исполняющий обязанности командира"
	parsed = morph.parse(commander_text)[0]
	gent_text = parsed.inflect({'gent'})
	print(f"gent_text={gent_text.word}")
	datv_text = parsed.inflect({'datv'})
	print(f"datv_text={datv_text.word}")

	maker = PetrovichDeclinationMaker()

	name_tokens = person.full_name.split(" ")
	surname = name_tokens[0]
	first_name = name_tokens[1]
	middle_name = name_tokens[2]
	cs = Case.INSTRUMENTAL
	print(maker.make(NamePart.LASTNAME, Gender.MALE, cs, surname))
	print(maker.make(NamePart.FIRSTNAME, Gender.MALE, cs, first_name))
	print(maker.make(NamePart.MIDDLENAME, Gender.MALE, cs, middle_name))


	# parsed = morph.parse(t)[0]
	# print(f"parsed={parsed}")
	# lex = parsed.lexeme
	# print(f"lex={lex}")
	# gent_text = parsed.inflect({'gent'})
	# print(f"gent_text={gent_text.word}")



