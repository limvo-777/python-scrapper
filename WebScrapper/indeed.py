import requests
from bs4 import BeautifulSoup

limit = 50; 
url =f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?as_and=python&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&radius=25&fromage=any&limit={limit}"

def extract_indeed_page():
  indeed_result = requests.get(url)
  indeed_soup = BeautifulSoup(indeed_result.text,"html.parser")
  pagination =indeed_soup.find("div",{"class":"pagination"})
  pages =pagination.find_all("a")

  num = []
  for page in pages[:-1]:
    num.append(int(page.string))
  
  max_page=num[-1]
  return max_page
  
def extract_job(result):
  title = result.find("h2",{"class":"title"}).find("a")["title"]
  company = result.find("div",{"class":"sjcl"}).find("span").string
  if company is None:
    company = result.find("div",{"class":"sjcl"}).find("a").string
  title = title.strip()
  location = result.find("div",{"class":"sjcl"}).find("span",{"class":"location"}).string
  job_id = result["data-jk"]
  jurl=f"https://kr.indeed.com/viewjob?jk={job_id}"
  return {'title': title, 'company': company,'location':location,'url':jurl}

def extract_indeed_job(last_page):
  jobs=[]
  for page in range(last_page):
    print(f"Scrapping Indeed : page {page}")
    result=requests.get(f"{url}&start={page*limit}")
    soup = BeautifulSoup(result.text,"html.parser")
    results =soup.find_all("div",{"data-tn-component":"organicJob"})
    for result in results:
      job =extract_job(result)
      jobs.append(job)
  return jobs

def get_indeed_jobs():
  max_indeed_page=extract_indeed_page()
  jobs=extract_indeed_job(max_indeed_page)
  #jobs=extract_indeed_job(2)
  return jobs