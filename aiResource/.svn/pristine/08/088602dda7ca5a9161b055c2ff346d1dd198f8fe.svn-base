# -*- coding: utf-8 -*-

import urllib2
import re
import os
import traceback

host = "https://www.2265bb.com"
for i in range(2, 8):
    base_url = "https://www.2270bb.com/Html/63/index-{}.html".format(i)
    print base_url
    tmp = urllib2.urlopen(base_url).read()
    link_list = re.findall('<li><a\s+href="([^\"]*)"', tmp, re.M)
    print len(link_list)
    for item in link_list:
        try:
            item = host + item
            data = urllib2.urlopen(item).read()
            img_url_list = re.findall('<img\s+src="([^\"]*)"', data, re.M)
            print len(img_url_list)
            for img in img_url_list:
                try:
                    print img
                    file_name = os.path.join("img", img.split("/")[-1])
                    user_agent = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
                    headers = {"User-Agent": user_agent}
                    request = urllib2.Request(img, headers=headers)
                    response = urllib2.urlopen(request)
                    buff = response.read()
                    f = file(file_name, "w")
                    f.write(buff)
                    f.close()
                except ValueError:
                    print traceback.format_exc()
        except urllib2.URLError:
            print traceback.format_exc()
