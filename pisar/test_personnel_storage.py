from classes.personnel_storage import PersonnelStorage

if __name__ == '__main__':
	full_path = "data\\personnel-demo.xlsx"
	pers_storage = PersonnelStorage(full_path)
	person = pers_storage.find_person_by_id(4)
	assert person is not None
