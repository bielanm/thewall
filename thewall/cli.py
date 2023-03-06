

import collections
from pathlib import Path
from typing import List

from thewall.domains import Team, WallProfile, WallSection
from thewall.team_pool import Task, TeamPool
from thewall.logs.file_log import FileLog
from thewall.lib.iterator import infinite

import typer

MAX_HEIGHT = 30
YARD_COST = 1900
FOOT_YARDS = 195


def read_input(input_path: Path) -> List[WallProfile]:
    with input_path.open() as fin:
        wall_profiles = []
        for profile_id, line in enumerate(fin):
            line = line.strip()
            if not line:
                continue
            profile = WallProfile(
                id=profile_id,
                sections=[
                    WallSection(id=section_id, final_height=MAX_HEIGHT, current_height=int(section_height)) 
                    for section_id, section_height in enumerate(line.split(' '))
                ] 
            )
            wall_profiles.append(profile)
    
    return wall_profiles



typer_cli = typer.Typer()


@typer_cli.command("singlethread")
def run_single_thread(
    log_file: Path = typer.Option(
        default=Path("data/logs/log.singlethread.txt"),
        help="Execution log file output"
    ),
    test_file: Path = typer.Option(
        default=Path("data/test.txt"),
        help="Input data"
    )
):
    wall_profiles = read_input(test_file)
    logger = FileLog(log_file)

    section_queue = collections.deque([
        Task(profile_id=profile.id, section=section) for profile in wall_profiles for section in profile.sections
    ])
    
    day = 0
    for day in infinite():
        unfinish_tasks = []
        while section_queue:
            task = section_queue.popleft()
            team=Team(id=f"own", power=1)
            team.build(section=task.section)
            if not task.section.finished:
                unfinish_tasks.append(task)
            logger.add(profile_id=task.profile_id, section=task.section, team=team, day=day)
        if not len(unfinish_tasks):
            break
        section_queue = collections.deque(unfinish_tasks)


@typer_cli.command("multithread")
def run_multi_thread(
    teams: int = typer.Option(
        default=5,
        help="Number of teams (threads) to build The Wall",
    ),
    log_file: Path = typer.Option(
        default=Path("data/logs/log.multithread.txt"),
        help="Execution log file output"
    ),
    test_file: Path = typer.Option(
        default=Path("data/test.txt"),
        help="Input data"
    )
):
    wall_profiles = read_input(test_file)
    logger = FileLog(log_file)
    
    sections = [Task(profile_id=profile.id, section=section) for profile in wall_profiles for section in profile.sections]
    teams = [Team(id=str(i), power=1) for i in range(teams)]
    with TeamPool(teams=teams, loggers=[logger]) as team_pool:
        team_pool.process(tasks=sections)


if __name__ == "__main__":
    typer_cli()
