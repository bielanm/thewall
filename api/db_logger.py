from pathlib import Path
import threading
from api.models.work_model import WorkExpenseModel
from thewall.domains import Team, WallSection
from thewall.logs.base_log import TheWallLog


class DbLoger(TheWallLog):
    
    def add(self, profile_id: int, section: WallSection, team: Team, day: int):
        model = WorkExpenseModel(
            profile = profile_id,
            day = day,
            ice = team.power
        )
        model.save()
