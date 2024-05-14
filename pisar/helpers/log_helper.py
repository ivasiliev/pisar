import logging


def log(text):
	logger = logging.getLogger("app")
	logger.info(text)
	print(text)
