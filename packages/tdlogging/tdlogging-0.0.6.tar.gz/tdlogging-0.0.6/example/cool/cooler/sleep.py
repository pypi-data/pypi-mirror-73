## Edited by TDLogger
from example.logger_instance import logger

import time

@logger
class Sleep:
    @staticmethod
    def sleep(n):
        time.sleep(n)
