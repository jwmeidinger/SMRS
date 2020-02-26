import os
import json
from collections.abc import Mapping

json_file_to_read = os.path.join(os.getcwd(), "mock.json")

def unpack_json(json_file):
    with open(json_file, "r") as content:
        data = json.load(content)
    return data

class JsonObject:
    def __init__(self, entries):
        new_entries = dict()
        for key, value in entries.items():
            if isinstance(value, Mapping):
                value = JsonObject(value)
            elif isinstance(value, list):
                value = JsonObject.expand_list(value)
            new_entries[key] = value
        
        self.__dict__.update(new_entries)
    
    @staticmethod
    def expand_list(unexpanded_list):
        expanded_list = list()
        for value in unexpanded_list:
            if isinstance(value, Mapping):
                value = JsonObject(value)
            elif isinstance(value, list):
                value = JsonObject.expand_list(value)
            expanded_list.append(value)
        return expanded_list
    
    def __getitem__(self, item):
         return self.__dict__[item]

    def __repr__(self):
        return str(self.__dict__)


json = unpack_json(json_file_to_read)
new_object = JsonObject(json)
