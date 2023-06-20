import os


def sizeof_fmt(file_size):
	for unit in ["", "Кб", "Мб", "Гб", "Ti", "Pi", "Ei", "Zi"]:
		if abs(file_size) < 1024.0:
			return f"{file_size:3.1f} {unit}"
		file_size /= 1024.0
	return f"{file_size:.1f} байт"


def get_file_size_info(full_path):
	file_stats = os.stat(full_path)
	return sizeof_fmt(file_stats.st_size)
