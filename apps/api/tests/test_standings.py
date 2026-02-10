from datetime import datetime, timezone
from uuid import uuid4

from app.models import Game, GameStatus, Team
from app.services import compute_standings


def make_team(name: str) -> Team:
    return Team(id=uuid4(), name=name, slug=name.lower())


def test_compute_standings_from_final_games() -> None:
    tigers = make_team('Tigers')
    bears = make_team('Bears')

    final_game = Game(
        home_team_id=tigers.id,
        away_team_id=bears.id,
        start_time=datetime.now(tz=timezone.utc),
        field='Field A',
        status=GameStatus.FINAL,
        home_score=5,
        away_score=2,
    )

    standings = compute_standings([tigers, bears], [final_game])

    assert standings[0].team_name == 'Tigers'
    assert standings[0].wins == 1
    assert standings[0].losses == 0
    assert standings[1].team_name == 'Bears'
    assert standings[1].wins == 0
    assert standings[1].losses == 1
