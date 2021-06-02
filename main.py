import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.common.exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

import configparser
import argparse


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


def main_parse(d):
    list = []
    for a in d.find_element_by_tag_name('table').find_elements_by_tag_name('a'):
        list.append(a.get_attribute('href'))
    for item in list:
        name = item.split('_')[-1]
        one_parson(d, name, item)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('host', help='hostname of manaba')
    parser.add_argument('cource', help='cource number of manaba')

    parser.add_argument('--config', help='config file for usernema and password')
    parser.add_argument('--timeout', help='timeout (Unit:sec)', default=30, type=int)

    args = parser.parse_args()

    driver = webdriver.Chrome()
    driver.get("https://{}/ct/course_{}_footprint".format(args.host, args.cource))  # 1931824

    if args.config is not None:
        config = configparser.ConfigParser()
        config.read(args.config, encoding='utf-8')
        config_manaba = config['manaba']
        driver.find_element_by_id('username').send_keys(config_manaba.get('username'))
        driver.find_element_by_id('password').send_keys(config_manaba.get('password'))
        driver.find_element_by_tag_name('button').click()
    else:
        print("Please login until {} sec".format(args.timeout))
        existTitle = WebDriverWait(driver, args.timeout).until(expected_conditions.title_contains("manaba"))

    main_parse(driver)
