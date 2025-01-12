import pandas as pd
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import urllib.parse
import uuid


user_answer = "yes"
keywords = []
while user_answer == "yes":
   keywords.append(input("enter keywords: "))
   user_answer = input("enter yes or no: ")


MAX_VACANCY = int(input("How many vacancies do you want? ")) // 10
options = webdriver.ChromeOptions()
options.add_argument("--incognito")
driver = webdriver.Chrome(options=options)

def generate_url(currentJobId, keywords, origin, refresh,position, pageNum,start, geoId=101620260):
    base_link = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?"
    return f"{base_link}&geoId={geoId}&keywords={keywords}&origin={origin}&refresh={refresh}&position={position}&pageNum={pageNum}&start={start}"


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


l = []
target_url='https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?{}&location=Tel%20Aviv&geoId=101620260&start={}'
for keyword in keywords:
    for i in range(MAX_VACANCY):
        time.sleep(2)
        res = requests.get(target_url.format(urllib.parse.urlencode({"keywords": keyword }),i))
        soup=BeautifulSoup(res.text,'html.parser')
        alljobs_on_this_page=soup.find_all("li")
        for x in range(0,len(alljobs_on_this_page)):
            jobid = alljobs_on_this_page[x].find("div",{"class":"base-card"}).get('data-entity-urn').split(":")[3]
            l.append(jobid)


jobs_table = {"vacancy_title":[],"company_title":[],"description":[],"seniority_level":[],"employment_type":[],"job_function":[],"industries":[]}

l = list(set(l))
for id in l:
    time.sleep(2)
    job_link = "https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/"+id
    res = requests.get(job_link)
    soup=BeautifulSoup(res.text,'html.parser')
    try:
        vacancy_title = soup.find("h2",{"class":"top-card-layout__title"}).text
    except:
        vacancy_title = ""
    try:
        company_title = soup.find("a",{"class":"topcard__org-name-link"}).text.strip()
    except:
        company_title = ""
    try:
        job_description = soup.find("div", {"class": "show-more-less-html__markup"}).text.strip()
    except:
        job_description = ""
    try:
        job_criteria = soup.find_all("span", {"class": "description__job-criteria-text"})
        seniority_level = job_criteria[0].text.strip()
        employment_type = job_criteria[1].text.strip()
        job_function = job_criteria[2].text.strip()
        industries = job_criteria[3].text.strip()
    except:
        seniority_level = ""
        employment_type = ""
        job_function = ""
        industries = ""
    jobs_table["vacancy_title"].append(vacancy_title)
    jobs_table["company_title"].append(company_title)
    jobs_table["description"].append(job_description)
    jobs_table["seniority_level"].append(seniority_level)
    jobs_table["employment_type"].append(employment_type)
    jobs_table["job_function"].append(job_function)
    jobs_table["industries"].append(industries)


df = pd.DataFrame(jobs_table)
df.to_excel(f"{uuid.uuid4()}.xlsx")

driver.close()
