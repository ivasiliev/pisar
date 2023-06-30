import os
import shutil

data_dir = "c:\\pisar_data\\"


def copy_if_not_exists(full_path, destination_folder):
	if not os.path.exists(full_path):
		print(f"Файл не обнаружен: {full_path}")
	else:
		destination_path = os.path.join(destination_folder, os.path.basename(full_path))
		if not os.path.exists(destination_path):
			shutil.copy(full_path, destination_folder)
			print(f"Скопирован файл {full_path} -> {destination_folder}")


def delete_if_exists(full_path):
	if os.path.exists(full_path):
		os.remove(full_path)
		print(f"Файл {full_path} удален")


shutil.copy("C:\\pisar\\pisar\\data\\personnel-demo.xlsx", data_dir)

copy_if_not_exists("c:\\pisar\\pisar\\data\\personnel-demo-massive.xlsx", data_dir)
copy_if_not_exists("c:\\pisar\\pisar\\report-settings\\soldier_info.json", data_dir)
copy_if_not_exists("c:\\pisar\\pisar\\report-settings\\common_info.json", data_dir)

obsolete_files = ["copy_impossible.json", "explanation_impossible.json", "official_proceeding.json", "order_official_proceeding.json", "performance_characteristics.json"]
for f in obsolete_files:
	fp = os.path.join(data_dir, f)
	delete_if_exists(fp)
