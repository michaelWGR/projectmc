import unittest
import os
import csv
from interfaceTest.common import configHttp, commonFunc,HTMLTestRunner, log
from interfaceTest.common.testCommon import TestTemplate


class TestLogin(unittest.TestCase):

    def setUp(self):
        self.template = TestTemplate()
        self.template.begin()
        path = commonFunc.DirPath()
        self.callPath = path.get_testFilePath('call')
        self.loginPath = os.path.join(self.callPath, 'v1_call_login.xls')
        print(self.loginPath)

    def testPasswordError(self):
        data_dict = self.template.get_dict_by_id(2, self.loginPath)
        result = self.template.testCaseTemplate(data_dict)
        if result != []:
            self.template.assertEqualDict(result["response"], result["excepted_code"], self.assertEqual)

    def testLoginSuccess(self):
        data_dict = self.template.get_dict_by_id(1, self.loginPath)

        result = self.template.testCaseTemplate(data_dict)
        if result != None:
            rp = result["response"]
            ep = result["excepted_code"]
            self.assertEqual(rp['code'], ep['code'])
            self.assertEqual(rp['msg'], ep['msg'])
            self.assertNotEqual(rp['data'], None)
            self.assertEqual(rp['success'], ep['success'])

            # 把token写入文件
            token_csv = os.path.join(self.callPath, 'token.csv')
            with open(token_csv, 'w') as f:
                writer = csv.writer(f)
                token = rp['data']['accessToken']
                writer.writerow([token])

    def tearDown(self):
        self.template.end()

if __name__ == '__main__':
    # print('1')
    # testunit = unittest.TestSuite()
    # testunit.addTest(TestLogin('testLogin'))
    #
    # runner = unittest.TextTestRunner()
    # runner.run(testunit)

    # logPath = log.MyLog().get_logPath()
    # file = os.path.join(logPath, 'report.html')
    # print(file)
    # with open(file, 'wb') as report:
    #     runner = HTMLTestRunner.HTMLTestRunner(stream=report, title='test result', description='result: ')
    #     runner.run(testunit)

    unittest.main()
