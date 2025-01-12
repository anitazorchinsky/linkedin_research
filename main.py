import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import urllib.parse
import uuid


user_answer = "yes"
keywords = []
while user_answer == "yes":
   keywords.append(input("enter keywords: "))
   user_answer = input("enter yes or no: ")


MAX_VACANCY = int(input("How many vacancies do you want? "))


l = []
target_url='https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?{}&location=Tel%20Aviv&geoId=101620260&start={}'
for keyword in keywords:
    for i in range(0,MAX_VACANCY,10):
        time.sleep(2)
        res = requests.get(target_url.format(urllib.parse.urlencode({"keywords": keyword }),i))
        soup = BeautifulSoup(res.text,'html.parser')
        alljobs_on_this_page = soup.find_all("li")
        for x in range(0,len(alljobs_on_this_page)):
            jobid = alljobs_on_this_page[x].find("div",{"class":"base-card"}).get('data-entity-urn').split(":")[3]
            l.append(jobid)


jobs_table = {"vacancy_title":[],"company_title":[],"description":[],"seniority_level":[],"employment_type":[],"job_function":[],"industries":[]}

l = list(set(l))
for id in l:
    time.sleep(2)
    print(f"{l.index(id) + 1} / {len(l)}")
    job_link = "https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/" + id
    res = requests.get(job_link)
    soup = BeautifulSoup(res.text,'html.parser')
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
