import time
import datetime
import traceback
from classcard_dataclient.client.action import DataClientV2
from config import SCHOOL_NAME
from utils.dateutils import date2str
from utils.loggerutils import logging

logger = logging.getLogger(__name__)


class BaseSync(object):
    def __init__(self):
        self.client = DataClientV2()
        code, school = self.client.get_school_by_name(SCHOOL_NAME)
        if code:
            logger.error("Error: get school info, Detail: {}".format(school))
        self.school_id = school.get("uuid")
        
    def get_date_range(self, days=7):
        now = datetime.datetime.now()
        last_datetime = now + datetime.timedelta(days=days)
        today, last_day = date2str(now.date()), date2str(last_datetime.date())
        return today, last_day

    @NotImplementedError
    def sync(self):
        pass

    def start(self):
        try:
            logger.info(">>> Start {} On:".format(self.__class__.__name__, datetime.datetime.now()))
            self.sync()
        except (Exception,):
            logger.error(">>> Error: sync error, Detail: {}".format(traceback.print_exc()))
            time.sleep(10)
        finally:
            logger.info(">>> Finish {} On:".format(self.__class__.__name__, datetime.datetime.now()))
