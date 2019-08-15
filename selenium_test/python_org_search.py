# -*- coding: utf-8 -*-
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("http://www.python.org")
# print driver.title
for i in driver.get_cookies():
    print i
assert "Python" in driver.title
# driver.get_screenshot_as_file('foo.png')
driver.save_screenshot('sr.png')
elem = driver.find_element_by_name("q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
# print driver.page_source
assert "No results found." not in driver.page_source
driver.close()

# class PythonOrgSearch(unittest.TestCase):
#
#     def setUp(self):
#         self.driver = webdriver.Chrome()
#
#     def test_search_in_python_org(self):
#         driver = self.driver
#         driver.get("http://www.python.org")
#         self.assertIn("Python", driver.title)
#         elem = driver.find_element_by_name("q")
#         elem.send_keys("pycon")
#         elem.send_keys(Keys.RETURN)
#         assert "No results found." not in driver.page_source
#
#
#     def tearDown(self):
#         self.driver.close()
#
# if __name__ == "__main__":
#     unittest.main()