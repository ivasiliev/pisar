from reports.report_official_proceeding import ReportOfficialProceeding

if __name__ == '__main__':
	print("Писарь начинает работу")
	report = ReportOfficialProceeding()
	report.render("c:\\temp\\report1\\")
