import urllib.request
from selenium import webdriver
import subprocess
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class Work():
    def __init__(self, url, path):
        self.driverLocation = '/usr/bin/chromedriver'
        self.driver = webdriver.Remote(
            command_executor='http://selenium:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)
        self.path_to_save = path
        self.url = url
        self.driver.get(self.url)
        self.m = self.get_src_original()
        self.size = self.driver.find_element_by_xpath('//tr[@valign="center"]/td[4][1]').text[1:]


    def write_djvu(self, name):
        subprocess.Popen(f'/app/jpg_to_djvu.sh {name}',cwd=self.path_to_save, shell=True)

    def connect(self):
        self.driver.get(self.url)

    def get_src_original(self):
        img = self.driver.find_element_by_xpath('//center/div//img')
        src = img.get_attribute('src')
        modif = src.split('/')
        modif = modif[:len(modif)-1]
        return modif

    def name_of_file(self):
        temp = self.driver.find_element_by_xpath('//body//div[2]//a').text.split(' ')
        return '_'.join(temp)

    def main(self, num):
        try:
            name = None
            if num < 10:
                name = f'000{num}.jpg'
            elif num >= 10 and num < 100:
                name = f'00{num}.jpg'
            elif num >= 100 and num <= 1000:
                name = f'0{num}.jpg'
            self.m.append(name)
            src = "/".join(self.m)
            self.m.pop()

            print("Downloading" + " " + src)

            urllib.request.urlretrieve(src, f"{self.path_to_save}/{name}")


        except:
            print("too much requests")

    def run(self):
        for  i in range(1,int(self.size)+1):
            self.main(i)

        self.write_djvu(self.name_of_file())
        self.driver.close()
        return True