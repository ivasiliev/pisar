import pymorphy2

from helpers.text_helper import decode_acronyms

if __name__ == '__main__':
	morph = pymorphy2.MorphAnalyzer()

	positions = ["ВрИО Командира 6 СР 2 СБ"
		, "ВрИО заместителя командира 6 СР 2 СБ по военно-воспитательной работе"
		, "ВрИО старшего офицера батареи 1 противотанкового артиллерийского взвода противотанковой артиллерийской батареи 2 Стрелкового батальона"]

	for position in positions:
		print(f"position={position}")
		declension_type = 0
		while declension_type <= 3:
			position_without_acronyms = decode_acronyms(morph, position, declension_type)
			print(f"declension_type={declension_type}: {position_without_acronyms}")
			declension_type = declension_type + 1
		print("")
