#encoding='utf-8'

from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service
from selenium.webdriver import Firefox
import time

class edge_webdriver:
    def __init__(self,binary_location=r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',\
                 service_location = r'F:\WorkRooms\WebDrivers\Edge\MicrosoftWebDriver.exe'):
        options = webdriver.EdgeOptions()
        options.binary_location = binary_location
        service = EdgeService(executable_path=service_location)
        self._driver = webdriver.Edge(options=options,service=service)

    @property
    def driver(self):
        return self._driver

web = edge_webdriver()
web.driver.get(r'http://www.baidu.com')

time.sleep(5)
web.driver.quit()