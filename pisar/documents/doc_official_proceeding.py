# ДОКУМЕНТ
# СЛУЖЕБНОЕ РАЗБИРАТЕЛЬСТВО по факту грубого дисциплинарного проступка
from classes.document_in_report import DocumentInReport
from classes.paragraph_settings import ParagraphSettings


class DocOfficialProceeding(DocumentInReport):
	def get_name(self):
		return "Служебное разбирательство по факту грубого дисциплинарного проступка"

	def get_name_for_file(self):
		return "Служебное_Разбирательство_ГДП_СОЧ.docx"

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
		self.add_empty_paragraphs(13)
		self.add_paragraph("СЛУЖЕБНОЕ РАЗБИРАТЕЛЬСТВО", self.bold_center_settings)
		self.add_empty_paragraphs(1)
		self.add_paragraph("по факту грубого дисциплинарного проступка", self.bold_center_settings)
		self.add_paragraph(
			"военнослужащим 2 стрелкового батальона войсковой части 42600 гвардии рядовым Ивановым Иваном Ивановичем",
			self.bold_center_settings)
		self.add_empty_paragraphs(18)
		self.add_paragraph("Начато «     » _________ 2023 г.", self.align_right_settings)
		self.add_paragraph("Окончено «     » _________ 2023 г.", self.align_right_settings)

	# Опись (стр 2)
	def inventory_page(self):
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
			,
			         "Акт о невозможности взять объяснение по факту действий совершенных военнослужащим, в которых усматривается преступление против военной службы"
			, "Служебная характеристика"
			, "Заключение служебного разбирательства"]
		self.add_table(27, captions, rows_data)

		self.add_empty_paragraphs(1)
		# TODO fix left and right
		self.add_paragraph_left_right("Опись составил:", "ВРИО ЗКБ по ВПР 2 СБ")
		self.add_paragraph("гвардии лейтенант", self.align_center_settings)
		self.add_paragraph("С.Белич", self.align_right_settings)

	# Рапорт 1 (стр 3)
	def report1_page(self):
		self.add_paragraph("Командиру войсковой части 42600", self.align_right_settings)
		self.add_empty_paragraphs(5)
		self.add_paragraph("Р а п о р т", self.align_center_settings)
		self.add_empty_paragraphs(1)
		self.add_paragraph("Настоящим докладываю, что 16 апреля 2023 года пулеметчик 3 стрелкового отделения 3 "
		                   "стрелкового взвода 5 стрелковой роты 2 стрелкового батальона войсковой части 42600 гвардии "
		                   "рядовой Иванов Иван Иванович 26 июня 1997 года рождения, самовольно покинул расположение "
		                   "воинской части, не уведомив вышестоящее командование.", self.ident_align_justify_settings)
		self.add_paragraph("Прошу Вашего указания на проведение административного расследования по данному факту.",
		                   self.ident_align_justify_settings)
		self.add_empty_paragraphs(2)
		self.add_paragraph("ВРИО командира 2 СБ", self.align_right_settings)
		self.add_paragraph("гвардии подполковник", self.align_center_settings)
		self.add_paragraph("ФИО подполковника", self.align_right_settings)
		self.add_paragraph("16.04.2023 г.", self.align_left_settings)

	# Рапорт 2 (стр 4)
	def report2_page(self):
		self.add_paragraph("Командиру 2 СБ", self.align_right_settings)
		self.add_empty_paragraphs(5)
		self.add_paragraph("Р а п о р т", self.align_center_settings)
		self.add_empty_paragraphs(1)
		self.add_paragraph("Настоящим докладываю, что в ходе проведения розыскных мероприятий розыскной группой из "
		                   "числа военнослужащих 2 стрелкового батальона под моим руководством место нахождения "
		                   "пулеметчика 3 стрелкового отделения 3 стрелкового взвода 5 стрелковой роты 2 стрелкового "
		                   "батальона войсковой части 42600 гвардии рядового Иванова Ивана Ивановича установить не "
		                   "удалось.", self.ident_align_justify_settings)
		self.add_empty_paragraphs(2)
		self.add_paragraph("ВРИО ЗКБ по ВПР 2СБ", self.align_right_settings)
		self.add_paragraph("гвардии лейтенант", self.align_center_settings)
		self.add_paragraph("ФИО лейтенанта", self.align_right_settings)
		self.add_paragraph("16.04.2023 г.", self.align_left_settings)

	# Рапорт 3 (стр 5)
	def report3_page(self):
		self.add_paragraph("Командиру 2 СБ", self.align_right_settings)
		self.add_empty_paragraphs(5)
		self.add_paragraph("Р а п о р т", self.align_center_settings)
		self.add_empty_paragraphs(1)
		self.add_paragraph("Настоящим докладываю, что 16 апреля 2023 года был выявлен факт отсутствия на месте несения "
		                   "службы пулеметчика 3 стрелкового отделения3 стрелкового взвода 5 стрелковой роты 2 "
		                   "стрелкового батальона войсковой части 42600 гвардии рядового Иванова Ивана Ивановича. На "
		                   "телефонные звонки не отвечает, настоящее местонахождение не известно.",
		                   self.ident_align_justify_settings)
		self.add_empty_paragraphs(2)
		self.add_paragraph("ВРИО командира 5 СР 2 СБ", self.align_right_settings)
		self.add_paragraph("гвардии рядовой", self.align_center_settings)
		self.add_paragraph("ФИО рядового", self.align_right_settings)
		self.add_paragraph("16.04.2023 г.", self.align_left_settings)

	# Заключение (стр 6 и 7)
	def conclusion_page(self):
		self.add_paragraph("Командиру войсковой части 42600", self.align_right_settings)
		self.add_empty_paragraphs(3)
		self.add_paragraph("ЗАКЛЮЧЕНИЕ", self.bold_center_settings)
		self.add_paragraph("по материалам служебного разбирательства", self.bold_center_settings)
		self.add_paragraph("по факту грубого дисциплинарного проступка", self.bold_center_settings)
		self.add_paragraph("военнослужащим 2 стрелкового батальона войсковой части 42600", self.bold_center_settings)
		self.add_paragraph("гвардии рядовым Ивановым Иваном Ивановичем", self.bold_center_settings)
		self.add_empty_paragraphs(1)
		self.add_paragraph_left_right("16.04.2023 г.", "г. Донецк")
		self.add_empty_paragraphs(2)
		self.add_paragraph("Мной, временно исполняющим обязанности командира 2 стрелкового батальона войсковой части "
		                   "42600 гвардии подполковником *** *** ***, проведено служебное разбирательство по факту "
		                   "самовольного оставления части пулеметчиком 3 стрелкового отделения 3 стрелкового взвода 5 "
		                   "стрелковой роты 2 стрелкового батальона войсковой части 42600  гвардии рядовым Ивановым "
		                   "Иваном Ивановичем 26 июня 1997 года рождения.", self.ident_align_justify_settings)
		self.add_paragraph("В ходе проведения служебного разбирательства было установлено, что 16 апреля 2023 года "
		                   "пулеметчик 3 стрелкового отделения 3 стрелкового взвода 5 стрелковой роты 2 стрелкового "
		                   "батальона войсковой части 42600 гвардии рядовой Иванов Иван Иванович самовольно покинул "
		                   "расположение части не уведомив вышестоящее командование.", self.ident_align_justify_settings)
		self.add_paragraph("Проведенные розыскные мероприятия, опрос сослуживцев, поиск в лечебных учреждениях, "
		                   "военных комендатурах, а также отделениях полиции гвардии рядового Иванова Ивана Ивановича "
		                   "результата не дали, установить причины отсутствия военнослужащего, а также его "
		                   "местонахождение не удалось.", self.ident_align_justify_settings)
		self.add_paragraph("Причинами данного правонарушения явились:", self.ident_align_justify_settings)
		self.add_paragraph("невыполнение требований статьи 144, 145 Устава Внутренней Службы Вооруженных Сил "
		                   "Российской Федерации в части, касающейся воспитания, поддержания воинской дисциплины, "
		                   "морально–психологического состояния личного состава в роте, а также в части касающееся "
		                   "знаний деловых и морально–психологических качеств и особенностей всех военнослужащих роты, "
		                   "постоянного проведения с ними индивидуальной работы по воинскому воспитанию ВРИО командира "
		                   "5 стрелковой роты (Командир зависит от того, где служит боец) 2 стрелкового батальона "
		                   "войсковой части 42600 гвардии рядовым таким-то;", self.ident_align_justify_settings)
		self.add_paragraph("невыполнение требований статьи 160, 161 Устава Внутренней Службы Вооруженных Сил "
		                   "Российской Федерации в части, касающейся точного и своевременного исполнения возложенных "
		                   "на него обязанностей, поставленных задач и личная недисциплинированность пулеметчика 3 "
		                   "стрелкового отделения 3 стрелкового взвода 5 стрелковой роты 2 стрелкового батальона "
		                   "войсковой части 42600 гвардии рядового Иванова Ивана Ивановича.",
		                   self.ident_align_justify_settings)
		p1 = self.add_paragraph("Исходя из материала служебного разбирательства следует, что гвардии рядовой Иванов Иван "
		                   "Иванович самовольно покинул расположение части, за что в соответствии со статьей «337» "
		                   "Уголовного кодекса Российской Федерации предусматривается уголовная ответственность, "
		                   "на основании вышеизложенного ", self.ident_align_justify_settings)
		runner = p1.add_run("ПРЕДЛАГАЮ:")
		runner.bold = True
		self.add_paragraph("1. Временно исполняющему обязанности командира 5 стрелковой роты 2 стрелкового батальона "
		                   "войсковой части 42600 гвардии рядовому Такой-то Такой-то Такой-то за невыполнение "
		                   "требований статьи 144, 145 Устава Внутренней Службы Вооруженных Сил Российской Федерации в "
		                   "части, касающейся воспитания, поддержания воинской дисциплины, морально–психологического "
		                   "состояния личного состава в роте, а также в части касающееся знаний деловых и "
		                   "морально–психологических качеств и особенностей всех военнослужащих роты, постоянного "
		                   "проведения с ними индивидуальной работы по воинскому воспитанию, строго указать на "
		                   "УПУЩЕНИЕ ПО СЛУЖБЕ.", self.ident_align_justify_settings)
		self.add_paragraph("2. Пулеметчику 3 стрелкового отделения 3 стрелкового взвода 5 стрелковой роты 2 "
		                   "стрелкового батальона войсковой части 42600  гвардии рядовому Иванову Ивану Ивановичу за "
		                   "грубый дисциплинарный проступок самовольное оставление части более 4 (четырех) часов, "
		                   "объявить СТРОГИЙ ВЫГОВОР.", self.ident_align_justify_settings)
		self.add_empty_paragraphs(2)
		self.add_paragraph("ВРИО командира 2 стрелкового батальона", self.align_center_settings)
		self.add_paragraph("гвардии подполковник", self.align_center_settings)
		self.add_empty_paragraphs(2)
		self.add_paragraph_left_right("17.04.2023 г.", "ФИО полковника")
