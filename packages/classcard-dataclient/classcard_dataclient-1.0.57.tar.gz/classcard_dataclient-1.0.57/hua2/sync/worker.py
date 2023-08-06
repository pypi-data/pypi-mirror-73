import time
from sync.student import StudentSync
from utils.loggerutils import logging

logger = logging.getLogger(__name__)


# def table_sync():
#     start_time = time.time()
#     course_table_sync = CourseTableSync()
#     course_table_sync.need_relate_student = False
#     course_table_sync.start()
#     logger.info("course table sync used: {}s".format(round(time.time() - start_time, 4)))
#     start_exam_sync()


def start_exam_sync():
    start_time = time.time()
    exam_sync = StudentSync()
    exam_sync.start()
    logger.info("exam sync used: {}s".format(round(time.time() - start_time, 4)))
