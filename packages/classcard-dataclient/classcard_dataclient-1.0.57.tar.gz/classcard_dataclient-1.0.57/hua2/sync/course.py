import datetime
import uuid
import pymssql
from sync.base import BaseSync
from utils.loggerutils import logging
from utils.code import get_md5_hash
from classcard_dataclient.models.course import CourseV2, CourseTableManagerV2, TableCategory, WalkingModeSet
from config import SQLSERVER_HOST, SQLSERVER_USER, SQLSERVER_PW, SQLSERVER_DB

logger = logging.getLogger(__name__)


class CourseSync(BaseSync):
    def __init__(self):
        super(CourseSync, self).__init__()
        self.db = pymssql.connect(server=SQLSERVER_HOST, user=SQLSERVER_USER, password=SQLSERVER_PW,
                                  database=SQLSERVER_DB)
        self.offset = 300
        self.cur = self.db.cursor()
        self.course_map = {}
        self.space_map = {}
        self.slot_map = {}
        self.student_map = {}
        self.teacher_map = {}
        self.classroom_map = {}
        self.rest_table = None
        self.semester = None

    def extract_course(self):
        today, last_day = self.get_date_range()
        sql = "SELECT id, coursename, sectionid, classroomid, coursedate, weekday, userid, isteacher " \
              "FROM mid_attendschedule " \
              "WHERE coursedate > {} and coursedate <= {} ORDER BY weekday".format(today, last_day)
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        for row in rows:
            category = TableCategory.ALL
            attend_id, subject_name, slot_id = row[0], row[1], row[2]
            classroom_id, course_date, week = row[3], row[4], row[5]
            user_id, is_teacher = row[6], row[7]
            unique_key = "{}_{}".format(subject_name, classroom_id)
            course_number = get_md5_hash(unique_key)
            subject_number = get_md5_hash(subject_name)
            num = self.slot_map.get(slot_id, None)
            classroom_number = self.classroom_map.get(str(classroom_id))
            if not num:
                print("Can't Find SlotID {}".format(slot_id))
                continue
            if unique_key not in self.course_map:
                course_data = {'name': subject_name, 'number': course_number, 'subject_number': subject_number,
                               "subject_name": subject_name, "class_name": class_name,
                               'classroom_number': classroom_number, 'is_walking': False,
                               "teacher_number": None, "begin_week": 1, "end_week": 8, 'student_list': []}
                course = CourseV2(**course_data)
                self.course_map[unique_key] = course
            else:
                course = self.course_map[unique_key]
            if is_teacher:
                teacher_number = self.teacher_map.get(user_id, None)
                course.teacher_number = teacher_number
            else:
                student_number = self.student_map.get(user_id, None)
                course.add_student(student_number)
            course.add_position(num, week, category, classroom_number)

    def sync(self):
        self.extract_course()
        if not self.course_map:
            logger.info("没有课程信息")
            return
        begin_date, end_date = self.get_date_range(days=60)
        course_table_name = "{}课表_{}".format(self.semester.name, str(uuid.uuid4())[:4])
        course_table_number = get_md5_hash(course_table_name)[:20]
        course_table = CourseTableManagerV2(name=course_table_name, number=course_table_number,
                                            rest_name=self.rest_table.name, walking_mode=WalkingModeSet.WALKING,
                                            begin_date=begin_date, end_date=end_date, semester_name=self.semester.name)
        course_table.classrooms_num = list(self.classroom_map.values())
        course_table.courses = list(self.course_map.values())
        print(">>> CREATE_COURSE_TABLE")
        logger.info(">>> CREATE_COURSE_TABLE")
        self.client.create_course_table(self.school_id, course_table, is_active=True)
        self.client.active_semester(self.school_id, self.semester, delete_other=True)
        self.cur.close()
        self.db.close()
