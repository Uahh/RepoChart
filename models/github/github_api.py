from models.github import private_config
from models.git_local.git_data import GitData, ConvertDict
import sys
import json
import time
import math
import datetime
import requests
from pprint import pprint

sys.path.append(sys.path[0] + '/..')


class GithubStarApi():
    def __init__(self, git_data) -> None:
        self.git_data = git_data
        self.git_data.line_chart_list.append(
            [
                "Star",
                "Repo",
                "Day"
            ]
        )
        self.link = "https://api.github.com/repos/{}/stargazers?per_page=100".format(
            git_data.repo_name)
        self.headers = {
            'Accept': 'application/vnd.github.v3.star+json',
            "Authorization": "token " + private_config.token
        }
        self.total_stars = 0
        self.cur_stars = 0
        self.get_total_stars()
        self.get_link_list()
        self.convert_line_chart()

    def get_total_stars(self):
        link = "https://api.github.com/repos/{}".format(
            self.git_data.repo_name)
        self.total_stars = self.request_api(link)['watchers']

    def get_link_list(self):
        if self.total_stars > 100:
            link_num = self.total_stars / 100

            # Github Api limited 400 pages.
            if link_num > 400:
                link_num = 400
        else:
            link_num = 1

        for i in range(1, link_num + 1):
            link = self.link + '&page=' + str(i)
            data = self.request_api(link)
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
            self.git_data.line_chart_list.append(temp)
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
            self.git_data.line_chart_list.append(temp)
