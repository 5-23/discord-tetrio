from .badge import *
from .league import *
from .solo import *

@dataclass
class Data():
    name: str
    nick: str
    discord_name: str
    friend: int
    gametime: int
    gameplayed: int
    gamewon: int


    badges: list[Badge]
    league: League

    l40: Solo
    blitz: Solo

    avatar_img: str
    banner_img: str