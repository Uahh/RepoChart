# -*- coding: utf-8 -*-
import re
import time
from optparse import OptionParser
from models.repo_chart import RepoChart


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-r', '--repo', dest='repo',
                    help="clone repo and get repo charts.")
    parser.add_option('-v', '--version', action="store", help="Repo Chart v1.0.0")
    options = parser.parse_args()[0]

    current_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime())
    print('start time: ' + current_time)

    if not re.match(".+/.+", options.repo):
        print('Error: this repo is not exist on Github.')
        exit()

    repo_name = options.repo.split('/')
    repo = RepoChart(repo_name[0], repo_name[1])
    repo.output()

    current_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime())
    print('end time: ' + current_time)
