import json


class Config(object):
    
    def __init__(self):
        self.__config_json = None
        self.__load_json()

    def ___load_json(self):
        with open('resources/config.json') as json_file:
            self.__config_json = json.load(json_file)

    def get_config(self) -> any:
        return self.__config_json
    
    def get_object(self, name: str) -> any:
        return self.__config_json[name]
