from classes.document_in_report import DocumentInReport


class DocLetterParents(DocumentInReport):
	def get_name(self):
		return "Письмо родственникам"

	def get_name_for_file(self):
		return f"Письмо_родственникам_СОЧ ({self.get_soldier_info().full_name}).docx"

	def render(self, custom_margins=None):
		s_info = self.get_soldier_info()
		rep_settings = self.get_report_settings()

		self.add_paragraph("МИНИСТЕРСТВО ОБОРОНЫ РОССИЙСКОЙ ФЕДЕРАЦИИ", self.bold_center_settings)
		self.add_paragraph(f"ВОЙСКОВАЯ ЧАСТЬ {self.get_military_unit()}", self.bold_center_settings)
		self.add_paragraph("_________________________________________________________________",
		                   self.align_center_settings)
		self.add_paragraph(rep_settings["military_unit_address"], self.align_center_settings)
		self.add_empty_paragraphs(3)

		mother = self.get_parent_name(rep_settings["mother_name"])
		father = self.get_parent_name(rep_settings["father_name"])
		courtesy = "[ВСТАВЬТЕ ОБРАЩЕНИЕ]"
		if len(father) > 0 and len(mother) > 0:
			courtesy = f"Уважаемые {mother} и {father}!"
		else:
			if len(father) > 0:
				courtesy = f"Уважаемый {father}!"
			else:
				if len(mother) > 0:
					courtesy = f"Уважаемая {mother}!"

		self.add_paragraph(f"{courtesy}", self.bold_center_settings)
		self.add_empty_paragraphs(1)

		rank = self.get_person_rank(s_info.rank, 0)
		name = self.get_person_name_declension(s_info.full_name, 0)

		self.add_paragraph(f"Командование войсковой части {self.get_military_unit()} сообщает Вам, что Ваш сын {rank} {name}, {self.get_date_format_1(self.get_date_of_event())} самовольно покинул расположение части, не уведомив вышестоящее командование.", self.ident_align_justify_settings)
		# TODO what if this is a lady?
		self.add_paragraph("Проведенные розыскные мероприятия, опрос сослуживцев вашего сына результата не дали, установить причины его отсутствия, а также его местонахождение не удалось.", self.ident_align_justify_settings)
		self.add_paragraph(f"Командование войсковой части {self.get_military_unit()} информирует Вас, что самовольное оставление части военнослужащим является уголовно наказуемым дисциплинарным проступком и влечет за собой уголовную ответственность по ст.337 УК РФ.", self.ident_align_justify_settings)
		name = self.get_person_name_declension(s_info.full_name, 1)
		self.add_paragraph(f"Просим Вас оказать содействие в поиске и возвращении Вашего сына {name} на место службы. В случае его появления просим сообщить по телефону: {rep_settings['phone_contact_to_report']}", self.ident_align_justify_settings)
		self.add_empty_paragraphs(2)

		self.add_paragraph("С уважением,", self.align_center_settings)
		cmd = self.get_commander_generic("commander_1_level", "СОСТАВИТЕЛЯ", 0, True)
		self.add_paragraph(cmd["position"], self.align_center_settings)
		self.add_paragraph(cmd["rank"], self.align_center_settings)
		self.add_paragraph(cmd["name"], self.align_right_settings)

		super().render()

	def get_parent_name(self, name):
		if name is None or len(name) == 0:
			return "[ВСТАВЬТЕ ИМЯ РОДИТЕЛЯ]"
		tokens = name.split(" ")
		if len(tokens) < 2:
			return name
		p_name = ""
		for t_ind in range(1, len(tokens)):
			p_name = f"{p_name} {tokens[t_ind]}"
		return p_name.strip()
