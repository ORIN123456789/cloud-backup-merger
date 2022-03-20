from common_objects import RunTypeEnum
from runners import accounts_dashboard, albums_dashboard, cmd_runner
from exceptions import NoSuchRunner


def RunnersFactory(_type=RunTypeEnum.ACCOUNTS):
    runners = {
        RunTypeEnum.ACCOUNTS: accounts_dashboard.AccountsDashboard,
        RunTypeEnum.ALBUMS: albums_dashboard.AlbumsDashboard,
        RunTypeEnum.NO_DASHBOARD: cmd_runner.CMD
    }
    if _type not in runners:
        raise NoSuchRunner
    return runners[_type]()

