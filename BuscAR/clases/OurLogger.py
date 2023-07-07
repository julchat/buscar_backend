import datetime
import logging


class OurLogger():
    def __init__(self, file_name = "newfile"):
        fecha = str(datetime.datetime.now())
        fecha = fecha.replace(' ', '')
        fecha = fecha.replace(':', '')
        fecha = fecha.replace('-', '')
        fecha = fecha[0:14]

        filename = f"{file_name}_{fecha}.log"
        logging.basicConfig(filename=filename, format='%(asctime)s::%(levelname)s::%(message)s', filemode='w')

        # Creating an object
        logger = logging.getLogger()

        # Setting the threshold of logger to DEBUG
        logger.setLevel(logging.DEBUG)

        self.logger = logger

    def get_logger(self):
        return self.logger