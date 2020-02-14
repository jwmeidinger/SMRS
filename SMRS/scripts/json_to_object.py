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
s = JsonObject(json)

#a = Struct(**"hello")

#data = unpack_json()
#data = '{"name": "John Smith"}'
#x = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
#print(x.name)




"""    
def unpack_json():
    with open("E:\\Users\\gandr\\Documents\\GitHub\\byte_le_royale_2020\\logs\\turn_0001.json", "r") as file:
        json = file.readlines()
        if len(json) != 1:
            raise Exception
        json = json[0]
        return json


def json_to_object(json):
    object = None
    return object

if __name__ == "__main__":
    json = unpack_json()
    object = json_to_object(json)
    print(object)
"""

"""
class Struct:
    def __init__(self, **entries):
        self.__dict__.update(Struct.__expand_mapping(entries))
    
    @staticmethod
    def __expand_mapping(unexpanded_mapping):
        expanded_mapping = dict()
        for key, value in unexpanded_mapping.items():
            value = Struct.__expand_item(value)
            expanded_mapping[key] = value
        return expanded_mapping

    @staticmethod
    def __expand_list(unexpanded_list):
        expanded_list = list()
        for value in unexpanded_list:
            value = Struct.__expand_item(value)
            expanded_list.append(value)
        return expanded_list
    
    @staticmethod
    def __expand_item(value):
        if isinstance(value, Mapping):
            value = Struct.__expand_mapping(value)
        elif isinstance(value, list):
            value = Struct.__expand_list(value)
        return value

        self.__dict__.update(new_entries)
    def __getitem__(self, item):
         return self.__dict__[item]
"""