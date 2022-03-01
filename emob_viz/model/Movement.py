import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class Movement:
    time: datetime.datetime
    type: str
    lat: float
    lon: float

    @classmethod
    def from_tuple(cls, tpl: tuple):
        return Movement(tpl[0], tpl[1], float(tpl[2]), float(tpl[3]))
