
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
            timer_config = self.__config.get_object('timer')
            result = self.__note_services.get_all(days=int(timer_config['days_of_grace']))
            print('run_task', result)
            self.__delete_note()
        except Exception as e:
            logger.error('run_task', e)
    
    def __delete_note(self):
        pass