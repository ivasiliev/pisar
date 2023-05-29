from classes.personnel_storage import PersonnelStorage
from reports.report_official_proceeding import ReportOfficialProceeding

if __name__ == '__main__':
	print("Писарь начинает работу")
	pers_storage = PersonnelStorage()
	pers_storage.load_personnel_list_from_file("\\data\\personnel-demo.xlsx")
	settings = None
	report = ReportOfficialProceeding(pers_storage, settings)
	report.render("c:\\temp\\report1\\")
