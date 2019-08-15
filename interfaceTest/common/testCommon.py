import os
import json
import time
from interfaceTest.common import commonFunc, configHttp, log

class TestTemplate(object):
    # 编写测试用例的模板

    def begin(self):
        print('****BEGIN****')

    def end(self):
        print('*****END*****')

    def testCaseTemplate(self, data_dict, method='', url='', headers='', title='', params='', excepted_code=''):
        if data_dict != {}:
            ht = configHttp.ConfigHttp()
            # 判断是否有传参
            if method == '':
                method_set = data_dict['method']
            else:
                method_set = method

            if url == '':
                url_set = data_dict['url']
            else:
                url_set = url
            ht.set_url(url_set)

            if headers == '':
                headers_set = data_dict['headers']
            else:
                headers_set = headers
            ht.set_headers(headers_set)

            if title == '':
                title_set = data_dict['title']
            else:
                title_set = title
            print('title: ' + title_set)

            if excepted_code == '':
                excepted_code_set = data_dict['excepted_code']
            else:
                excepted_code_set = excepted_code

            if method_set == 'get':
                if params == '':
                    params_set = data_dict['params']
                else:
                    params_set = params
                ht.set_params(params_set)

                # 计算请求的时间
                start = time.time()
                response = ht.get()
                end = time.time()
                print('duration: {}'.format(end-start))

                response_dict = json.loads(response.content)

                return {"response":response_dict, "excepted_code":excepted_code_set}

            elif method_set == 'post':
                if params == '':
                    data_set = data_dict['params']
                else:
                    data_set = params
                ht.set_data(data_set)

                start = time.time()
                response = ht.post()
                end = time.time()
                print('duration: {}'.format(end-start))

                response_dict = json.loads(response.content)

                return {"response":response_dict, "excepted_code":excepted_code_set}

            else:
                print('have no method')
                return []

        else:
            return []

    def assertEqualDict(self, dict1, dict2, method):
        eq1 =dict1
        eq2 = dict2
        if type(eq1) == type({}) and type(eq2) == type({}):
            for key in eq1:
                if type(eq1[key]) != type({}):
                    method(eq1[key], eq2[key])
                else:
                    self.assertEqualDict(eq1[key], eq2[key], method)

    def get_dict_by_id(self, id, filePath, sheet=0):
        doExcel = commonFunc.DoExcel(filePath, sheet)
        data_list = doExcel.read_excel()
        for data in data_list:
            if int(data['id']) == id:
                return data

        return {}


if __name__ == '__main__':
    path = commonFunc.DirPath()
    testFilePath = path.get_testFilePath()
    loginPath = os.path.join(testFilePath, 'login.xls')
    # print(loginPath)
    # fe = common.DoExcel(loginPath, 1)
    # data_list = fe.read_excel()
    # print(data_list)


    # for d in data_list:
    #     t = TestTemplate(d)
    #     result = t.testCaseTemplate()
    #     t.assertEqualDict(result[0], result[1])

    t = TestTemplate()
    d = t.get_dict_by_id(2, loginPath, 1)
    print(d)


