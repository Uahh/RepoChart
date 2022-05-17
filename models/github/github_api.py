from models.github import private_config
from models.git_local.git_data import GitData, ConvertDict
import sys
import json
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
        self.first_link = "https://api.github.com/repos/{}/stargazers?per_page=100".format(git_data.repo_name)
        self.link_list = []
        self.headers = {
            'Accept': 'application/vnd.github.v3.star+json',
            "Authorization": "token " + private_config.token
        }
        self.cur_stars = 0
        self.get_link_list()
        self.convert_line_chart()

    def get_link_list(self):
        first_result = requests.get(self.first_link, headers=self.headers)

        link_sqlit = first_result.links['last']['url'].split('&page=')
        link_num = int(link_sqlit[-1])
        
        self.add_stars(json.loads(first_result.text))

        for i in range(2, link_num + 1):
            link = link_sqlit[0] + '&page=' + str(i)
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

# def get_repo_tree(owner, repo):
#     link = "https://api.github.com/repos/{}/{}/contents".format(owner, repo)
#     r = RequestGithubApi(link, headers)
#     r.get_repo_data()
#     repo_tree = ConvertDict(r.api_data)
#     # pprint(repo_tree.dict)
#     with open("../../output/StarTrack-js.json", 'w') as f:
#         f.write(json.dumps(repo_tree.dict))

# get_repo_tree("seladb", "StarTrack-js")
