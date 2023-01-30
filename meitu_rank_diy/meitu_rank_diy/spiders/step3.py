import scrapy
import pathlib
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.remote_connection import LOGGER
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv as csv3
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
import re


""" selenium """
driver_options = Options()
LOGGER.setLevel(logging.FATAL)
driver_options.add_argument('--headless')
driver_options.add_argument('--user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"')
driver = webdriver.Chrome(options=driver_options)
driver.set_window_rect(x=0, y=0, width=1440, height=900)


class CreateCsv2:
    """ csv """
    fn3 = 'model.csv'
    f3 = open(file=fn3, mode='w', encoding='utf-8', newline='')
    w3 = csv3.writer(f3)
    fields = ['M.NAME', 'M.SCORE', 'A.QYT', 'M.URL']
    w3.writerow(fields)


class Step3Spider(scrapy.Spider):
    name = 'step3'
    allowed_domains = []
    start_urls = ['https://www.meitu131.com/nvshen/']

    def parse(self, response, **kwargs):
        if pathlib.Path('mid_sorted.csv').exists():
            d = pd.read_csv('mid_sorted.csv', encoding='utf-8')
            mxmid = d.iloc[0]['M.ID']
            for i in range(1, mxmid+1):
                mu = response.urljoin(str(i))
                driver.get(mu)
                try:
                    mn = driver.find_element(by=By.XPATH, value='//*[@id="meinv-wrapper"]/div[1]/div/div[2]/h3').text
                    ms = int(driver.find_element(by=By.ID, value='diggnum').text)
                    aq = re.sub(pattern='([^0-9])', repl='', string=driver.find_element(by=By.XPATH, value='/html/body/div[3]/div[1]/span').text)
                    rows = [[mn, ms, aq, mu]]
                    CreateCsv2.w3.writerows(rows)
                    print('-'*18, mn, ms, aq, mu)
                except NoSuchElementException:
                    capture = 'NoSuchElementException.png'
                    driver.get_screenshot_as_file(capture)
                    raise
                except WebDriverException:
                    capture = 'WebDriverException.png'
                    driver.get_screenshot_as_file(capture)
        else:
            print('CSV FILE NOT FOUND')

    def __del__(self):
        driver.quit()
        CreateCsv2.f3.close()
