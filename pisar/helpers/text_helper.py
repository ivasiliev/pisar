def decode_acronyms(morph, position, declension_type):
	if position is None or len(position) == 0:
		return ""
	# pairs text -- index of word for declension
	acronyms = {
		"врио": ["временно исполняющий обязанности", 1]
		, "ср": ["стрелковая рота", -1]
		, "сб": ["стрелковый батальон", -1]
	}

	result = ""
	words = position.split(" ")
	for wrd in words:
		word = wrd.lower()
		if word in acronyms:
			word_acr_info = acronyms[word]
			word_index = word_acr_info[1]
			# if there is no special index of word, then convert all words
			words_acr_all = word_acr_info[0].split(" ")
			if word_index == -1:
				for words_acr_all_each in words_acr_all:
					result = result + " " + get_word_declension(morph, words_acr_all_each, 1)
			else:
				current_index = 0
				for words_acr_all_each in words_acr_all:
					if current_index == word_index:
						result = result + " " + get_word_declension(morph, words_acr_all_each, declension_type)
					else:
						result = result + " " + words_acr_all_each
					current_index = current_index + 1
		else:
			result = result + " " + word

	return result.strip()


def get_word_routines(morph, wrd, grm):
	if morph is None:
		print("Внутренняя ошибка. Морфоанализатор не создан.")
		return ""
	parsed = morph.parse(wrd)[0]
	gent_text = parsed.inflect({grm})
	return gent_text.word


def get_word_gent(morph, wrd):
	return get_word_routines(morph, wrd, "gent")


def get_word_ablt(morph, wrd):
	return get_word_routines(morph, wrd, "ablt")


def get_word_datv(morph, wrd):
	return get_word_routines(morph, wrd, "datv")


def get_word_declension(morph, wrd, declension_type):
	if declension_type == 0:
		result = wrd
	else:
		if declension_type == 1:
			result = get_word_gent(morph, wrd)
		else:
			if declension_type == 2:
				result = get_word_ablt(morph, wrd)
			else:
				if declension_type == 3:
					result = get_word_datv(morph, wrd)
				else:
					result = wrd

	return result
