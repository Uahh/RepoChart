import os
import json
import redis


class RepoBackup():
    def __init__(self):
        self.repo_list = []
        if not os.path.exists('repo_cache'):
            os.mkdir('repo_cache')

        if os.path.exists('repo_cache/repo_list.txt'):
            with open('repo_cache/repo_list.txt') as txt_file:
                for line in txt_file.readlines():
                    self.repo_list.append(line.rstrip())

    def add_repo(self, repo):
        self.repo_list.append(repo)
        with open('repo_cache/repo_list.txt', encoding="utf-8", mode="a") as txt_file:
            txt_file.write(repo + '\n')
