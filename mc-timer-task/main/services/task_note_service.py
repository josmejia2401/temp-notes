
from main.util.job import Task
from main.services.note_service import NoteService
from main.log.log import logger

class TaskNoteService(Task):
    
    def __init__(self, config = {}):
        super().__init__(config)
        self.__config = config
        self.__note_services = NoteService(config)

    def run_task(self):
        try:
            logger.info('Iniciando la tarea programada')
            timer_config = self.__config.get_object('timer')
            result = self.__note_services.delete_many(days=int(timer_config['days_of_grace']))
            logger.info('Eliminando notas. Cantidad {}'.format(result))
        except Exception as e:
            logger.error('run_task', e)