import logging


class MyLogger:
    def __init__(self, name):
        self.log = logging.getLogger(name)
        self.formatter = logging.Formatter("%(message)s")
        self.levels = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }

    def stream_handler(self, level):
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(self.formatter)
        self.log.addHandler(streamHandler)
        return self.log

    def file_handler(self, file_name):
        fileHandler = logging.FileHandler(file_name)
        fileHandler.setFormatter(self.formatter)
        self.log.addHandler(fileHandler)
        return self.log


user_say_logger = MyLogger("user_say")
user_say_logger.stream_handler("INFO")
user_say_logger.file_handler("./logs/user_say.log")
user_say_logger.log.setLevel(logging.INFO)

res_logger = MyLogger("response")
res_logger.stream_handler("INFO")
res_logger.file_handler("./logs/response.log")
res_logger.log.setLevel(logging.INFO)
