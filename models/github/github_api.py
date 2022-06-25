import re
import json
import time
import math
import datetime
import requests
from models.github import private_config


class GithubStarApi():
    def __init__(self, git_data, server=False) -> None:
        self.git_data = git_data
        self.server = server
        self.headers = {
            'Accept': 'application/vnd.github.v3.star+json',
            "Authorization": "token " + private_config.token
        }
        self.star_link = "https://api.github.com/repos/{}/stargazers?per_page=100".format(
            self.git_data.repo_full_name)
        self.commit_link = "https://api.github.com/repos/{}/commits?per_page=1".format(
            self.git_data.repo_full_name)

        self.existence_flag = True
        self.large_flag = False
        self.star_flag = False
        self.check_existence()
        if self.existence_flag == False and self.server == True:
            return

        self.get_commit_count()
        if self.commit_count > 1000 and self.server == True:
            self.large_flag = True
            return

        self.get_total_stars()
        if self.total_stars > 4000 and self.server == True:
            self.star_flag = True
            return

        self.total_stars = 0
        self.cur_stars = 0
        self.git_data.star_chart_list.append(
            [
                "Star",
                "Repo",
                "Day"
            ]
        )

    def get_star_chart(self):
        print('start get star list...')
        self.get_link_list()
        self.convert_line_chart()
        print('succeed got all stars!')

    def get_total_stars(self):
        link = "https://api.github.com/repos/{}".format(
            self.git_data.repo_full_name)
        self.total_stars = self.request_api(link)['watchers']

    def get_link_list(self):
        if self.total_stars > 100:
            link_num = self.total_stars // 100
            # Github Api limited 400 pages.
            if link_num > 400:
                link_num = 399
        else:
            link_num = 1

        for i in range(1, link_num + 2):
            link = self.star_link + '&page=' + str(i)
            data = self.request_api(link)
            if data and i == 1:
                zero = int(data[0]['starred_at'].split(
                    'T')[0].replace('-', '')) - 1
                self.git_data.star_data[zero] = 0
            self.add_stars(data)

    def add_stars(self, data):
        for day in data:
            day = int(day['starred_at'].split('T')[0].replace('-', ''))
            self.cur_stars += 1
            self.git_data.star_data[day] = self.cur_stars

    def request_api(self, link):
        try:
            result = json.loads(requests.get(link, headers=self.headers).text)
        except:
            print("Github api request failed.")
        return result

    def convert_line_chart(self):
        for key in self.git_data.star_data.keys():
            temp = []
            temp.append(self.git_data.star_data[key])
            temp.append(self.git_data.repo_name)
            temp.append(key)
            self.git_data.star_chart_list.append(temp)
        if self.total_stars > 40000:
            self.cal_time(temp[2])

    def cal_time(self, begin):
        begin = str(begin)
        date1 = "{}/{}/{}".format(begin[0:4], begin[4:6], begin[6:8])
        date2 = datetime.datetime.now().strftime('%Y/%m/%d')
        date1 = time.strptime(date1, "%Y/%m/%d")
        date2 = time.strptime(date2, "%Y/%m/%d")
        date1 = datetime.datetime(date1[0], date1[1], date1[2])
        date2 = datetime.datetime(date2[0], date2[1], date2[2])

        diff_day = (date2 - date1).days
        inc_stars = math.floor((self.total_stars - 40000) / diff_day)
        remainder_stars = (self.total_stars - 40000) % diff_day
        for i in range(0, diff_day):
            date1 += datetime.timedelta(days=1)
            self.cur_stars += inc_stars
            if i == diff_day - 1:
                self.cur_stars += remainder_stars
            temp = []
            temp.append(self.cur_stars)
            temp.append(self.git_data.repo_name)
            temp.append(int(date1.strftime("%Y%m%d")))
            self.git_data.star_chart_list.append(temp)

    def check_existence(self):
        result = self.request_api(self.commit_link)
        if type(result) == dict:
            if 'message' in result.keys():
                if result['message'] == 'Not Found':
                    self.existence_flag = False

    def get_commit_count(self):
        self.commit_count = int(
            re.search('\d+$', requests.get(self.commit_link).links['last']['url']).group())
