from csv import reader
from os.path import join
from interfaceTest.common.commonFunc import DirPath

def get_token():
    testFilePath = DirPath().get_testFilePath()
    tkPath = join(join(testFilePath, 'call'), 'token.csv')
    with open(tkPath, 'r') as f:
        r = reader(f)
        for l in r:
            if len(l) != 0:
                return l[0]


if __name__ == '__main__':
    t = get_token()
    print(t)