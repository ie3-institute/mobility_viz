import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    time: datetime.datetime
    id: str
    is_charging: bool
    lat: float
    lon: float

    @classmethod
    def from_tuple(cls, tpl: tuple):
        return Position(tpl[0], tpl[1], tpl[2], float(tpl[3]), float(tpl[4]))
