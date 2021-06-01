import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.common.exceptions

import configparser

def one_parson(d, name, url):
    while True:
        d.get(url)
        rows = d.find_elements(By.XPATH, '//table//tr')
        for row in rows:
            items = row.find_elements_by_tag_name('td')
            if items is not None and len(items) > 4:
                print(','.join([name, items[0].get_attribute('title'), items[1].get_attribute('title'),
                                      items[2].text, items[3].text]))
        try:
            _next = d.find_element_by_id('AFHasNext')
        except selenium.common.exceptions.NoSuchElementException as e:
            break
        url = _next.get_attribute('href')


config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')
config_manaba = config['manaba']

driver = webdriver.Chrome()
driver.get("https://{}/ct/course_{}_footprint".format(config_manaba.get('host'),config_manaba.get('cource'))) #1931824

driver.find_element_by_id('username').send_keys(config_manaba.get('username'))
driver.find_element_by_id('password').send_keys(config_manaba.get('password'))
driver.find_element_by_tag_name('button').click()

list = []
for a in driver.find_element_by_tag_name('table').find_elements_by_tag_name('a'):
    list.append(a.get_attribute('href'))
for item in list:
    name = item.split('_')[-1]
    one_parson(driver, name, item)

