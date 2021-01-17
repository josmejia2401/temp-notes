
import abc
from pymongo import MongoClient
from pymongo.errors import AutoReconnect
from util.config import Config
from util.db_util import retry

retry_auto_reconnect = retry(3, (AutoReconnect,))


class Database(abc.ABC):

    def __init__(self):
        pass

    @abc.abstractmethod
    def connect(self):
        pass

    @abc.abstractmethod
    def disconnect(self):
        pass

    @abc.abstractmethod
    def reconnect(self):
        pass

    @abc.abstractmethod
    def get_db(self, name):
        pass

# @Database.register


class MongoDatabase(Database):
    def __init__(self):
        super().__init__()
        self.__config = Config()
        self.__client = None

    def connect(self):
        try:
            db_config = self.__config.get_object('db')
            general_config = self.__config.get_object('general')
            # variables
            uri = db_config['uri']
            name = db_config['name']
            maxPoolSize = db_config['maxPoolSize']
            minPoolSize = db_config['minPoolSize']
            maxIdleTimeMS = db_config['maxIdleTimeMS']
            socketTimeoutMS = db_config['socketTimeoutMS']
            connectTimeoutMS = db_config['connectTimeoutMS']
            serverSelectionTimeoutMS = db_config['serverSelectionTimeoutMS']
            appName = general_config['appName']
            # conexion
            self.__client = MongoClient(host=uri,
                                        appname=appName,
                                        maxPoolSize=maxPoolSize,
                                        minPoolSize=minPoolSize,
                                        maxIdleTimeMS=maxIdleTimeMS,
                                        socketTimeoutMS=socketTimeoutMS,
                                        connectTimeoutMS=connectTimeoutMS,
                                        serverSelectionTimeoutMS=serverSelectionTimeoutMS)
        except Exception as e:
            pass

    def disconnect(self):
        if self.__client:
            self.__client.close()

    @retry_auto_reconnect
    def reconnect(self):
        db_config = self.__config.get_object('db')
        general_config = self.__config.get_object('general')
        # variables
        uri = db_config['uri']
        name = db_config['name']
        maxPoolSize = db_config['maxPoolSize']
        minPoolSize = db_config['minPoolSize']
        maxIdleTimeMS = db_config['maxIdleTimeMS']
        socketTimeoutMS = db_config['socketTimeoutMS']
        connectTimeoutMS = db_config['connectTimeoutMS']
        serverSelectionTimeoutMS = db_config['serverSelectionTimeoutMS']
        appName = general_config['appName']
        self.__client = MongoClient(host=uri,
                                    appname=appName,
                                    maxPoolSize=maxPoolSize,
                                    minPoolSize=minPoolSize,
                                    maxIdleTimeMS=maxIdleTimeMS,
                                    socketTimeoutMS=socketTimeoutMS,
                                    connectTimeoutMS=connectTimeoutMS,
                                    serverSelectionTimeoutMS=serverSelectionTimeoutMS)

    def get_db(self, name):
        pass
