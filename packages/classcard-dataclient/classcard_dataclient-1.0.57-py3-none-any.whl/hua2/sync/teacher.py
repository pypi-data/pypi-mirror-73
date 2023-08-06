import datetime
import pymssql
from sync.base import BaseSync
from utils.loggerutils import logging
from classcard_dataclient.models.user import Student, Teacher, GenderSet
from config import SQLSERVER_HOST, SQLSERVER_USER, SQLSERVER_PW, SQLSERVER_DB

logger = logging.getLogger(__name__)


class TeacherSync(BaseSync):
    def __init__(self):
        super(TeacherSync, self).__init__()
        self.db = pymssql.connect(server=SQLSERVER_HOST, user=SQLSERVER_USER, password=SQLSERVER_PW,
                                  database=SQLSERVER_DB)
        now = datetime.datetime.now()
        self.offset = 300
        self.cur = self.db.cursor()
        self.teacher_list = []
        self.teacher_map = {}

    def extract_teacher(self):
        sex_map = {0: GenderSet.FEMALE, 1: GenderSet.MALE}
        sql = "SELECT id, OUTID, NAME, Sex, CARDSFID FROM BASE_CUSTOMERS " \
              "WHERE CARDSFID=0 ORDER BY OUTID"
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        for row in rows:
            external_id, number, name, sex, role_id = row[0], row[1], row[2], row[3], row[4]
            gender = sex_map.get(sex, GenderSet.MALE)
            if external_id not in self.teacher_map:
                teacher = Teacher(number=number, name=name, password="MTIzNDU2", gender=gender,
                                  email="teacher{}@edt.com".format(number), birthday="1980-01-01",
                                  phone='0000000', school=self.school_id)
                self.teacher_map[external_id] = number
                self.teacher_list.append(teacher)

    def sync(self):
        self.extract_teacher()
        if not self.teacher_map:
            logger.info("没有老师信息")
            return
        code, data = self.client.create_teacher(self.teacher_list)
        logger.info("Code: {}, Msg: {}".format(code, data))
        self.cur.close()
        self.db.close()
