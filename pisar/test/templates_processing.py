from docx import Document

f = open("c:\\pisar_data\\doc.docx", 'rb')
document = Document(f)
f.close()

runs = []

for paragraph in document.paragraphs:
	if len(paragraph.runs) < 2:
		continue
	run_anchor = None
	run_candidate = None
	for index in range(1, len(paragraph.runs)):
		# on start
		if run_anchor is None:
			run_anchor = paragraph.runs[index - 1]
		run_this = paragraph.runs[index]
		if len(run_this.text) == 0:
			continue

		if run_this.bold == run_anchor.bold and run_this.italic == run_anchor.italic and run_this.underline == run_anchor.underline:
			# merge them
			run_anchor.text = run_anchor.text + run_this.text
			run_this.clear()
		else:
			run_anchor = paragraph.runs[index]

	# replacement
	for run in paragraph.runs:
		if "{ИМЯ}" in run.text:
			run.text = run.text.replace("{ИМЯ}", "Иванов")

document.save("c:\\pisar_data\\doc-updated.docx")


