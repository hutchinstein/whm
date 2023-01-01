import logging

import sys
sys.path.append('..')
from const.const import PROJECT_LOCATION # noqa


class LocalLog:
    def __init__(self, file_name):
        self.log_location = f"{PROJECT_LOCATION}/logs"
        self.file_name = file_name
        logging.basicConfig(filename=f"{self.log_location}/{self.file_name}",
                            encoding='utf-8',
                            level=logging.DEBUG,
                            format='%(asctime)s.%(msecs)03d %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        logging.info("Object initialized")

    def info(self, msg):
        logging.info(msg)

    def warning(self, msg):
        logging.warning(msg)
            
    def debug(self, msg):
        logging.debug(msg)
