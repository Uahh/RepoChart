from cgitb import reset
import json
import requests
from queue import Queue
from pprint import pprint

import private_config
from convert_dict import ConvertDict

headers = {"Authorization": "token " + private_config.token}


class RequestGithubApi():
    def __init__(self, link, headers) -> None:
        self.link = link
        self.current_path = '/'
        self.headers = headers
        self.path_list = []
        self.size_list = []

        self.q = Queue()
        self.q.put(self.current_path)
        while not self.q.empty():
            path = self.q.get(False)
            current_node = self.request_github_api(self.link + path)
            for node in current_node:
                current_path = path + node['name'] + '/'
                if node['type'] == 'dir':
                    self.q.put(current_path)
                self.size_list.append(node['size'])
                self.path_list.append(current_path)


    def request_github_api(self, link) -> dict:
        try:
            json_text = requests.get(link, headers=self.headers).text
            node = json.loads(json_text)
        except:
            print("Github api request failed.")
        return node

def get_repo_tree(owner, repo):
    link = "https://api.github.com/repos/{}/{}/contents".format(owner, repo)
    result = RequestGithubApi(link, headers)
    repo_tree = ConvertDict(result.path_list, result.size_list)
    pprint(repo_tree.dict)
    with open("data/Fyzhq.json", 'w') as f:
        f.write(json.dumps(repo_tree.dict))

get_repo_tree("Uahh", "Fyzhq")