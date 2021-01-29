import requests
from bs4 import BeautifulSoup

limit = 50
url = f"https://stackoverflow.com/jobs?q=python"



def extract_so_page():
    so_result = requests.get(url)
    so_soup = BeautifulSoup(so_result.text, "html.parser")
    pagination = so_soup.find("div", {"class": "s-pagination"})
    pages = pagination.find_all("a")
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)


def extract_job(result):
    title = result.find("h2").find("a")["title"]
    company, location = result.find("h3", {
        "class": "fc-black-700 fs-body1 mb4"
    }).find_all(
        "span", recursive=False)
    company = company.get_text(strip=True)
    location = location.get_text(strip=True)
    job_id = result["data-result-id"]
    jurl = f"https://stackoverflow.com/jobs/{job_id}"
    return {
        'title': title,
        'company': company,
        'location': location,
        'url': jurl
    }


def extract_so_job(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping Indeed : page {page}")
        result = requests.get(f"{url}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_so_jobs():
    max_so_page = extract_so_page()
    jobs = extract_so_job(max_so_page)
    return jobs
