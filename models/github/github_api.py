import json
import requests
from queue import Queue
from pprint import pprint

import private_config
from convert_dict import ConvertDict

headers = {"Authorization": "token " + private_config.token}

class GithubApiData():
    def __init__(self) -> None:
        self.path_list = []
        self.size_list = []
        self.url_list = []
        self.sha_list = []


class RequestGithubApi():
    def __init__(self, link, headers) -> None:
        self.link = link
        self.current_path = '/'
        self.headers = headers
        self.api_data = GithubApiData()
        self.q = Queue()

    def get_repo_data(self):
        self.q.put(self.current_path)
        while not self.q.empty():
            path = self.q.get(False)
            current_node = self.request_github_api(self.link + path)
            for node in current_node:
                current_path = path + node['name'] + '/'
                if node['name'][0] == '.':
                    continue
                if node['type'] == 'dir':
                    self.q.put(current_path)
                self.api_data.size_list.append(node['size'])
                self.api_data.path_list.append(current_path)
                self.api_data.url_list.append(node['html_url'])
                self.api_data.sha_list.append(node['sha'])
                
    def request_github_api(self, link) -> dict:
        try:
            json_text = requests.get(link, headers=self.headers).text
            node = json.loads(json_text)
        except:
            print("Github api request failed.")
        return node

def get_repo_tree(owner, repo):
    link = "https://api.github.com/repos/{}/{}/contents".format(owner, repo)
    r = RequestGithubApi(link, headers)
    r.get_repo_data()
    repo_tree = ConvertDict(r.api_data)
    # pprint(repo_tree.dict)
    with open("../../output/StarTrack-js.json", 'w') as f:
        f.write(json.dumps(repo_tree.dict))

get_repo_tree("seladb", "StarTrack-js")