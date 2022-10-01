import os
import logging


# 환경변수를 읽어서 로깅 레벨과 로그를 남길 파일의 경로를 변수에 저장한다
if os.environ["FLASK_ENV"] == "development":
    loggerLevel = logging.DEBUG
    filename = "./logs/developServer.log"
elif os.environ["FLASK_ENV"] == "test":
    loggerLevel = logging.DEBUG
    filename = "./logs/testServer.log"
else:
    loggerLevel = logging.INFO
    filename = "./logs/server.log"

# 로거 인스턴스를 만든다
logger = logging.getLogger("mylogger")

# 포매터를 만든다
formatter = logging.Formatter("[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s")

# 스트림과 파일로 로그를 출력하는 핸들러를 각각 만든다.
fileHandler = logging.FileHandler(filename)
streamHandler = logging.StreamHandler()

# 각 핸들러에 포매터를 지정한다.
fileHandler.setFormatter(formatter)
streamHandler.setFormatter(formatter)

# 로거 인스턴스에 스트림 핸들러와 파일핸들러를 붙인다.
logger.addHandler(fileHandler)
logger.addHandler(streamHandler)
logger.setLevel(loggerLevel)
