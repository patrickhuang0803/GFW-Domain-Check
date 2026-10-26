#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from bs4 import BeautifulSoup

import time
import os

class GfwCheck:

    def __init__(self):
        self.work_dir = os.path.abspath(os.path.dirname(__file__))
    
    def check_ready_to_check_content(self, file):
        with open(os.path.join(self.work_dir, file)) as f: 
            domains = [line.strip() for line in f if line.strip()]
        if len(domains) == 0:
            print("Need check zones is no exist, program end.")           
            os._exit(0)
        else:
            print("Need check zones is exist, program continue.")
    
    def split_domains(self, file):
        domain_limit = 100
        file_count = 0
        urls_list = []
        with open(os.path.join(self.work_dir, file)) as f: 
            domains = [line.strip() for line in f if line.strip()]
        for i in range(0, len(domains), domain_limit):
            urls = domains[i:i + domain_limit]
            urls_list.append(urls)
        return urls_list
        
    def browser_prepare(self):
        chrome_options = Options()
        chrome_options.page_load_strategy="none"
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        browser = webdriver.Chrome(options=chrome_options)
        return browser

    @staticmethod
    def htool_domains_check(browser, urls_list):
        try:
            browser.get('http://www.htool.com/domain/walls.html')
        except TimeoutException:
            print('頁面載入第一次逾時，重試')
            try:
                browser.get('http://www.htool.com/domain/walls.html')
            except TimeoutException:
                print('頁面載入第二次逾時，重試')
                try:
                    browser.get('http://www.htool.com/domain/walls.html')
                except TimeoutException:
                    print('頁面載入第三次逾時，停止')
                    os._exit(1)

        wait = ui.WebDriverWait(browser, 30)
        wait.until(lambda driver: driver.find_element(
            by=By.XPATH, value='//textarea[@id="searchKey"]')
        )
        wait.until(lambda driver: driver.find_element(
            by=By.XPATH, value='//button[@id="btnSearch"]')
        )

        searchbox = browser.find_element(By.ID, value="searchKey")
        searchbtn = browser.find_element(By.ID, value="btnSearch")

        html_texts=[]
        for urls in urls_list:
            domains = '\n'.join(urls)
            searchbox.send_keys(domains)
            time.sleep(10)
            searchbtn.click()
            time.sleep(30)
            html_text = browser.page_source
            html_texts.append(html_text) 
            searchbox.clear()
        browser.quit()

        return html_texts

    @staticmethod
    def htool_html_text_resolve(html_texts):
        check_results=""
        for html_text in html_texts:
            soup = BeautifulSoup(html_text, 'html.parser')
            rows = soup.select('#wallsResult .item-result')
            for row in rows:
                domain = row.select_one('.domainItem').get('domain')
                status = row.select_one('.searchResult').get_text(strip=True)
                check_results += f"{domain} {status}\n"
        return check_results