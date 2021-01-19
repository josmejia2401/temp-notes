
from bson import ObjectId
from main.db.db import MongoDatabase

class NoteService(object):
    
    def __init__(self, config = {}):
        self.__db_client = MongoDatabase(config)
        self.__db_client.connect()
        self.__db = self.__db_client.get_db()
        self.__collection = self.__db['temp_notes']

    def insert(self, username=None, payload=None) -> str:
        if not payload or not username:
            return None
        payload['username'] = username
        response = self.__collection.insert_one(payload)
        if response:
            oid = str(response.inserted_id)
            document = self.__collection.find_one({"username": username, "_id": ObjectId(oid) })
            if document:
                document['id'] = str(document['_id'])
                del document['_id']
                return document
        return None

    def get(self, username=None, noteId=None) -> any:
        if not username or not noteId:
            return None
        document = self.__collection.find_one({"username": username, "_id": ObjectId(noteId)})
        if document:
            document['id'] = str(document['_id'])
            del document['_id']
        return document

    def get_all(self, username=None) -> any:
        documents = list(self.__collection.find({"username": username}))
        if documents and isinstance(documents, list):
            for document in documents:
                document['id'] = str(document['_id'])
                del document['_id']
        return documents

    def update(self, username=None, noteId=None, payload = None) -> str:
        updated_payload = { "$set": payload }
        where_payload = { "username": username, "_id": ObjectId(noteId) }
        response = self.__collection.update_one(where_payload, updated_payload, upsert=False)
        if response and response.modified_count > 0:
            document = self.__collection.find_one({"username": username, "_id": ObjectId(noteId) })
            if document:
                document['id'] = str(document['_id'])
                del document['_id']
                return document
        return None

    def delete(self, username=None, noteId=None) -> int:
        where_payload = { "username": username, "_id": ObjectId(noteId)}
        response = self.__collection.delete_one(where_payload)
        return response.deleted_count