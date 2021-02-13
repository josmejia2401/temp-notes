
import time
from main.main import task_note_service, ProgramKilled
from main.log.log import logger

if __name__ == '__main__':
    task_note_service.run()
    while True:
        try:
            time.sleep(5)
        except ProgramKilled as e:
            print('ProgramKilled', e)
            logger.error('ProgramKilled', e)
            task_note_service.stop()
            break
        except Exception as e:
            print('Exception', e)
            logger.error('Exception', e)
            task_note_service.stop()
            break
