from abc import ABC, abstractmethod

from thewall.domains import Team, WallSection


class TheWallLog(ABC):

    @abstractmethod
    def add(self, profile_id: int, section: WallSection, team: Team, day: int):
        pass