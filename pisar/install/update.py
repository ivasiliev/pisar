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


copy_if_not_exists("c:\\pisar\\pisar\\data\\personnel-demo-massive.xlsx", data_dir)
