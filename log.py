import logging


class Log():
    def __init__(self):
        self.logger = logging.getLogger('gestClasse.Database')
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        hdlr = logging.FileHandler('gestClasse.log')
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        self.logger.addHandler(hdlr)

    def get_logger(self):
        return self.logger
