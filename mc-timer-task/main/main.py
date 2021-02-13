
from main.util.config import Config
from main.services.task_note_service import TaskNoteService
from main.util.job import ProgramKilled

config = Config()
task_note_service = TaskNoteService(config)