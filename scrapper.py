from indeed import get_jobs as get_indeed_jobs
from save import save_to_file

indeed_jobs = get_indeed_jobs()
#csv파일로 저장
save_to_file(indeed_jobs)