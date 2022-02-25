from dataclasses import dataclass


@dataclass
class Poi:
    id: str
    size: float
    lat: float
    lon: float
    type: str

    @classmethod
    def from_tuple(cls, tpl: tuple):
        return Poi(tpl[0], float(tpl[1]), float(tpl[2]), float(tpl[3]), str(tpl[4]))
