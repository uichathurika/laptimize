import logging

class LogFactory:
    __instance = None
    __logger = None

    def __init__(self, logger):
        if LogFactory.__instance is not None:
            raise Exception('Only one log factory can be created')
        else:
            LogFactory.__instance = self
            LogFactory.__logger = logger

    @staticmethod
    def get_instance(logger):
        if LogFactory.__instance is None:
            return LogFactory(logger)
        return LogFactory.__instance

    @staticmethod
    def get_logger():
        if LogFactory.__logger is not None:
            return  LogFactory.__logger
        else:
            logging.basicConfig(format='%(asctime)s %(message)s')
            return logging
