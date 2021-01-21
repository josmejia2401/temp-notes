
from main.services.note_service import NoteService
from main.db.entity.note import NoteEntity

class NoteController(object):

    def __init__(self, config = {}):
        self.__noteService = NoteService(config)

    def insert(self, username=None, payload=None) -> any:
        try:
            note = NoteEntity(payload)
            note.validate(['title', 'description'])
            return self.__noteService.insert(username=username, payload=note.get_json())
        except Exception as e:
            raise e

    def get(self, username=None, noteId=None) -> any:
        try:
            if not username or not noteId:
                raise Exception('username or noteId not found') 
            result = self.__noteService.get(username, noteId)
            return result
        except Exception as e:
            raise e

    def get_all(self, username=None) -> any:
        try:
            if not username:
                raise Exception('username not found') 
            return self.__noteService.get_all(username)
        except Exception as e:
            raise e

    def update(self, username=None, noteId=None, payload=None) -> any:
        try:
            if not payload or not username or not noteId:
                raise Exception('payload or username or noteId not found') 
            payload['username'] = username
            note = NoteEntity(payload)
            note.validate(['title', 'description'])
            return self.__noteService.update(username, noteId, note.get_json())
        except Exception as e:
            raise e

    def delete(self, username=None, noteId=None) -> any:
        try:
            if not username or not noteId:
                raise Exception('username or noteId not found')
            return self.__noteService.delete(username, noteId)
        except Exception as e:
            raise e