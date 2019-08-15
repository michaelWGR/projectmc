import requests
from readConfig import ReadConfig
from common.log import Log

localReadConfig = ReadConfig()

class ConfigHttp:
    def __init__(self):
        self.host = localReadConfig.get_http("baseurl")
        self.port = localReadConfig.get_http("port")
        self.timeout = localReadConfig.get_http("timeout")
        self.logger = Log().get_logger()
        self.headers = {}
        self.params = {}
        self.data = {}
        self.url = ""
        self.files = {}

    def set_url(self, url, host=""):
        if host == "":
            self.url= self.host + url
        else:
            self.url = host + url

    def set_headers(self, header):
        self.headers = header

    def set_params(self, param):
        self.params = param

    def set_data(self, data):
        self.data = data

    def set_files(self, file):
        self.files = file

    # define http method
    def get(self):
        try:
            response = requests.get(self.url, params=self.params, headers=self.headers, timeout=float(self.timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    def post(self):
        try:
            response = requests.post(self.url, data=self.data, headers=self.headers, timeout=float(self.timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

if __name__ == "__main__":
    cf = ConfigHttp()
    host = "https://www.jianshu.com"
    url = "/p/bb754296db41"
    cf.set_url(url, host)
    print(cf.get().content)
