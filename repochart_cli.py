# -*- coding: utf-8 -*-
import re
import time
from optparse import OptionParser
from models.repo_chart import RepoChart

parser = OptionParser()
parser.add_option('-r', '--repo', dest='repo',
                  help="clone repo and get repo charts.")
parser.add_option('-v', '--version', action="store", help="Repo Chart v1.0.0")
options = parser.parse_args()[0]


def daily_repo():
    repo_list = ['vuejs/vue', 'tianocore/edk2', 'Uahh/RepoChart',
                 'Uahh/ToastFish', 'itorr/nbnhhsh', 'nlohmann/json', 'apache/echarts', 'Richasy/Bili.Uwp']
    for repo in repo_list:
        start = time.time()
        print(repo)
        repo_name = repo.split('/')
        repo = RepoChart(repo_name[0], repo_name[1])
        repo.output()
        end = time.time() - start
        print(str(end))


if __name__ == '__main__':
    daily_repo()
    # start = time.time()

    # if not re.match(".+/.+", options.repo):
    #     print('Error: this repo is not exist on Github.')
    #     exit()

    # repo_name = options.repo.split('/')
    # repo = RepoChart(repo_name[0], repo_name[1])
    # repo.output()

    # end = time.time() - start
    # print(str(end))
