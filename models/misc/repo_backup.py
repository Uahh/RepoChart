import os

class RepoBackup():
    def __init__(self):
        self.repo_list = []
        if not os.path.exists('repo_cache'):
            os.mkdir('repo_cache')

        if os.path.exists('repo_cache/repo_list.txt'):
            with open('repo_cache/repo_list.txt') as txt_file:
                for line in txt_file.readlines():
                    self.repo_list.append(line.rstrip())

    def add_repo(self, repo, type='Normal'):
        with open('repo_cache/repo_list.txt', encoding="utf-8", mode="a") as txt_file:
            if type == 'Normal':
                repo_name = repo + '\n'
            elif type == 'Without':
                repo_name = repo + '_without\n'
            elif type == 'Large':
                repo_name = repo + '_large\n'
            txt_file.write(repo_name)
            self.repo_list.append(repo_name[:-1])
    
    def del_repo(self, repo):
        if repo in self.repo_list:
            self.repo_list.remove(repo)
            with open('repo_cache/repo_list.txt', 'r') as txt_file:
                lines = txt_file.readlines()
            with open('repo_cache/repo_list.txt', 'w') as txt_file:
                for line in lines:
                    if repo not in line:
                        txt_file.write(line)


    def check_repo(self, repo):
        if repo + '_without' in self.repo_list:
            return 'Without'
        elif repo + '_large' in self.repo_list:
            return 'Large'
        elif repo in self.repo_list:
            return True
        else:
            return False