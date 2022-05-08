import json
from collections import defaultdict
from pprint import pprint

class ConvertDict():
    def __init__(self, api_data) -> None:
        self.api_data = api_data
        self.load_language_colors()
        self.dict = self.get_path_dict()

    # Creates a default dictionary where each value is an other default dictionary.
    def nested_dict(self) -> defaultdict:
        return defaultdict(self.nested_dict)

    # Converts defaultdicts of defaultdicts to dict of dicts.
    def default_to_regular(self, new_path_dict):
        if isinstance(new_path_dict, defaultdict):
            new_path_dict = {k: self.default_to_regular(v) for k, v in new_path_dict.items()}
        return new_path_dict

    def get_path_dict(self):
        new_path_dict = self.nested_dict()
        for i in range(0, len(self.api_data.path_list)):
            parts = self.api_data.path_list[i].split('/')
            if parts:
                marcher = new_path_dict
                for key in parts[:-1]:
                    marcher = marcher[key]
                marcher['$count'] = self.api_data.size_list[i]
                marcher['$url'] = self.api_data.url_list[i]
                marcher['$sha'] = self.api_data.sha_list[i]
                marcher['$color'] = self.get_color(parts[-2].split('.')[-1])
        return self.default_to_regular(new_path_dict)['']

    def load_language_colors(self):
        with open("config/language_colors.json") as json_file:
            self.language_colors = json.load(json_file)
    
    def get_color(self, file):
        if file in self.language_colors:
            return self.language_colors[file]
        return '#E5E7EB'

# l1 = ['/foo/e.txt','/foo/bar/a.txt','/foo/bar/b.cfg','/foo/bar/c/d.txt', '/test.txt']
# l2 = [1, 2, 3, 4, 5]
# result = ConvertDict(l1, l2)
# pprint(result.dict)