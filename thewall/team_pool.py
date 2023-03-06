

import collections
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
import threading
from typing import Dict, List

from thewall.domains import Team, WallSection
from thewall.lib.iterator import infinite
from thewall.logs.base_log import TheWallLog


@dataclass
class Task:
    profile_id: int
    section: WallSection



class TeamPool(ThreadPoolExecutor):
    """
        Class extends `concurrent.futures.ThreadPoolExecutor` and
        represent pool of teams where each team corresponds to a work 
        that gonna be done inside each separate thread.
    """

    def __init__(self, teams: List[Team], loggers: List[TheWallLog]) -> None:
        super().__init__(max_workers=len(teams), thread_name_prefix='team_')
        self._day_memo = collections.defaultdict(lambda: 1)
        self._teams: List[Team] = teams
        self._loggers: List[TheWallLog] = loggers
        self._teams_thread_mapping: Dict[str, Team] = {}
    
    def _day_generator(self):
        team = self._get_current_team()
        for i in infinite(start=self._day_memo[team.id]):
            self._day_memo[team.id] = i + 1
            yield i
    
    def _get_current_team(self) -> Team:
        thread_name = threading.current_thread().name
        if thread_name not in self._teams_thread_mapping:
            team_idx = len(self._teams_thread_mapping)
            self._teams_thread_mapping[thread_name] = self._teams[team_idx]
        return self._teams_thread_mapping[thread_name]


    def process_one_section(self, task: Task):
        team = self._get_current_team()
        if task.section.finished:
            return

        for day in self._day_generator():
            team.build(task.section)
            for logger in self._loggers:
                logger.add(profile_id=task.profile_id, section=task.section, team=team, day=day)
            if task.section.finished:
                return

    def process(self, tasks: List[Task]):
        self.map(self.process_one_section, tasks)
