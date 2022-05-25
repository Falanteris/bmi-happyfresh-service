import inspect
import logging
from logging.handlers import TimedRotatingFileHandler
class LogFormatClass():
    def __init__(self):
        # initialize 5 log files 
        self.info_log = self.get_logger_format_default(logger_name="log/info.log")
        self.info_log.setLevel(logging.INFO)
        self.warning_log = self.get_logger_format_default(logger_name="log/warning.log")
        self.warning_log.setLevel(logging.WARNING)
        self.error_log = self.get_logger_format_default(logger_name="log/error.log")
        self.error_log.setLevel(logging.ERROR)
        self.critical_log = self.get_logger_format_default(logger_name="log/critical.log")
        self.critical_log.setLevel(logging.CRITICAL)

        #self.info_log.info("BEGIN LOG")
    def get_logger_format_default(self,**kwargs):
        logger_name = "{}.log".format(inspect.stack()[1][3])
        if "logger_name" in kwargs:
            logger_name = kwargs["logger_name"]
        logger = logging.getLogger(logger_name)
        # file handler to be passed into the logger
        logging.getLogger().handlers.clear()
        formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(name)s : %(message)s")
        fileHandler = TimedRotatingFileHandler(logger_name,when="midnight")
        fileHandler.setFormatter(formatter)
        if (logger.hasHandlers()):
           logger.handlers.clear()
        logger.addHandler(fileHandler)
        logger.propagate = False
        """
        asctime: time and date
        levelname: log importane (debug, info, warning, etc.)
        the 's' in the end is to make it parsed as a string
        name: test name
        message : actual message from logger

        """
        """
        log hierarchy (bottom to top):
            1. debug
            2. info
            3. warning
            4. error
            5. critical
        using setLevel method from logger object would 
        only display specific log level.

        """
        # this will only make info and the levels below it visible
        logger.setLevel(logging.DEBUG)
        # this will only make error and the levels below it visible
        # logger.setLevel(logging.ERROR)
        return logger
    def get_logger_format_default_static(self,**kwargs):
        logger_name = "{}.log".format(inspect.stack()[1][3])
        if "logger_name" in kwargs:
            logger_name = kwargs["logger_name"]
        logger = logging.getLogger(logger_name)
        # file handler to be passed into the logger
        formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(name)s : %(message)s")
        fileHandler = logging.FileHandler(logger_name)
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)
        """
        asctime: time and date
        levelname: log importane (debug, info, warning, etc.)
        the 's' in the end is to make it parsed as a string
        name: test name
        message : actual message from logger

        """
        """
        log hierarchy (bottom to top):
            1. debug
            2. info
            3. warning
            4. error
            5. critical
        using setLevel method from logger object would 
        only display specific log level.

        """
        # this will only make info and the levels below it visible
        logger.setLevel(logging.DEBUG)
        # this will only make error and the levels below it visible
        # logger.setLevel(logging.ERROR)
        return logger
    def get_logger_format_csv(self,**kwargs):
        # use inspect.stack()[1][3] to get the caller of this method
        logger_name = inspect.stack()[1][3]
        if "logger_name" in kwargs:
            logger_name = kwargs["logger_name"]
        logger = logging.getLogger(logger_name)
        template = logging.Formatter("%(asctime)s,%(levelname)s,%(name)s,%(message)s")
        file_handler = logging.FileHandler("log.csv")
        file_handler.setFormatter(template)
        logger.addHandler(file_handler)
        logger.setLevel(logging.INFO)
        return logger
    def info(self,data):
        self.info_log.info(data)
    def error(self,data):
        self.error_log.error(data)
    def critical(self,data):
        self.error_log.critical(data)
    def warning(self,data):
        self.warning_log.warning(data)
