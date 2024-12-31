import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from model import Base, ModuleInfo, Property
import constant

id = 0
date = datetime.date.today()

sqlite='sqlite:///../data/sqlite.db'


def init():
    engine = create_engine(sqlite, echo=True)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        demona = ModuleInfo(id=0, name="Demona", ip="3.64.204.102", port=5121)
        thalie = ModuleInfo(id=1, name="Thalie", ip="78.108.108.89", port=5121)
        demona2 = ModuleInfo(id=2, name="Demona EE", ip="78.108.108.89", port=25121)
        equilibrie2 = ModuleInfo(id=3, name="Equilibrie EE", ip="176.102.64.93", port=5121)

        session.merge(demona)
        session.merge(thalie)
        session.merge(demona2)
        session.merge(equilibrie2)

        session.merge(Property(key="NWN_CHECKER_URL", value=constant.NWN_CHECKER_URL))
        session.merge(Property(key="NWN_CHECKER_URL_PLAYER_COUNT_REGEX", value=constant.NWN_CHECKER_URL_PLAYER_COUNT_REGEX))
        session.merge(Property(key="NWN_CHECKER_URL_SERVER_OFFLINE_REGEX", value=constant.NWN_CHECKER_URL_SERVER_OFFLINE_REGEX))
        session.merge(Property(key="NWN_CHECKER_URL_INTERVAL_CRON_PER_HOUR", value=constant.NWN_CHECKER_URL_INTERVAL_CRON_PER_HOUR))
        session.merge(Property(key="PASSWORD_SHA_3_512", value=constant.PASSWORD_SHA_3_512))
        session.merge(Property(key="NWN_CHECKER_URL_PLAYER_COUNT_REGEX_GROUP_0_X", value=constant.NWN_CHECKER_URL_PLAYER_COUNT_REGEX_GROUP_0_X))
        session.merge(Property(key="NWN_CHECKER_URL_INTERVAL_UPDATE_DB_SECONDS", value=constant.NWN_CHECKER_URL_INTERVAL_UPDATE_DB_SECONDS))

        session.commit()


if __name__ == '__main__':
    init()
