import unittest
import os
import time
from interfaceTest.common import HTMLTestRunner, commonFunc, log

class RunCase(object):
    def __init__(self):
        rootPath = commonFunc.DirPath().get_rootPath()
        self.caseListFile = os.path.join(rootPath, 'caseList.xlsx')
        self.caseList = []
        myLog = log.Log()
        self.logger = myLog.get_logger()
        self.logPath = myLog.get_logPath()
        self.resultFile = os.path.join(self.logPath, 'report.html')

    def set_case_list(self):
        caseExcel=commonFunc.DoExcel(self.caseListFile)
        self.caseList=caseExcel.read_excel()
        # print(self.caseList)
        # with open(self.caseListFile, 'r') as f:
        #     reader = csv.reader(f)
        #     for r in reader:
        #         for value in r:
        #             if value != '' and not value.startswith('#'):
        #                 self.caseList.append(value.strip())
        # print(self.caseList)

    def set_case_suite(self):
        self.set_case_list()
        test_suite = unittest.TestSuite()
        suite_model = []
        
        for case in self.caseList:
            #根据caselist的state来获取应该进行的用例
            if(case["State"]):
                testCasePath = commonFunc.DirPath().get_testCasePath(case["Project"])
                # print(testCasePath)
                case_name = case["CaseName"]#.split('/')[-1]
                discover = unittest.defaultTestLoader.discover(testCasePath, pattern=case_name+'.py', top_level_dir=None)
                suite_model.append(discover)
            # print(discover)
        if len(suite_model) > 0:
            for suite in suite_model:
                for test_name in suite:
                    test_suite.addTest(test_name)
        else:
            return None
        return test_suite

    def run(self):
        try:
            self.logger.info('*********TEST START*********')
            time.sleep(0.5)
            suit = self.set_case_suite()
            if suit is not None:
                with open(self.resultFile, 'wb') as fp:
                    runnner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='Test Report', description='Test Description', verbosity=2)
                    runnner.run(suit)

            else:
                self.logger.info('Have no case to test.')
        except Exception as ex:
            self.logger.error(str(ex))
        finally:
            self.logger.info('*********TEST END***********')

if __name__ == '__main__':
    # RunCase().set_case_suite()
    # RunCase().set_case_list()
    RunCase().run()

