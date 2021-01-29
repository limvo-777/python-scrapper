import os
import csv
import requests
import re
from bs4 import BeautifulSoup

os.system("clear")
alba_url = "http://www.alba.co.kr"

alba_scrap = requests.get(alba_url)
alba_soup = BeautifulSoup(alba_scrap.text,"html.parser")
alba_comp = alba_soup.find("div",{"id":"MainSuperBrand"}).find("ul",{"class":"goodsBox"})
# alba_company = alba_comp.find_all("span",{"class":"company"})
alba_companyUrl = alba_comp.find_all("a",{"class":"goodsBox-info"})
alba_companyList = []

for company in alba_companyUrl:
  name = company.find("img")['alt']
  alba_companyList.append({'url':company['href'],'company':name})


def alba_guhagi(url):
  scrap = requests.get(url+"/?pagesize=1000")
  soup = BeautifulSoup(scrap.text,"html.parser")
  # jobcount = soup.find("p",{"class":"jobCount"}).find("strong").string
  # scrap = requests.get(url+f"/?pagesize={jobcount}")
  # soup = BeautifulSoup(scrap.text,"html.parser")
  jobList = soup.find("div",{"id":"NormalInfo"}).find("tbody").find_all("tr")
  jobData = []
  i=0
  for job in jobList:
    try:
      jplace = job.find("td",{"scope":"row"}).get_text()
      jtitle = job.find("span",{"class":"company"}).string
      jtime = job.find("span",{"class":"time"}).string
      jpay = job.find("span",{"class":"number"}).string
      jpayicon = job.find("span",{"class":"payIcon"}).string
      jdate = job.find("td",{"class":"regDate"}).string
      jobData.append({'place':jplace,'title':jtitle,'time':jtime,'pay':jpayicon+jpay,'date':jdate})
    except:
      i=i+1
  return jobData



def save_to_file(jobs,company):
  text = company
  parse = re.sub('[-=.#/?:$}]', '', text)
  file = open(f"[{parse}].csv",mode="w")
  writer=csv.writer(file)
  writer.writerow(["place, title, time, pay, date"])
  for job in jobs:
    writer.writerow(list(job.values()))
  return
# i=0
# for company in alba_companyUrl:
#   url=company['href']
#   alba_companyList[i]['url']=url
#   i=i+1

# print(alba_companyList)

alba_guhagi(alba_companyList[0].get('url'))

ii=0
for company in alba_companyList:
  ii=ii+1
  save_to_file(alba_guhagi(company['url']),company['company'])
  print(ii)