from dataclasses import dataclass

@dataclass
class League():
    rank: str
    bast_rank: str
    rating: int

    apm: float
    pps: float
    vs: float
