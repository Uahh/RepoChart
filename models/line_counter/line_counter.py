import os
from re import L
from models.git_local.git_data import GitData


class LineCounter():
    def __init__(self, git_data):
        self.git_data = git_data
        self.lines = 0

    
    def count_line(self):
        for file in self.git_data.path_list:
            file_path = os.path.join(self.git_data.repo_dir, file[1:-1])
            with open(file_path, 'r', encoding='utf-8') as temp:
                try:
                    self.lines += len(temp.readlines())
                except:
                    continue