import json
from pathlib import Path
import os

class Config(object):
    
    def __init__(self):
        self.__config_json = None
        self.__load_json()

    def __load_json(self):
        current_dir = Path(__file__).parent
        file_path = os.path.join(current_dir, 'resources', 'config.json')
        contBreak = 0
        while os.path.exists(file_path) == False:
            if contBreak > 3: break
            current_dir = Path(current_dir).parent
            file_path = os.path.join(current_dir, 'resources', 'config.json')
            contBreak += 1
        with open(file_path) as json_file:
            self.__config_json = json.load(json_file)

    def get_config(self) -> any:
        return self.__config_json
    
    def get_object(self, name: str) -> any:
        return self.__config_json[name]
