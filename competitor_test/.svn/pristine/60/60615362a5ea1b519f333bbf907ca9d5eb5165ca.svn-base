# -*- coding:utf-8 -*-

from utils import FrameGenerator

__author__ = 'LibX'


class TestFrameGenerator(FrameGenerator):
    def __init__(self):
        super(TestFrameGenerator, self).__init__()

    def setUp(self):
        self.results = [1,2,3]
        self.index = 0

    def tearDown(self):
        self.results = [1,2,3]
        self.index = 0

    def get(self):
        if self.index >= len(self.results):
            return None
        result = self.results[self.index]
        self.index += 1
        return result


def main():
    with TestFrameGenerator() as g:
        for r in g:
            print r


if __name__ == '__main__':
    main()