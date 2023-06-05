# 1. manually:
# git clone https://github.com/ivasiliev/pisar.git c:/pisar
import os
import shutil

folders = ["c:\\pisar_data", "c:\\pisar_output"]

for folder in folders:
	if not os.path.exists(folder):
		os.makedirs(folder)

src_folder = "c:\\pisar\\pisar\\report-settings\\"
dest_folder = "c:\\pisar_data\\"
src_files = os.listdir(src_folder)
for file_name in src_files:
	full_file_name = os.path.join(src_folder, file_name)
	if os.path.isfile(full_file_name):
		shutil.copy(full_file_name, dest_folder)

print(f"Каталог настроек: {folders[0]}")
print(f"Каталог для выгрузки документов: {folders[1]}")
print("Нажмите любую клавишу...")

input()
