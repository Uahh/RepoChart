import os
import json


class LineCounter():
    def __init__(self, git_data):
        self.git_data = git_data
        self.lines = 0
        with open("data/language_colors.json") as json_file:
            self.language_suffix = json.load(json_file)
    
    def count_line(self):
        for file in self.git_data.path_list:
            file_path = os.path.join(self.git_data.repo_dir, file[1:-1])
            suffix = file_path.split('/')[-1].split('.')[-1]
            if not suffix in self.language_suffix:
                continue
            with open(file_path, 'r', encoding='utf-8') as temp:
                try:
                    self.lines += len(temp.readlines())
                except:
                    continue
        self.lines = {"data": self.lines}