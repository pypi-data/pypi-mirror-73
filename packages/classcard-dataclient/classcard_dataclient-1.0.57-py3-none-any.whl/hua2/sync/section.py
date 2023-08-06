import datetime
import pymssql
from sync.base import BaseSync
from utils.loggerutils import logging
from classcard_dataclient.models import Class
from config import SQLSERVER_HOST, SQLSERVER_USER, SQLSERVER_PW, SQLSERVER_DB

logger = logging.getLogger(__name__)


class SectionSync(BaseSync):
    def __init__(self):
        super(SectionSync, self).__init__()
        self.db = pymssql.connect(server=SQLSERVER_HOST, user=SQLSERVER_USER, password=SQLSERVER_PW,
                                  database=SQLSERVER_DB)
        now = datetime.datetime.now()
        self.offset = 300
        self.cur = self.db.cursor()
        self.section_map = {}

    def extract_section(self):
        sql = "SELECT id, ecode, dpcode, dpname FROM BASE_CUSTDEPT ORDER BY id"
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        for row in rows:
            external_id, ecode, code, name = row[0], row[1], row[2], row[3]
            section = Class(name=name, number=code, school=self.school_id)
            self.section_map[code] = section

    def sync(self):
        self.extract_section()
        if not self.section_map:
            logger.info("没有班级信息")
            return
        for code, section in self.section_map.items():
            code, data = self.client.create_section(sections=section)
            if code:
                logger.error("Code: {}, Msg: {}".format(code, data))
        self.cur.close()
        self.db.close()
