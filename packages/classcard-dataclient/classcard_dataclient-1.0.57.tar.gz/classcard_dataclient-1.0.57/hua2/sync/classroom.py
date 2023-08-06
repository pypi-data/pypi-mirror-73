import datetime
import pymssql
from sync.base import BaseSync
from utils.loggerutils import logging
from classcard_dataclient.models.classroom import Classroom, RoomType
from config import SQLSERVER_HOST, SQLSERVER_USER, SQLSERVER_PW, SQLSERVER_DB

logger = logging.getLogger(__name__)


class ClassroomSync(BaseSync):
    def __init__(self):
        super(ClassroomSync, self).__init__()
        self.db = pymssql.connect(server=SQLSERVER_HOST, user=SQLSERVER_USER, password=SQLSERVER_PW,
                                  database=SQLSERVER_DB)
        now = datetime.datetime.now()
        self.offset = 300
        self.cur = self.db.cursor()
        self.classroom_list = []
        self.classroom_map = {}
        self.building_map = {}

    def extract_building(self):
        sql = "SELECT id, areaname, pid, levf FROM mid_areainfo WHERE levf=1 ORDER BY id"
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        for row in rows:
            external_id, name, parent_id, level = row[0], row[1], row[2], row[3]
            self.building_map[external_id] = name

    def extract_classroom(self):
        sql = "SELECT id, areaname, pid, levf FROM mid_areainfo WHERE levf=2 ORDER BY id"
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        for row in rows:
            external_id, name, parent_id, level = row[0], row[1], row[2], row[3]
            building = self.building_map.get(parent_id, None)
            try:
                name_info = name.split("-")
                floor = name_info[-1][0] if len(name_info[-1]) <= 3 else name_info[-1][:2]
            except (Exception, ):
                floor = None
            classroom = Classroom(number=str(external_id), name=name, building=building,
                                  floor=floor, school=self.school_id, category=RoomType.TYPE_PUBLIC)
            self.classroom_list.append(classroom)
            self.classroom_map[str(external_id)] = str(external_id)

    def sync(self):
        self.extract_building()
        self.extract_classroom()
        if not self.classroom_map:
            logger.info("没有教室信息")
            return
        self.client.create_classrooms(self.school_id, self.classroom_list)
        self.cur.close()
        self.db.close()
