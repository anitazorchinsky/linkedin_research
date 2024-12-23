import pandas as pd
from bs4 import BeautifulSoup
import requests
import openpyxl
from selenium import webdriver
import time

URL = "https://www.linkedin.com/jobs/search?keywords=&location=Israel&geoId=101620260&trk=public_jobs_jobs-search-bar_search-submit"

def get_soup_by_link(link):
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    driver = webdriver.Chrome(options=options)
    driver.get(link)
    scroll_pause_time = 2
    screen_height = driver.execute_script("return window.screen.height;")
    i = 1
    while True:
        driver.execute_script(f"window.scrollTo(0, {screen_height * i});")
        i += 1
        time.sleep(scroll_pause_time)
        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        if screen_height * i > scroll_height:
            break
    source = driver.page_source
    driver.quit()
    return BeautifulSoup(source, "html.parser")



def get_company_name_by_link(link):
    pass



soup = get_soup_by_link(URL)

# soup = BeautifulSoup(page.text, 'html.parser')
jobs_list = soup.find_all('a', class_='base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]')
jobs_table = {"vacancy_title":[],"vacancy_link":[],"company_name":[]}
for job in jobs_list:
    vacancy_title = job.find("span").text.strip()
    vacancy_link = job["href"]
    jobs_table["vacancy_title"].append(vacancy_title)
    jobs_table["vacancy_link"].append(vacancy_link)
    jobs_table["company_name"].append("test")
df = pd.DataFrame(jobs_table)
df.to_excel("vacancies.xlsx")

