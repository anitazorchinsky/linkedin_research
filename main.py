import pandas as pd
from bs4 import BeautifulSoup
import requests
import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# URL = "https://www.linkedin.com/jobs/search?keywords=&location=Israel&geoId=101620260&trk=public_jobs_jobs-search-bar_search-submit"
# URL = "https://www.linkedin.com/jobs/search?trk=guest_homepage-basic_guest_nav_menu_jobs&position=1&pageNum=0"
options = webdriver.ChromeOptions()
options.add_argument("--incognito")
# options.add_experimental_option("mobileEmulation", {"deviceName":"iPhone 14 Pro Max"})
# options.add_experimental_option("windowTypes",["webview"])
# options.add_argument("start-maximized")
driver = webdriver.Chrome(options=options)

def generate_url(currentJobId, keywords, origin, refresh,position, pageNum,start, geoId=101620260):
    base_link = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?"
    return f"{base_link}&geoId={geoId}&keywords={keywords}&origin={origin}&refresh={refresh}&position={position}&pageNum={pageNum}&start={start}"

# URL = generate_url(None, "python", "JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE", "false", "1", "0", "0" )
# print(URL)


def login():
    login_email = "cabil42488@myweblaw.com"
    login_password = "3$&Kq6pmuQaEA39"
    url_login = "https://www.linkedin.com/uas/login"
    driver.get(url_login)
    driver.find_element(By.ID,"username").send_keys(login_email)
    driver.find_element(By.ID,"password").send_keys(login_password)
    driver.find_element(By.TAG_NAME,"button").click()

def get_soup_by_link(link):
    driver.get(link)
    time.sleep(5)
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
    return BeautifulSoup(source, "html.parser")

def get_company_name_by_link(soup):
    company_name = None
    company_name = soup.find("a", class_="topcard__org-name-link topcard__flavor--black-link")
    if company_name is None:
        company_name = None
    else:
        company_name = company_name.text.strip()
    return company_name

# # login()
# # time.sleep(10)
# driver.get(URL)
# time.sleep(10)
# URL = generate_url(None, "python", "JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE", "false", "1", "0", "25" )
# print(URL)
# driver.get(URL)
# time.sleep(10)
# URL = generate_url(None, "python", "JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE", "false", "1", "0", "50" )
# print(URL)
# driver.get(URL)
# time.sleep(10)



# soup = get_soup_by_link(URL)
# time.sleep(2)

# driver.execute_script(f"window.scrollTo(0, {2000});")
# scroll_height = driver.execute_script("return document.body.scrollHeight;")
#
#
# for ul_tag in driver.find_element(By.TAG_NAME,"main").find_element(By.TAG_NAME,"ul").find_elements(By.TAG_NAME,"a"):
#     time.sleep(2)
#     ul_tag.click()
#
# jobs_list = soup.find_all('a',class_="job-card-container__link")
# jobs_table = {"vacancy_title":[],"vacancy_link":[],"company_name":[]}
# count = 3
# # jobs_table = {"vacancy_title":[],"vacancy_link":[]}
# for job in jobs_list:
#     vacancy_title = job.find("span").text.strip()
#     vacancy_link = job["href"]
#     jobs_table["vacancy_title"].append(vacancy_title)
#     jobs_table["vacancy_link"].append(vacancy_link)
#     count -= 1
#     if count == 0:
#         break
# for link in jobs_table["vacancy_link"]:
#     result = get_company_name_by_link(get_soup_by_link(link))
#     while result is None:
#         time.sleep(2)
#         result = get_company_name_by_link(get_soup_by_link(link))
#     jobs_table["company_name"].append(result)
# df = pd.DataFrame(jobs_table)
# df.to_excel("vacancies.xlsx")
# print(jobs_table)

# link = "https://il.linkedin.com/jobs/view/sports-marketing-manager-at-adidas-4070975528?position=1&pageNum=0&refId=6MQHdbVnRtGL4UwCmZXydw%3D%3D&trackingId=VnFKJKJ0q4dFC5a7B4maxQ%3D%3D"
# result = get_company_name_by_link(get_soup_by_link(link))
# while result is None:
#     time.sleep(2)
#     result = get_company_name_by_link(get_soup_by_link(link))
# print(result)

l = []
target_url='https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Python&location=Tel%20Aviv&geoId=101620260&start={}'
for i in range(0,100):
    res = requests.get(target_url.format(i))
    soup=BeautifulSoup(res.text,'html.parser')
    alljobs_on_this_page=soup.find_all("li")

    for x in range(0,len(alljobs_on_this_page)):
        jobid = alljobs_on_this_page[x].find("div",{"class":"base-card"}).get('data-entity-urn').split(":")[3]
        l.append(jobid)


# driver.quit()
for id in l:
    print("https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/"+id)