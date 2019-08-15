from readConfig import rootDir
from time import strftime
from threading import Lock
import logging
import os

class Log:
    def __init__(self):

        # define logger
        self.logger = logging.getLogger('testLogger')
        self.logger.setLevel(logging.INFO)

        # 判断是否已有handler,防止重复打印log
        if not self.logger.handlers:
            # creat the dir of result
            resultPath = os.path.join(rootDir, "result")
            if not os.path.exists(resultPath):
                os.mkdir(resultPath)

            # creat the dir of log
            self.logPath = os.path.join(resultPath, strftime("%Y%m%d%H%M%S"))
            if not os.path.exists(self.logPath):
                os.mkdir(self.logPath)

            # define handle
            handle = logging.FileHandler(os.path.join(self.logPath, "output{}.log".format(strftime("%Y%m%d%H%M%S"))))
            # define formatter
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            handle.setFormatter(formatter)
            handle.setLevel(logging.INFO)

            # 创建handle，输出到控制台
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            ch.setFormatter(formatter)

            # add handle
            self.logger.addHandler(handle)
            self.logger.addHandler(ch)


    def get_logger(self):
        return self.logger

    def get_logPath(self):
        return self.logPath

class MyLog(Log):
    def __init__(self):
        Log.__init__(self)

    def get_logger(self):
        lock = Lock()
        lock.acquire()
        log = self.logger
        lock.release()
        return log

    def get_logPath(self):
        return self.logPath

if __name__ == "__main__":

    logger = Log().get_logger()
    logger.info('test')
    logger2 = Log().get_logger()
    logger2.info('test2')
    logger3 = Log().get_logger()
    logger3.info('test3')

