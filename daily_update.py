import time
from models.repo_chart import RepoChart

current_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime())
print('start time: ' + current_time)

repo_list = ['vuejs/vue', 'tianocore/edk2-edkrepo', 'Uahh/ToastFish', 'itorr/nbnhhsh', 'nlohmann/json', 'apache/echarts']
for repo in repo_list:
    start = time.time()
    print(repo)
    repo_name = repo.split('/')
    repo = RepoChart(repo_name[0], repo_name[1])
    repo.output()
    end = time.time() - start
    print(str(end))

current_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime())
print('end time: ' + current_time)