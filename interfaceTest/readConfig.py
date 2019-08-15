import os
from configparser import ConfigParser

rootDir = os.path.dirname(os.path.realpath(__file__))
configPath = os.path.join(rootDir, 'config.ini')

class ReadConfig:
    def __init__(self):
        self.cf = ConfigParser()
        self.cf.read(configPath)

    def get_db(self, name):
        value = self.cf.get('DATABASE', name)
        return value

    def get_http(self, name):
        value = self.cf.get('HTTP', name)
        return value

    def get_email(self, name):
        value = self.cf.get('EMAIL', name)
        return value


if __name__ == '__main__':
    print(rootDir)
    print(configPath)
    db_test = ReadConfig().get_db('host')
    print(db_test)
    http_test = ReadConfig().get_http('baseurl')
    print(http_test)
    email_test = ReadConfig().get_email('test')
    print(email_test)
