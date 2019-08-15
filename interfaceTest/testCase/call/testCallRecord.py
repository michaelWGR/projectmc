import unittest
import os
import time
from interfaceTest.testCase.call import get_token
from interfaceTest.common import commonFunc, testCommon

class TestCallRecord(unittest.TestCase):
    def setUp(self):
        self.tp = testCommon.TestTemplate()
        testFilePath = commonFunc.DirPath().get_testFilePath()
        self.exPath = os.path.join(os.path.join(testFilePath, 'call'), 'v1_call_callrecord.xlsx')
        # self.tkPath = os.path.join(os.path.join(testFilePath, 'call'), 'token.csv')
        self.tp.begin()

    def tearDown(self):
        self.tp.end()

    def testGetDataSuccess(self):
        dt = self.tp.get_dict_by_id(1, self.exPath)
        tk = get_token()
        headers = {'Authorization': tk}
        result = self.tp.testCaseTemplate(dt, headers=headers)
        # print(result[0])
        # print(result[1])
        rp = result["response"]
        ep = result["excepted_code"]
        if len(result) != 0:
            self.assertEqual(rp['code'], ep['code'])
            self.assertEqual(rp['msg'], ep['msg'])
            self.assertEqual(rp['success'], ep['success'])
            for d in ep['data']:
                self.assertTrue((d in rp['data']))

if __name__ == '__main__':
    unittest.main()



