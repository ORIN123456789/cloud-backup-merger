from enum import Enum
from dataclasses import dataclass

@dataclass
class Account:
    name: str
    credentials: str

class RunTypeEnum(Enum):
    NO_DASHBOARD = "no_dashboard"
    ALBUMS = "albums"
    ACCOUNTS = "accounts"


