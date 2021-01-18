
from main.util.job import Task
from main.services.note_service import NoteService

class TaskNoteService(Task):
    
    def __init__(self, config = {}):
        super().__init__(config)
        self.__config = config
        self.__note_services = NoteService(config)

    def run_task(self):
        timer_config = self.__config.get_object('timer')
        result = self.__note_services.get_all(days=int(timer_config['days_of_grace']))
        print('run_task', result)
        self.__delete_note()
    
    def __delete_note(self):
        pass