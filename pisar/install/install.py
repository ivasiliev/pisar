# do this manually:
# git clone https://github.com/ivasiliev/pisar.git c:/pisar
import os
import shutil

folders = ["c:\\pisar_data", "c:\\pisar_output"]

for folder in folders:
	if not os.path.exists(folder):
		os.makedirs(folder)

settings_folder = "c:\\pisar\\pisar\\data\\"
data_folder = "c:\\pisar\\pisar\\report-settings\\"
dest_folder = "c:\\pisar_data\\"

folders_to_copy = [settings_folder, data_folder]
for fldr in folders_to_copy:
	src_files = os.listdir(fldr)
	for file_name in src_files:
		full_file_name = os.path.join(fldr, file_name)
		if os.path.isfile(full_file_name):
			print(f"{full_file_name} -> {dest_folder}")
			shutil.copy(full_file_name, dest_folder)

print(f"Каталог настроек: {folders[0]}")
print(f"Каталог для выгрузки документов: {folders[1]}")
print("Нажмите любую клавишу...")

input()
