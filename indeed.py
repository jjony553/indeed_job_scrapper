import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?as_and=python&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&as_src=&radius=25&l=&fromage=any&limit={LIMIT}&sort=&psf=advsrch&from=advancedsearchhttps://kr.indeed.com/jobs?q=python&l=%EC%84%B1%EB%82%A8+%ED%8C%90%EA%B5%90%EB%8F%99&limit={LIMIT}&radius=25"

def extract_indeed_pages():
    #스크랩할 url
    result = requests.get(URL)
    #사이트 모든 정보 가져옴
    soup = BeautifulSoup(result.text, "html.parser")
    #div의 class명 pagination 찾기
    pagination = soup.find("div", {"class": "pagination"})
    #a테그 찾기
    links = pagination.find_all('a')
    pages =[]
    #links의 string만 리스트에 담기,'다음'은 삭제하기 위해 마지막 문자 삭제
    for link in links[:-1]:
        pages.append(int(link.string))
    max_pages = pages[-1]
    return max_pages

def extract_job(html):
    #제목 가져오기
    title = html.find("div",{"class": "title"}).find("a")["title"]
    #회사 이름 가져오기
    company = html.find("span", {"class":"company"})
    company_anchor = company.find("a")
    #회사에 링크가 있으면 anchor에서 정보 가져오기
    if company.find("a") is not None:
        company = company_anchor.string
    else:
        company = company.string
    #공백 제거를 위해 strip 사용
    company = company.strip()
    #location 정보 있으면
    #location = html.find("span",{"class":"location"}).string
    #location정보가 없을시
    location = html.find("div",{"class":"recJobLoc"})["data-rc-loc"]
    job_id=html["data-jk"]
    return {'title': title, 
            'company': company, 
            "location": location,
            "link":f"https://kr.indeed.com/viewjob?jk={job_id}&tk=1dsr5b5jr7lsj800&from=serp&vjs=3"}

def extract_indeed_jobs(last_pages):
    jobs = []
    for page in range(last_pages):
        print(f"Scrapping page {page+1}")
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div",{"class":"jobsearch-SerpJobCard"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs

def get_jobs():
    last_indeed_pages = extract_indeed_pages()
    jobs = extract_indeed_jobs(last_indeed_pages)
    return jobs
