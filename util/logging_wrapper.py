import logging

from datetime import datetime


class Log:
    date_fmt = '%m/%d/%Y %H:%M:%S'

    @staticmethod
    def init_logger():
        logging.basicConfig(filename='logs/launchpad.log',
                            level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s: %(message)s',
                            datefmt='%m/%d/%Y %H:%M:%S')

    @staticmethod
    def debug(message):
        logging.debug(message)
        Log.__log_to_term(message, "DEBUG")

    @staticmethod
    def info(message):
        logging.info(message)
        Log.__log_to_term(message, "INFO")

    @staticmethod
    def warn(message):
        logging.warning(message)
        Log.__log_to_term(message, "WARNING")

    @staticmethod
    def error(message):
        logging.error(message)
        Log.__log_to_term(message, "ERROR")

    @staticmethod
    def __log_to_term(message: str, level: str):
        now = datetime.now()
        date_time = now.strftime(Log.date_fmt)
        print(f'{date_time} {level}: {message}')
