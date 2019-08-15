import os
import xlwt
import xlrd
import json
from interfaceTest.common.log import Log

__author__ = 'Michael Wang'

class DoExcel(object):
    def __init__(self, workbook, sheet=0):
        self.workbook = workbook
        self.sheet = sheet
        self.logger = Log().get_logger()

    # 读取excel文件里的数据，写为一个list
    def read_excel(self):
        # 定义excel文件内容list
        excel_list = []

        # 判断是否为excel文件
        file_suffix = os.path.splitext(self.workbook)[-1]
        if file_suffix not in ['.xls', '.xlsx']:
            self.logger.error('the name of {} is wrong'.format(self.workbook))
            return excel_list

        # 打开文件读取数据
        file = xlrd.open_workbook(self.workbook)
        # 获取一个表通过索引顺序
        table = file.sheet_by_index(self.sheet)

        nrows = table.nrows
        ncols = table.ncols

        # 定义该excel的key列表
        keys_list = []
        for i in range(nrows):
            # 先获取用例的key值
            if i == 0:
                # global keys_list
                keys_list = table.row_values(i)
                for j in range(len(keys_list)):
                    # 判断key值是否有重复
                    if keys_list[j] in keys_list[j+1:]:
                        self.logger.error('the name of key is duplicated that is {}'.format(keys_list[j]))
                        return excel_list
                continue

            # 把每行的值写到一个case_dict里
            case_dict = {}
            for k in range(ncols):
                values_list = table.row_values(i)
                case_dict[keys_list[k]] = values_list[k]

            # 把用例行写到list表里
            excel_list.append(case_dict)

        # 把json格式转化为dict格式
        for data in excel_list:
            for key in data:
                # 判断为json的值才转换
                if str(data[key]) == '':
                    # 跳过值为空的key
                    continue
                elif str(data[key]).strip()[0] == '{' and str(data[key]).strip()[-1] == '}':
                    value_dict = json.loads(data[key].strip())
                    data[key] = value_dict

        return excel_list

    # # 把json格式转化为dict格式
    # def format_data(self):
    #     data_list = self.read_excel()
    #     print(data_list)
    #     for data in data_list:
    #         for key in data:
    #             # 判断为json的值才转换
    #             if str(data[key]).strip()[0] == '{' and str(data[key]).strip()[-1] == '}':
    #                 value_dict = json.loads(data[key].strip())
    #                 data[key] = value_dict
    #
    #     return data_list

# 获取框架内文件夹的目录
class DirPath(object):
    def __init__(self):
        self.rootPath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    def get_rootPath(self):
        if not os.path.exists(self.rootPath):
            os.mkdir(self.rootPath)
        return self.rootPath

    def get_commonPath(self):
        commonPath = os.path.join(self.rootPath, 'common')
        if not os.path.exists(commonPath):
            os.mkdir(commonPath)
        return commonPath

    def get_resultPath(self):
        resultPath = os.path.join(self.rootPath, 'result')
        if not os.path.exists(resultPath):
            os.mkdir(resultPath)
        return resultPath

    def get_testCasePath(self,project):
        testCasePath = os.path.join(self.rootPath, 'testCase/'+project)
        if not os.path.exists(testCasePath):
            os.mkdir(testCasePath)
        return testCasePath

    def get_testFilePath(self,project):
        testFilePath = os.path.join(self.rootPath, 'testFile/'+project)
        if not os.path.exists(testFilePath):
            os.mkdir(testFilePath)
        return testFilePath

if __name__ == "__main__":
    path = DirPath()

    testFilePath = path.get_testFilePath()
    # print(testFilePath)
    callPath = os.path.join(testFilePath, 'call')
    loginPath = os.path.join(callPath, 'v1_call_login.xls')
    print(loginPath)
    file = DoExcel(loginPath, 0)
    dt = file.read_excel()
    print(dt)

