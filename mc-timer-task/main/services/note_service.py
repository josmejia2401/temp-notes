
from bson import ObjectId
from main.db.db import MongoDatabase
from datetime import date, datetime, timedelta

class NoteService(object):
    
    def __init__(self, config = {}):
        self.__db_client = MongoDatabase(config)
        self.__db_client.connect()
        self.__db = self.__db_client.get_db()
        self.__collection = self.__db['temp_notes']

    def get_all(self, days: int = 5) -> any:
        d = datetime.now() - timedelta(days=days)
        date_string = d.isoformat()
        documents = list(self.__collection.find({"updateAt": { "$lt": date_string } }))
        if documents and isinstance(documents, list):
            for document in documents:
                document['id'] = str(document['_id'])
                del document['_id']
        return documents

    def delete(self, username=None, noteId=None) -> int:
        where_payload = { "username": username, "_id": ObjectId(noteId)}
        response = self.__collection.delete_one(where_payload)
        return response.deleted_count
    
    def delete_many(self, days: int = 5) -> int:
        d = datetime.now() - timedelta(days=days)
        date_string = d.isoformat()
        where_payload = { "updateAt": { "$lt": date_string } }
        response = self.__collection.delete_many(where_payload)
        return response.deleted_count