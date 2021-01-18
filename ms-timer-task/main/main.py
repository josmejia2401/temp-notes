
from flask import Flask, request, Response
from main.util.config import Config
from main.services.task_note_service import TaskNoteService
from main.util.job import ProgramKilled

app = Flask(__name__)
config = Config()
task_note_service = TaskNoteService(config)