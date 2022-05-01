from collections import defaultdict
from pprint import pprint

class ConvertDict():
    def __init__(self, path_list, size_list) -> None:
        self.path_list = path_list
        self.size_list = size_list
        self.dict = self.get_path_dict()

    # Creates a default dictionary where each value is an other default dictionary.
    def nested_dict(self):
        return defaultdict(self.nested_dict)

    # Converts defaultdicts of defaultdicts to dict of dicts.
    def default_to_regular(self, new_path_dict):
        if isinstance(new_path_dict, defaultdict):
            new_path_dict = {k: self.default_to_regular(v) for k, v in new_path_dict.items()}
        return new_path_dict

    def get_path_dict(self):
        new_path_dict = self.nested_dict()
        for i in range(0, len(self.path_list)):
            parts = self.path_list[i].split('/')
            if parts:
                marcher = new_path_dict
                for key in parts[:-1]:
                    marcher = marcher[key]
                marcher['count'] = self.size_list[i]
        return self.default_to_regular(new_path_dict)

l1 = ['foo/e.txt','foo/bar/a.txt','foo/bar/b.cfg','foo/bar/c/d.txt', 'test.txt']
l2 = [1, 2, 3, 4, 5]
result = ConvertDict(l1, l2)
pprint(result.dict)