from dataclasses import dataclass
import time
from typing import List


MAX_HEIGHT = 30


@dataclass
class WallSection:
    id: int
    current_height: int
    final_height: int = MAX_HEIGHT

    @property
    def finished(self) -> bool:
        return self.current_height >= self.final_height


@dataclass
class WallProfile:
    id: int
    sections: List[WallSection]


class Team:

    def __init__(self, id: str, power: int = 1, _sleep: float = 1) -> None:
        self.id = id
        self.power = power # foots per day
        self._sleep = _sleep # sleep per foot

    
    def build(self, section: WallSection) -> int:
        time.sleep(self._sleep * self.power)
        section.current_height = min(section.current_height + self.power, section.final_height)
