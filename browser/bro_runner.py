# -*- coding:utf-8 -*-
import ConfigParser
import os
import traceback
import thread

import argparse
import pyscreenshot

from threading import Timer

import time

DATA_FILE = "data.ini"
CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
WINDOWS_DELIMITER = "\\"


class Bro(object):
    def __init__(self, name, browser_path):
        self.name = name
        self.browser_path = browser_path
        self.process_name = browser_path.split(WINDOWS_DELIMITER)[-1]

    def start_and_open_url(self, url):
        import webbrowser
        self.suicide()
        thread.start_new_thread(lambda x: webbrowser.get(self.browser_path).open(x), (url,))

    def suicide(self):
        """
        The browser is so sad to suicide.
        :return:
        """
        import psutil
        for proc in psutil.process_iter():
            if proc.name() == self.process_name:
                os.system("taskkill /f /im {}".format(proc.pid))


class Data(object):
    SECTION_APP_URL = "app_url"
    SECTION_BRO = "browsers"

    def __init__(self, config_path):
        config = ConfigParser.ConfigParser()
        config.read(config_path)

        self.app_urls = config_section_map(config, Data.SECTION_APP_URL)
        self.bros = config_section_map(config, Data.SECTION_BRO)

        import os
        bro_list = []
        for k, v in self.bros.items():
            bro_list.append(v)

        os.environ['BROWSER'] = ";".join(bro_list)


class Watcher(object):
    INTERVAL = 30
    DURATION = 1800

    def __init__(self, bro, app):
        self.count = Watcher.DURATION
        self.bro = bro
        self.app = app
        self.folder_time = time.strftime("%Y-%m-%d-%H-%M-%S")

    def on_listening(self):
        self.schedule()

    def schedule(self):
        if self.count > 0:
            self.count -= Watcher.INTERVAL
            Timer(Watcher.INTERVAL, self.schedule, ()).start()
            self.get_and_save_screenshot()

    def get_and_save_screenshot(self):
        dir_path = os.path.join(CURRENT_FOLDER, self.folder_time, "{}_{}".format(self.app, self.bro.name))
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)

        img = pyscreenshot.grab()
        img_name = "screenshot_{}.jpg".format(Watcher.DURATION - self.count)
        print("Taking : {}".format(img_name))
        img.save(os.path.join(dir_path, img_name))


def config_section_map(config, section):
    result_dict = {}
    options = config.options(section)
    for option in options:
        try:
            result_dict[option] = config.get(section, option)
            if result_dict[option] == -1:
                print ("skip: %s" % option)
        except Exception:
            traceback.print_exc()
            result_dict[option] = None
    return result_dict


def main():
    parser = argparse.ArgumentParser('Description')
    parser.add_argument('app')
    args = parser.parse_args()
    app = args.app

    # 1. Init.
    data = Data(os.path.join(CURRENT_FOLDER, DATA_FILE))

    # 2. New bro object and start
    for k, v in data.bros.items():
        bro = Bro(k, v)

        # Support one app only now.
        bro.start_and_open_url(data.app_urls[app])

        # 3. Watching
        watcher = Watcher(bro, app)
        watcher.on_listening()

        # 4. End
        time.sleep(Watcher.DURATION)
        bro.suicide()


if __name__ == '__main__':
    main()
