from indeed import *
from so import *
from save import *

indeed_jobs=get_indeed_jobs()
so_jobs=get_so_jobs()
jobs=so_jobs+indeed_jobs
#jobs=indeed_jobs
save_to_file(jobs)