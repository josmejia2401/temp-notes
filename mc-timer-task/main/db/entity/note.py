import json
import datetime


class NoteEntity(object):
    def __init__(self, json_data={}):
        self.id = None
        self.username = None
        self.title = None
        self.username = None
        if 'title' in json_data and json_data['title']:
            self.title = json_data['title']
        if 'description' in json_data and json_data['description']:
            self.description = json_data['description']
        if 'username' in json_data and json_data['username']:
            self.username = json_data['username']
        self.updateAt = datetime.datetime.utcnow()
        self.createAt = datetime.datetime.utcnow()

    def validate_all(self):
        if not self.title:
            raise Exception('title not found')
        if not self.description:
            raise Exception('description not found')
        if not self.username:
            raise Exception('username not found')
    
    def validate(self, validate_items = []):
        for item in validate_items:
            if item in self.__dict__:
                if not self.__dict__[item]:
                    raise Exception(item + ' not found')
            else:
                raise Exception(item + ' not found 2') 

    def get_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'username': self.username,
            'updateAt': self.updateAt.isoformat(),
            'createAt': self.createAt.isoformat()
        }
