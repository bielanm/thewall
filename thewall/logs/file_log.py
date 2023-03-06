

from pathlib import Path
import threading
from thewall.domains import Team, WallSection
from .base_log import TheWallLog


class FileLog(TheWallLog):

    def __init__(self, path: Path):
        if path.exists():
            path.unlink()
        path.parent.mkdir(exist_ok=True, parents=True)
        self._path = path
        self._lock = threading.Lock()
    
    def add(self, profile_id: int, section: WallSection, team: Team, day: int):
        # Better be replaced with thread safe "logging" module instead of threading.Lock()
        self._lock.acquire()
        with self._path.open('a') as fout:
            message = (

                f"Day#{day}: team#{team.id} worked on section#{section.id} of wall profile#{profile_id}. "
                f"Built {team.power} foots. "
                f"Current section state {section.current_height}/{section.final_height}. "
                f"Finished: {section.finished}"
            )
            fout.write(message)
            fout.write('\n')
        print(message) # TODO: replace with separate StdoutLog
        self._lock.release()
