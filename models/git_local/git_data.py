import os
import copy
import json
from collections import defaultdict
from pprint import pprint


class GitData():
    def __init__(self, owner, repo_name) -> None:
        self.owner = owner
        self.repo_name = repo_name
        self.repo_full_name = owner + '/' + repo_name
        self.user_dir = os.path.join('repo_cache', self.owner)
        self.repo_dir = os.path.join(self.user_dir, self.repo_name)
        self.path_list = []
        self.commits_list = []
        self.lines_list = []
        self.size_list = []
        self.url_list = []
        self.star_chart_list = []
        self.star_data = {}
        self.circle_dict = {}
        self.square_dict = {}
        self.commit_line_list = []
        self.first_commit_size = []
        self.file_suffix = {}
        self.commit_sha_dict = {}
        self.commit_date_dict = {}
        self.active_chart_list = []
        self.load_language_colors()
        self.total_line_template = {
            'name': '',
            'type': 'line',
            'stack': 'Total',
            'areaStyle': {},
            'emphasis': {
                'focus': 'series'
            },
            'itemStyle': {
                'color': '#333333'
            },
            'data': []
        }
        self.first_commit_template = {
            'value': 0,
            'name': '',
            'itemStyle':{
                'color': ''
            }
        }

    def get_git_path(self, repo_dir=None):
        if not repo_dir:
            repo_dir = self.repo_dir
        file_list = os.listdir(repo_dir)
        for file in file_list:
            if file == '.git':
                continue
            file_path = os.path.join(repo_dir, file)
            if os.path.isfile(file_path):
                # append path
                file_path = file_path.replace('\\', '/')
                self.path_list.append(file_path)

                # append file size
                self.size_list.append(os.path.getsize(file_path))

                # append file url
                file_name = ''
                url_path = file_path.split('/')
                for dir in url_path[3:]:
                    file_name = os.path.join(file_name, dir)
                file_name = file_name.replace('\\', '/')
                url = 'https://github.com/{}/{}/tree/master/{}'.format(
                    url_path[1], url_path[2], file_name)
                self.url_list.append(url)

                if '.' not in file_path:
                    continue
                suffix = file_path.split('/')[-1].split('.')[-1]
                suffix = '.' + suffix
                if suffix not in self.file_suffix:
                    temp_line = copy.deepcopy(self.total_line_template)
                    temp_line['name'] = suffix
                    temp_line['itemStyle']['color'] = self.get_color(suffix[1:])
                    self.commit_line_list.append(temp_line)
                    self.file_suffix[suffix] = 0
                    
            elif os.path.isdir(file_path):
                self.get_git_path(file_path)

    def get_color(self, file):
        if file in self.language_colors:
            return self.language_colors[file]
        return '#999999'

    def load_language_colors(self):
        with open("data/language_colors.json") as json_file:
            self.language_colors = json.load(json_file)
