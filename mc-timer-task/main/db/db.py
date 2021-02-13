
import abc
from pymongo import MongoClient
from pymongo.errors import AutoReconnect
from main.util.db_util import retry

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
# https://api.mongodb.com/python/3.3.0/api/pymongo/mongo_client.html
class MongoDatabase(Database):
    def __init__(self, config = {}):
        super().__init__()
        self.__config = config
        self.__client = None

    def connect(self):
        try:
            print('conecting to MongoDB!')
            db_config = self.__config.get_object('db')
            general_config = self.__config.get_object('general')
            # variables
            uri = db_config['uri2']
            name = db_config['name']
            maxPoolSize = None if db_config['maxPoolSize'] == 0 else db_config['maxPoolSize']
            minPoolSize = 0 if db_config['minPoolSize'] == 0 else db_config['minPoolSize']
            maxIdleTimeMS = None if db_config['maxIdleTimeMS'] == 0 else db_config['maxIdleTimeMS']
            socketTimeoutMS = None if db_config['socketTimeoutMS'] == 0 else db_config['socketTimeoutMS']
            connectTimeoutMS = None if db_config['connectTimeoutMS'] == 0 else db_config['connectTimeoutMS']
            serverSelectionTimeoutMS = None if db_config['serverSelectionTimeoutMS'] == 0 else db_config['serverSelectionTimeoutMS']
            appName = general_config['appName']
            # conexion
            self.__client = MongoClient(host=uri,
                                        appname=appName,
                                        maxPoolSize=maxPoolSize,#el número máximo permitido de conexiones simultáneas a cada servidor conectado. Las solicitudes a un servidor se bloquearán si hay conexiones pendientes de maxPoolSize al servidor solicitado. El valor predeterminado es 100. No puede ser 0.
                                        minPoolSize=minPoolSize,#el número mínimo requerido de conexiones simultáneas que el grupo mantendrá en cada servidor conectado. El valor predeterminado es 0.
                                        maxIdleTimeMS=maxIdleTimeMS,#a cantidad máxima de milisegundos que una conexión puede permanecer inactiva en el grupo antes de ser eliminada y reemplazada. El valor predeterminado es Ninguno (sin límite).
                                        socketTimeoutMS=socketTimeoutMS,#Controla cuánto tiempo (en milisegundos) el controlador esperará una respuesta después de enviar una operación de base de datos normal (sin supervisión) antes de concluir que se ha producido un error de red. El valor predeterminado es Ninguno (sin tiempo de espera).
                                        connectTimeoutMS=connectTimeoutMS,#Controla cuánto tiempo (en milisegundos) esperará el controlador durante la supervisión del servidor cuando se conecta un nuevo socket a un servidor antes de concluir que el servidor no está disponible. El valor predeterminado es 20000 (20 segundos).
                                        serverSelectionTimeoutMS=serverSelectionTimeoutMS#Controla cuánto tiempo (en milisegundos) esperará el controlador para encontrar un servidor apropiado disponible para llevar a cabo una operación de base de datos; mientras está esperando, se pueden realizar múltiples operaciones de monitoreo del servidor, cada una controlada por connectTimeoutMS . El valor predeterminado es 30000 (30 segundos).
                                        )
            print('conected to MongoDB!')
        except Exception as e:
            print('MongoDatabase.connect', e)
            raise e

    def disconnect(self):
        if self.__client:
            self.__client.close()

    @retry_auto_reconnect
    def reconnect(self):
        print('reconecting to MongoDB!')
        db_config = self.__config.get_object('db')
        general_config = self.__config.get_object('general')
        # variables
        uri = db_config['uri2']
        name = db_config['name']
        maxPoolSize = None if db_config['maxPoolSize'] == 0 else db_config['maxPoolSize']
        minPoolSize = 0 if db_config['minPoolSize'] == 0 else db_config['minPoolSize']
        maxIdleTimeMS = None if db_config['maxIdleTimeMS'] == 0 else db_config['maxIdleTimeMS']
        socketTimeoutMS = None if db_config['socketTimeoutMS'] == 0 else db_config['socketTimeoutMS']
        connectTimeoutMS = None if db_config['connectTimeoutMS'] == 0 else db_config['connectTimeoutMS']
        serverSelectionTimeoutMS = None if db_config['serverSelectionTimeoutMS'] == 0 else db_config['serverSelectionTimeoutMS']
        appName = general_config['appName']
        # conexion
        self.__client = MongoClient(host=uri,
                                    appname=appName,
                                    maxPoolSize=maxPoolSize,#el número máximo permitido de conexiones simultáneas a cada servidor conectado. Las solicitudes a un servidor se bloquearán si hay conexiones pendientes de maxPoolSize al servidor solicitado. El valor predeterminado es 100. No puede ser 0.
                                    minPoolSize=minPoolSize,#el número mínimo requerido de conexiones simultáneas que el grupo mantendrá en cada servidor conectado. El valor predeterminado es 0.
                                    maxIdleTimeMS=maxIdleTimeMS,#a cantidad máxima de milisegundos que una conexión puede permanecer inactiva en el grupo antes de ser eliminada y reemplazada. El valor predeterminado es Ninguno (sin límite).
                                    socketTimeoutMS=socketTimeoutMS,#Controla cuánto tiempo (en milisegundos) el controlador esperará una respuesta después de enviar una operación de base de datos normal (sin supervisión) antes de concluir que se ha producido un error de red. El valor predeterminado es Ninguno (sin tiempo de espera).
                                    connectTimeoutMS=connectTimeoutMS,#Controla cuánto tiempo (en milisegundos) esperará el controlador durante la supervisión del servidor cuando se conecta un nuevo socket a un servidor antes de concluir que el servidor no está disponible. El valor predeterminado es 20000 (20 segundos).
                                    serverSelectionTimeoutMS=serverSelectionTimeoutMS#Controla cuánto tiempo (en milisegundos) esperará el controlador para encontrar un servidor apropiado disponible para llevar a cabo una operación de base de datos; mientras está esperando, se pueden realizar múltiples operaciones de monitoreo del servidor, cada una controlada por connectTimeoutMS . El valor predeterminado es 30000 (30 segundos).
                                    )
        print('reconected to MongoDB!')

    def get_db(self, name: str = None):
        if name and self.__client:
            return self.__client[name]
        elif self.__client:
            db_config = self.__config.get_object('db')
            name = db_config['name']
            return self.__client[name]
        else:
            raise Exception('No se encuentra el cliente DB')
