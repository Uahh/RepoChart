import os
import copy
import json
from collections import defaultdict

from models.git_local.git_data import GitData
from models.git_local.git_command import GitCommand
from models.github.github_api import GithubStarApi


class RepoChart():
    def __init__(self, owner, repo_name):
        self.repo = GitCommand(owner, repo_name)
        self.repo.get_all_chart_data()
        GithubStarApi(self.repo.git_data)
        self.circle_dict = {}
        self.sqare_dict = {}
        self.get_repo_path_dict()
        self.star_chart_list = self.repo.git_data.star_chart_list
        self.commit_line_list = self.repo.git_data.commit_line_list
        self.json_path = os.path.join('output', self.repo.owner)
        self.json_name = self.repo.repo_name


    # Creates a default dictionary where each value is an other default dictionary.
    def nested_dict(self) -> defaultdict:
        return defaultdict(self.nested_dict)

    # Converts defaultdicts of defaultdicts to dict of dicts.
    def default_to_regular(self, new_path_dict):
        if isinstance(new_path_dict, defaultdict):
            new_path_dict = {k: self.default_to_regular(
                v) for k, v in new_path_dict.items()}
        return new_path_dict

    def get_repo_path_dict(self):
        new_path_dict = self.nested_dict()
        for i in range(0, len(self.repo.git_data.path_list)):
            parts = self.repo.git_data.path_list[i].split('/')
            if parts:
                marcher = new_path_dict
                for key in parts[:-1]:
                    if len(parts) > 3:
                        if '$size' not in marcher.keys():
                            marcher['$size'] = 0
                    marcher = marcher[key]
                marcher['$size'] = self.repo.git_data.size_list[i]
                marcher['$commits'] = self.repo.git_data.commits_list[i]
                marcher['$lines'] = self.repo.git_data.lines_list[i]
                marcher['$url'] = self.repo.git_data.url_list[i]
                suffix = parts[-2].split('.')[-1]
                marcher['$color'] = self.get_color(suffix)
                index = len(parts) - 3
                while index > 0:
                    temp_marcher = new_path_dict
                    for key in parts[:-(index + 1)]:
                        temp_marcher = temp_marcher[key]
                    temp_marcher['$size'] += marcher['$size']
                    index -= 1

        self.circle_dict = self.default_to_regular(new_path_dict)['']
        sqare_dict = {
            'value': 0,
            "name": self.repo.git_data.repo_name,
            "path": '',
            'children': []
        }
        self.total_size = 0
        self.sqare_dict = [self.convert_sqare_dict(
            self.circle_dict, sqare_dict)]
        self.sqare_dict[0]['value'] = self.total_size

    def convert_sqare_dict(self, circle_dict, sqare_dict):
        dict_template = {
            'value': 0,
            'name': '',
            'path': '',
            'itemStyle': {
                'color': '#333333'
            },
            'children': []
        }
        for key in circle_dict.keys():
            if key == '$size':
                continue
            dt = copy.deepcopy(dict_template)
            dt['value'] = circle_dict[key]['$size']
            if '$color' in circle_dict[key].keys():
                dt['itemStyle']['color'] = circle_dict[key]['$color']
            if '$commits' not in circle_dict[key]:
                dt['name'] = key
                dt['path'] = sqare_dict['path'] + '/' + key
                dt['children'] = []
                sqare_dict['children'].append(dt)
                self.convert_sqare_dict(circle_dict[key], dt)
            else:
                dt['name'] = key
                dt['path'] = sqare_dict['path'] + '/' + key
                sqare_dict['children'].append(dt)
                self.total_size += dt['value']
        return sqare_dict

    def get_color(self, file):
        if file in self.repo.git_data.language_colors:
            return self.repo.git_data.language_colors[file]
        return '#E5E7EB'

    def output(self):
        if not os.path.exists(self.json_path):
            os.mkdir(self.json_path)
        
        if self.circle_dict:
            output_path = os.path.join(self.json_path, self.json_name)
            with open(output_path + '_circle.json', 'w') as json_file:
                json_file.write(json.dumps(self.circle_dict))
            print('Circle chart output succeed!')

        if self.sqare_dict:
            output_path = os.path.join(self.json_path, self.json_name)
            with open(output_path + '_square.json', 'w') as json_file:
                json_file.write(json.dumps(self.sqare_dict))
            print('Square chart output succeed!')

        if self.star_chart_list:
            output_path = os.path.join(self.json_path, self.json_name)
            with open(output_path + '_line.json', 'w') as json_file:
                json_file.write(json.dumps(self.star_chart_list))
            print('Star chart output succeed!')

        if self.commit_line_list:
            output_path = os.path.join(self.json_path, self.json_name)
            with open(output_path + '_commit_line.json', 'w') as json_file:
                json_file.write(json.dumps(self.commit_line_list))
            print('Commit line chart output succeed!')
