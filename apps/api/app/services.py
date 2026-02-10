from collections import defaultdict
from datetime import datetime
from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.models import Announcement, Game, GameStatus, Player, Team
from app.schemas import StandingsRow


@dataclass
class TeamStandingAccumulator:
    wins: int = 0
    losses: int = 0
    runs_for: int = 0
    runs_against: int = 0


def compute_standings(teams: list[Team], final_games: list[Game]) -> list[StandingsRow]:
    rows: dict[UUID, TeamStandingAccumulator] = defaultdict(TeamStandingAccumulator)

    for game in final_games:
        if game.home_score is None or game.away_score is None:
            continue

        home = rows[game.home_team_id]
        away = rows[game.away_team_id]

        home.runs_for += game.home_score
        home.runs_against += game.away_score
        away.runs_for += game.away_score
        away.runs_against += game.home_score

        if game.home_score > game.away_score:
            home.wins += 1
            away.losses += 1
        else:
            away.wins += 1
            home.losses += 1

    team_name_by_id = {team.id: team.name for team in teams}
    output: list[StandingsRow] = []
    for team in teams:
        acc = rows[team.id]
        output.append(
            StandingsRow(
                team_id=team.id,
                team_name=team.name,
                wins=acc.wins,
                losses=acc.losses,
                games_played=acc.wins + acc.losses,
                runs_for=acc.runs_for,
                runs_against=acc.runs_against,
            )
        )

    output.sort(key=lambda row: (-row.wins, row.losses, team_name_by_id[row.team_id]))
    return output


def get_schedule(db: Session, from_date=None, to_date=None) -> list[dict]:
    home = Team.__table__.alias('home')
    away = Team.__table__.alias('away')

    query = (
        select(
            Game,
            home.c.name.label('home_team_name'),
            away.c.name.label('away_team_name'),
        )
        .join(home, Game.home_team_id == home.c.id)
        .join(away, Game.away_team_id == away.c.id)
        .order_by(Game.start_time.asc())
    )

    filters = []
    if from_date:
        filters.append(Game.start_time >= from_date)
    if to_date:
        filters.append(Game.start_time <= to_date)
    if filters:
        query = query.where(and_(*filters))

    records = db.execute(query).all()
    return [
        {
            'game': row.Game,
            'home_team_name': row.home_team_name,
            'away_team_name': row.away_team_name,
        }
        for row in records
    ]


def seed_example_data(db: Session) -> None:
    if db.scalar(select(Team.id).limit(1)):
        return

    tigers = Team(name='Tigers', slug='tigers')
    bears = Team(name='Bears', slug='bears')
    eagles = Team(name='Eagles', slug='eagles')
    db.add_all([tigers, bears, eagles])
    db.flush()

    db.add_all(
        [
            Player(team_id=tigers.id, name='Alex Carter', number=12, position='P'),
            Player(team_id=tigers.id, name='Sam Reed', number=7, position='CF'),
            Player(team_id=bears.id, name='Luis Gomez', number=22, position='1B'),
            Player(team_id=eagles.id, name='Chris Park', number=4, position='SS'),
        ]
    )

    db.add_all(
        [
            Game(home_team_id=tigers.id, away_team_id=bears.id, start_time=datetime.fromisoformat('2026-04-10T18:00:00+00:00'), field='Field A'),
            Game(
                home_team_id=bears.id,
                away_team_id=eagles.id,
                start_time=datetime.fromisoformat('2026-04-17T18:00:00+00:00'),
                field='Field B',
                status=GameStatus.FINAL,
                home_score=3,
                away_score=6,
            ),
        ]
    )

    db.add(Announcement(title='Season Kickoff', body='Opening day is April 10!', created_by_email='admin@example.com'))
    db.commit()
