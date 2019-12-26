import csv

def save_to_file(indeed_jobs):
    #한글깨짐 해결, 빈칸 제거
    file = open("jobs.txt", mode="w",encoding="utf-8",newline='')
    writer = csv.writer(file)
    writer.writerow(["title", "company", "location", "link"])
    for job in indeed_jobs:
        #dict의 값만 가져옴
        writer.writerow(list(job.values()))
    return