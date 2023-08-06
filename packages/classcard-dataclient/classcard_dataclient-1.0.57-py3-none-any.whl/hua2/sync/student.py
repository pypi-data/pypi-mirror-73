import datetime
import pymssql
from sync.base import BaseSync
from utils.loggerutils import logging
from classcard_dataclient.models.user import Student, Teacher, GenderSet
from config import SQLSERVER_HOST, SQLSERVER_USER, SQLSERVER_PW, SQLSERVER_DB

logger = logging.getLogger(__name__)


class StudentSync(BaseSync):
    def __init__(self):
        super(StudentSync, self).__init__()
        self.db = pymssql.connect(server=SQLSERVER_HOST, user=SQLSERVER_USER, password=SQLSERVER_PW,
                                  database=SQLSERVER_DB)
        now = datetime.datetime.now()
        self.offset = 300
        self.cur = self.db.cursor()
        self.student_list = []
        self.student_map = {}

    def get_section_map(self):
        code, sections = self.client.get_section_list(school_id=self.school_id)
        if code or not isinstance(sections, list):
            logger.error("Error: get section info, Detail: {}".format(sections))
            sections = []
        section_map = {d["number"]: d['uuid'] for d in sections if d.get("number")}
        return section_map

    def extract_student(self):
        section_map = self.get_section_map()
        sex_map = {0: GenderSet.FEMALE, 1: GenderSet.MALE}
        sql = "SELECT id, OUTID, NAME, Sex, CARDSFID, CUSTDEPT FROM BASE_CUSTOMERS " \
              "WHERE CARDSFID=1 ORDER BY OUTID"
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        for row in rows:
            external_id, number, name, sex, role_id, section_num = row[0], row[1], row[2], row[3], row[4], row[5]
            gender = sex_map.get(sex, GenderSet.MALE)
            if external_id not in self.student_map:
                section_id = section_map.get(section_num, None)
                student = Student(number=number, name=name, password="MTIzNDU2", gender=gender, birthday="1996-01-01",
                                  section=section_id, classof=2018, graduateat=2021, school=self.school_id)
                self.student_map[external_id] = number
                self.student_list.append(student)

    def sync(self):
        self.extract_student()
        if not self.student_map:
            logger.info("没有学生信息")
            return
        code, data = self.client.create_student(self.student_list)
        logger.info("Code: {}, Msg: {}".format(code, data))
        self.cur.close()
        self.db.close()
