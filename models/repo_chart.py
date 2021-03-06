import os
import copy
import json
from collections import defaultdict

from models.git_local.git_data import GitData
from models.git_local.git_command import GitCommand
from models.github.github_api import GithubStarApi
from models.misc.line_counter import LineCounter


class RepoChart():
    def __init__(self, owner, repo_name, server=False):
        self.chart_status = False
        self.json_path = os.path.join('output', owner)
        self.json_name = repo_name
        self.output_path = os.path.join(self.json_path, self.json_name)
        self.large_flag = False
        self.existence_flag = True
        self.star_flag = False
        self.check_output()
        if not self.chart_status or server == False:
            self.git_data = GitData(owner, repo_name)

            self.api = GithubStarApi(self.git_data, server)
            self.star_flag = self.api.star_flag
            self.large_flag = self.api.large_flag
            if self.large_flag or not self.existence_flag or self.star_flag:
                self.chart_status = True
                return
            
            self.api.get_star_chart()
            self.repo = GitCommand(self.git_data)
            if self.repo == 'Network failed':
                return 'Network failed'
            self.repo.get_all_chart_data()
            self.circle_dict = {}
            self.sqare_dict = {}
            self.get_repo_path_dict()

            self.counter = LineCounter(self.git_data)
            self.counter.count_line()

            self.lines = self.counter.lines

            self.star_chart_list = self.repo.git_data.star_chart_list

            self.commit_line_list = self.repo.git_data.commit_line_list
            self.commit_line_list.sort(key=lambda data: len(data['name']))

            self.first_commit_size = self.repo.git_data.first_commit_size
            self.first_commit_size.sort(key=lambda data: len(data['name']))

            self.active_chart_list = self.repo.git_data.active_chart_list
            self.active_chart_list.sort(key=lambda data: data[0])

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
        return '#999999'

    def sort_by(self, data):
        return len(data['name'])

    def output(self):
        if not os.path.exists('output'):
            os.mkdir('output')
        if not os.path.exists(self.json_path):
            os.mkdir(self.json_path)

        if self.circle_dict:
            output_name = self.output_path + '_circle.json'
            with open(output_name, 'w') as json_file:
                json_file.write(json.dumps(self.circle_dict))
            print('{} circle chart output succeed!'.format(output_name.replace('\\', '/')))

        if self.sqare_dict:
            output_name = self.output_path + '_square.json'
            with open(output_name, 'w') as json_file:
                json_file.write(json.dumps(self.sqare_dict))
            print('{} square chart output succeed!'.format(output_name.replace('\\', '/')))

        if self.first_commit_size:
            output_name = self.output_path + '_commit_pie.json'
            with open(output_name, 'w') as json_file:
                json_file.write(json.dumps(self.first_commit_size))
            print('{} commit size pie chart output succeed!'.format(output_name.replace('\\', '/')))

        if self.commit_line_list:
            output_name = self.output_path + '_commit_line.json'
            with open(output_name, 'w') as json_file:
                json_file.write(json.dumps(self.commit_line_list))
            print('{} commit line chart output succeed!'.format(output_name.replace('\\', '/')))

        if self.active_chart_list:
            output_name = self.output_path + '_active_line.json'
            with open(output_name, 'w') as json_file:
                json_file.write(json.dumps(self.active_chart_list))
            print('{} active chart output succeed!'.format(output_name.replace('\\', '/')))

        if self.star_chart_list:
            output_name = self.output_path + '_star_line.json'
            with open(output_name, 'w') as json_file:
                json_file.write(json.dumps(self.star_chart_list))
            print('{} star chart output succeed!'.format(output_name.replace('\\', '/')))

        if self.lines:
            output_name = self.output_path + '_code_of_lines.json'
            with open(output_name, 'w') as json_file:
                json_file.write(json.dumps(self.lines))
            print('{} star chart output succeed!'.format(output_name.replace('\\', '/')))
        self.chart_status = True

    def check_output(self, static=False):
        if static == False:
            if os.path.exists(self.output_path + '_circle.json'):
                self.chart_status = True
                print('Already existing output file, directly return data.')
        else:
            repo = static.split('/')
            output_path = os.path.join('output', repo[0], repo[1])
            if os.path.exists(output_path + '_circle.json'):
                return True
            return False

    def open_all_charts(self, chart_type, static=False):
        if static == False:
            if chart_type == 'circle':
                with open(self.output_path + '_circle.json', encoding='utf-8') as json_file:
                    return json.load(json_file)
            if chart_type == 'square':
                with open(self.output_path + '_square.json', encoding='utf-8') as json_file:
                    return json.load(json_file)
            if chart_type == 'commit_pie':
                with open(self.output_path + '_commit_pie.json', encoding='utf-8') as json_file:
                    return json.load(json_file)
            if chart_type == 'commit_line':
                with open(self.output_path + '_commit_line.json', encoding='utf-8') as json_file:
                    return json.load(json_file)
            if chart_type == 'active_line':
                with open(self.output_path + '_active_line.json', encoding='utf-8') as json_file:
                    return json.load(json_file)
            if chart_type == 'star_line':
                with open(self.output_path + '_star_line.json', encoding='utf-8') as json_file:
                    return json.load(json_file)
            if chart_type == 'code_of_lines':
                with open(self.output_path + '_code_of_lines.json', encoding='utf-8') as json_file:
                    return json.load(json_file)
        else:
            repo = static.split('/')
            output_path = os.path.join('output', repo[0], repo[1])
            if chart_type == 'circle':
                with open(output_path + '_circle.json', encoding='utf-8') as json_file:
                    return json.load(json_file)
            if chart_type == 'square':
                with open(output_path + '_square.json', encoding='utf-8') as json_file:
                    return {'data': json.load(json_file)}
            if chart_type == 'commit_pie':
                with open(output_path + '_commit_pie.json', encoding='utf-8') as json_file:
                    return {'data': json.load(json_file)}
            if chart_type == 'commit_line':
                with open(output_path + '_commit_line.json', encoding='utf-8') as json_file:
                    return {'data': json.load(json_file)}
            if chart_type == 'active_line':
                with open(output_path + '_active_line.json', encoding='utf-8') as json_file:
                    return {'data': json.load(json_file)}
            if chart_type == 'star_line':
                with open(output_path + '_star_line.json', encoding='utf-8') as json_file:
                    return {'data': json.load(json_file)}
            if chart_type == 'code_of_lines':
                with open(output_path + '_code_of_lines.json', encoding='utf-8') as json_file:
                    return json.load(json_file)