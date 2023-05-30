# ДОКУМЕНТ
# СЛУЖЕБНОЕ РАЗБИРАТЕЛЬСТВО по факту грубого дисциплинарного проступка
from classes.document_in_report import DocumentInReport
# from classes.paragraph_settings import ParagraphSettings


class DocOfficialProceeding(DocumentInReport):
	def get_name(self):
		return "Служебное разбирательство по факту грубого дисциплинарного проступка"

	def get_name_for_file(self):
		return f"Служебное_Разбирательство_ГДП_СОЧ ({self.get_soldier_info().full_name}).docx"

	def render(self):
		# TODO order and list of documents should be customizable
		self.render_page_title()
		self.word_document.add_page_break()
		self.inventory_page()
		self.word_document.add_page_break()
		# TODO tabs in reports
		self.report1_page()
		self.word_document.add_page_break()
		self.report2_page()
		self.word_document.add_page_break()
		self.report3_page()
		self.word_document.add_page_break()
		self.conclusion_page()

		super().render()

	# Титульный лист (стр 1)
	def render_page_title(self):
		s_info = self.get_soldier_info()
		rep_settings = self.get_report_settings()

		self.add_empty_paragraphs(13)
		self.add_paragraph("СЛУЖЕБНОЕ РАЗБИРАТЕЛЬСТВО", self.bold_center_settings)
		self.add_empty_paragraphs(1)
		self.add_paragraph("по факту грубого дисциплинарного проступка", self.bold_center_settings)

		sold_str = self.get_person_full_str(s_info, rep_settings, 2, True, True, False, False)

		self.add_paragraph(
			sold_str,
			self.bold_center_settings)
		self.add_empty_paragraphs(18)

		# TODO year should be changeable
		# TODO finish this piece
		# ds = rep_settings["date_started"]
		# df = rep_settings["date_finished"]

		# if ds is not None:

		self.add_paragraph("Начато «     » _________ 2023 г.", self.align_right_settings)
		self.add_paragraph("Окончено «     » _________ 2023 г.", self.align_right_settings)

	# Опись (стр 2)
	def inventory_page(self):
		rep_settings = self.get_report_settings()
		commander = rep_settings["commander_2_level"]

		self.add_paragraph("О П И С Ь", self.align_center_settings)
		self.add_paragraph("документов, находящихся в материалах служебного разбирательства",
		                   self.align_center_settings)
		self.add_empty_paragraphs(1)

		captions = ["№ п/п", "Название документа", "Номер листов"]
		rows_data = ["Рапорт ВРИО командира 2 СБ"
			, "Рапорт ВРИО ЗКБ по ВПР 2 СБ"
			, "Рапорт ВРИО командира 5 СР 2 СБ"
			, "Объяснение сослуживца"
			, "Объяснение сослуживца"
			, "Объяснение сослуживца"
			, "Протокол о грубом дисциплинарном проступке"
			, "Акт о невозможности получения копии протокола о грубом дисциплинарном проступке"
			, "Акт о невозможности взять объяснение по факту действий совершенных военнослужащим, в которых усматривается преступление против военной службы"
			, "Служебная характеристика"
			, "Заключение служебного разбирательства"]

		self.add_table(28, captions, rows_data)
		self.add_empty_paragraphs(1)
		self.add_paragraph_left_right("Опись составил:", commander["position"])
		pst = ""
		if rep_settings["is_guard"]:
			pst = "гвардии "
		pst = pst + commander["rank"]
		self.add_paragraph(pst, self.align_center_settings)
		self.add_paragraph(self.get_person_name_short_format_1(commander["name"]), self.align_right_settings)

	# Рапорт 1 (стр 3)
	def report1_page(self):
		s_info = self.get_soldier_info()
		rep_settings = self.get_report_settings()
		commander = rep_settings["commander_3_level"]
		date_of_event = rep_settings["date_of_event"]

		self.add_paragraph("Командиру войсковой части " + rep_settings["military_unit"], self.align_right_settings)
		self.add_empty_paragraphs(5)
		self.add_paragraph("Р а п о р т", self.align_center_settings)
		self.add_empty_paragraphs(1)
		ps = "Настоящим докладываю, что"
		ps = f"{ps} {self.get_date_format_1(rep_settings['date_of_event'])} "

		sold_str = self.get_person_full_str(s_info, rep_settings, 0, False, False, True, True)

		ps = ps + sold_str + ", самовольно покинул расположение воинской части, не уведомив вышестоящее командование."
		self.add_paragraph(ps, self.ident_align_justify_settings)
		self.add_paragraph("Прошу Вашего указания на проведение административного расследования по данному факту.",
		                   self.ident_align_justify_settings)
		self.add_empty_paragraphs(2)
		self.add_paragraph(commander["position"], self.align_right_settings)

		rnk = commander["rank"]
		if rep_settings["is_guard"]:
			rnk = "гвардии " + rnk

		self.add_paragraph(rnk, self.align_center_settings)
		self.add_paragraph(self.get_person_name_short_format_1(commander["name"]), self.align_right_settings)

		self.add_paragraph(date_of_event, self.align_left_settings)

	# Рапорт 2 (стр 4)
	def report2_page(self):
		s_info = self.get_soldier_info()
		rep_settings = self.get_report_settings()
		commander = rep_settings["commander_2_level"]
		date_of_event = rep_settings["date_of_event"]

		self.add_paragraph("Командиру 2 СБ", self.align_right_settings)
		self.add_empty_paragraphs(5)
		self.add_paragraph("Р а п о р т", self.align_center_settings)
		self.add_empty_paragraphs(1)

		ps = "Настоящим докладываю, что в ходе проведения розыскных мероприятий розыскной группой из числа " \
		     "военнослужащих 2 стрелкового батальона под моим руководством место нахождения "

		sold_str = self.get_person_full_str(s_info, rep_settings, 1, False, False, True, False)

		ps = ps + sold_str + " установить не удалось."

		self.add_paragraph(ps, self.ident_align_justify_settings)
		self.add_empty_paragraphs(2)
		self.add_paragraph(commander["position"], self.align_right_settings)

		rnk = commander["rank"]
		if rep_settings["is_guard"]:
			rnk = "гвардии " + rnk

		self.add_paragraph(rnk, self.align_center_settings)
		self.add_paragraph(self.get_person_name_short_format_1(commander["name"]), self.align_right_settings)

		self.add_paragraph(date_of_event, self.align_left_settings)

	# Рапорт 3 (стр 5)
	def report3_page(self):
		s_info = self.get_soldier_info()
		rep_settings = self.get_report_settings()
		commander = s_info.company_commander
		date_of_event = rep_settings["date_of_event"]

		self.add_paragraph("Командиру 2 СБ", self.align_right_settings)
		self.add_empty_paragraphs(5)
		self.add_paragraph("Р а п о р т", self.align_center_settings)
		self.add_empty_paragraphs(1)

		ps = f"Настоящим докладываю, что {self.get_date_format_1(rep_settings['date_of_event'])} был выявлен факт " \
		     f"отсутствия на месте несения службы"

		sold_str = self.get_person_full_str(s_info, rep_settings, 1, False, False, True, False)

		ps = f"{ps} {sold_str}."
		ps = ps + " На телефонные звонки не отвечает, настоящее местонахождение не известно."

		self.add_paragraph(ps, self.ident_align_justify_settings)
		self.add_empty_paragraphs(2)

		c_name = "[ФИО РОТНОГО КОМАНДИРА]"
		c_rank = "[ЗВАНИЕ РОТНОГО КОМАНДИРА]"
		c_position = "[ДОЛЖНОСТЬ РОТНОГО КОМАНДИРА]"

		if len(commander) > 0:
			c_name = self.get_person_name_short_format_1(commander["name"])
			c_rank = commander["rank"]
			if rep_settings["is_guard"]:
				c_rank = "гвардии " + c_rank
			c_position = commander["position"]

		self.add_paragraph(c_position, self.align_right_settings)
		self.add_paragraph(c_rank, self.align_center_settings)
		self.add_paragraph(c_name, self.align_right_settings)

		self.add_paragraph(date_of_event, self.align_left_settings)

	# Заключение (стр 6 и 7)
	def conclusion_page(self):
		s_info = self.get_soldier_info()
		commander_company_info = s_info.company_commander
		rep_settings = self.get_report_settings()
		commander = rep_settings["commander_3_level"]
		date_of_event = rep_settings["date_of_event"]

		self.add_paragraph(f"Командиру войсковой части {rep_settings['military_unit']}", self.align_right_settings)
		self.add_empty_paragraphs(3)
		self.add_paragraph("ЗАКЛЮЧЕНИЕ", self.bold_center_settings)
		self.add_paragraph("по материалам служебного разбирательства", self.bold_center_settings)
		self.add_paragraph("по факту грубого дисциплинарного проступка", self.bold_center_settings)
		self.add_paragraph(f"военнослужащим 2 стрелкового батальона войсковой части {rep_settings['military_unit']}",
		                   self.bold_center_settings)

		rnk = s_info.rank
		if rep_settings["is_guard"]:
			rnk = "гвардии " + self.get_word_ablt(rnk)

		self.add_paragraph(f"{rnk} {self.get_person_name_instr(s_info.full_name)}", self.bold_center_settings)
		self.add_empty_paragraphs(1)

		# TODO what the date?
		self.add_paragraph_left_right("16.04.2023 г.", "г. Донецк")
		self.add_empty_paragraphs(2)

		# TODO ВРИО -> временно исполняющим обязанности. long_position?
		txt1 = f"Мной, временно исполняющим обязанности командира 2 стрелкового батальона войсковой части {rep_settings['military_unit']} "

		rnk = commander["rank"]
		if rep_settings["is_guard"]:
			rnk = "гвардии " + self.get_word_ablt(rnk)

		txt1 = txt1 + f"{rnk} {self.get_person_name_instr(commander['name'])},"
		txt1 = txt1 + " проведено служебное разбирательство по факту самовольного оставления части"
		sold_str = self.get_person_full_str(s_info, rep_settings, 2, False, False, True, True)
		self.add_paragraph(f"{txt1} {sold_str}.", self.ident_align_justify_settings)

		txt2 = f"В ходе проведения служебного разбирательства было установлено, что {self.get_date_format_1(rep_settings['date_of_event'])}"
		sold_str = self.get_person_full_str(s_info, rep_settings, 0, False, False, True, False)
		txt2 = f"{txt2} {sold_str} самовольно покинул расположение части не уведомив вышестоящее командование."
		self.add_paragraph(txt2, self.ident_align_justify_settings)

		rnk = s_info.rank
		if rep_settings["is_guard"]:
			rnk = "гвардии " + self.get_word_gent(rnk)

		txt3 = "Проведенные розыскные мероприятия, опрос сослуживцев, поиск в лечебных учреждениях, " \
		       "военных комендатурах, а также отделениях полиции"
		txt3 = f"{txt3} {rnk} {self.get_person_name_gent(s_info.full_name)} результата не дали, установить причины " \
		       f"отсутствия военнослужащего, а также его местонахождение не удалось."

		self.add_paragraph(txt3, self.ident_align_justify_settings)
		self.add_paragraph("Причинами данного правонарушения явились:", self.ident_align_justify_settings)

		txt4 = "невыполнение требований статьи 144, 145 Устава Внутренней Службы Вооруженных Сил Российской Федерации в " \
		       "части, касающейся воспитания, поддержания воинской дисциплины, морально–психологического состояния " \
		       "личного состава в роте, а также в части касающееся знаний деловых и морально–психологических качеств и " \
		       "особенностей всех военнослужащих роты, постоянного проведения с ними индивидуальной работы по воинскому " \
		       "воспитанию"

		commander_company_text1 = self.get_commander_company_full_str(commander_company_info, rep_settings, 2)

		self.add_paragraph(f"{txt4} {commander_company_text1};", self.ident_align_justify_settings)

		sold_str = self.get_person_full_str(s_info, rep_settings, 1, False, False, True, False)
		self.add_paragraph("невыполнение требований статьи 160, 161 Устава Внутренней Службы Вооруженных Сил "
		                   "Российской Федерации в части, касающейся точного и своевременного исполнения возложенных "
		                   f"на него обязанностей, поставленных задач и личная недисциплинированность {sold_str}.",
		                   self.ident_align_justify_settings)

		rnk = s_info.rank
		if rep_settings["is_guard"]:
			rnk = "гвардии " + rnk

		p1 = self.add_paragraph(
			f"Исходя из материала служебного разбирательства следует, что {rnk} {s_info.full_name} "
			"самовольно покинул расположение части, за что в соответствии со статьей «337» "
			"Уголовного кодекса Российской Федерации предусматривается уголовная ответственность, "
			"на основании вышеизложенного ", self.ident_align_justify_settings)
		runner = p1.add_run("ПРЕДЛАГАЮ:")
		runner.bold = True

		commander_company_text2 = self.get_commander_company_full_str(commander_company_info, rep_settings, 3)

		txt5 = "за невыполнение требований статьи 144, 145 Устава Внутренней Службы Вооруженных Сил Российской " \
		       "Федерации в части, касающейся воспитания, поддержания воинской дисциплины, морально–психологического " \
		       "состояния личного состава в роте, а также в части касающееся знаний деловых и морально–психологических " \
		       "качеств и особенностей всех военнослужащих роты, постоянного проведения с ними индивидуальной работы " \
		       "по воинскому воспитанию, строго указать на УПУЩЕНИЕ ПО СЛУЖБЕ."

		self.add_paragraph(f"{commander_company_text2} {txt5}", self.ident_align_justify_settings)

		sold_str = self.get_person_full_str(s_info, rep_settings, 3, False, False, True, False)
		# TODO use just one variable txt
		txt4 = f"2. {sold_str} за грубый дисциплинарный проступок самовольное оставление части более 4 (четырех) часов, объявить СТРОГИЙ ВЫГОВОР."

		self.add_paragraph(txt4, self.ident_align_justify_settings)
		self.add_empty_paragraphs(2)
		self.add_paragraph(commander["position"], self.align_center_settings)

		rnk = commander["rank"]
		if rep_settings["is_guard"]:
			rnk = "гвардии " + rnk

		self.add_paragraph(rnk, self.align_center_settings)
		self.add_empty_paragraphs(2)

		self.add_paragraph_left_right(date_of_event, self.get_person_name_short_format_1(commander["name"]))

	# declension_type. 0 (without), 1 (gent), 2 (ablt), 3 (datv)
	def get_person_full_str(self, s_info, rep_settings, declension_type, battalion_only, militaryman_required,
	                        position_required, dob_required):
		sld_position = ""  # if not required
		if militaryman_required:
			sld_position = self.get_word_declension("военнослужащий", declension_type)
		else:
			if position_required:
				sld_position = self.get_word_declension(s_info.position, declension_type)

		sld_rank = self.get_word_declension(s_info.rank, declension_type)
		if rep_settings["is_guard"]:
			sld_rank = "гвардии " + sld_rank

		# TODO battalion must be a variable
		address = "2 стрелкового батальона войсковой части " + rep_settings["military_unit"]
		if not battalion_only:
			address = f"{s_info.squad} стрелкового отделения {s_info.platoon} стрелкового взвода {s_info.company} стрелковой роты " + address

		full_name = self.get_person_name_declension(s_info.full_name, declension_type)

		dob_str = ""
		if dob_required:
			dob_str = self.get_date_format_1(s_info.dob_string) + " рождения"

		result = f"{sld_position} {address} {sld_rank} {full_name}"
		if len(dob_str) > 0:
			result = result + " " + dob_str
		return result

	def get_commander_company_full_str(self, commander_company_info, rep_settings, declension_type):
		text = "[ВСТАВЬТЕ СВЕДЕНИЯ О КОМАНДИРЕ РОТЫ]"
		if len(commander_company_info) > 0:
			c_name = commander_company_info["name"]
			c_rank = commander_company_info["rank"]
			if rep_settings["is_guard"]:
				c_rank = "гвардии " + self.get_word_declension(c_rank, declension_type)
			c_position = commander_company_info["position"]

			# TODO more intelligent algorithm for position declension


			m_unit = rep_settings["military_unit"]
			c_company = commander_company_info["company"]
			text = f"{self.get_word_declension(c_position, declension_type)} {c_company} стрелковой роты 2 стрелкового батальона войсковой части {m_unit} {c_rank} {self.get_person_name_declension(c_name, declension_type)}"
		return text
