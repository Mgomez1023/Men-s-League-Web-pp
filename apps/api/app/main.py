from datetime import date, datetime, time
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_admin_email
from app.config import get_settings
from app.database import get_db
from app.models import Announcement, Game, GameStatus, Player, Team
from app.schemas import (
    AnnouncementCreate,
    AnnouncementResponse,
    GameCreate,
    GameResponse,
    GameUpdate,
    PlayerCreate,
    PlayerResponse,
    PlayerUpdate,
    ScheduleGameResponse,
    StandingsRow,
    TeamCreate,
    TeamDetailResponse,
    TeamResponse,
)
from app.services import compute_standings, get_schedule, seed_example_data

settings = get_settings()
app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.on_event('startup')
def startup_seed() -> None:
    # optional startup seed for local MVP convenience
    from app.database import SessionLocal

    db = SessionLocal()
    try:
        seed_example_data(db)
    finally:
        db.close()


@app.get('/health')
def health() -> dict[str, str]:
    return {'status': 'ok'}


@app.get('/schedule', response_model=list[ScheduleGameResponse])
def schedule(
    from_date: date | None = Query(default=None, alias='from'),
    to_date: date | None = Query(default=None, alias='to'),
    db: Session = Depends(get_db),
) -> list[ScheduleGameResponse]:
    from_dt = datetime.combine(from_date, time.min) if from_date else None
    to_dt = datetime.combine(to_date, time.max) if to_date else None

    records = get_schedule(db, from_date=from_dt, to_date=to_dt)
    return [
        ScheduleGameResponse(
            id=item['game'].id,
            home_team_id=item['game'].home_team_id,
            away_team_id=item['game'].away_team_id,
            start_time=item['game'].start_time,
            field=item['game'].field,
            status=item['game'].status,
            home_score=item['game'].home_score,
            away_score=item['game'].away_score,
            home_team_name=item['home_team_name'],
            away_team_name=item['away_team_name'],
        )
        for item in records
    ]


@app.get('/standings', response_model=list[StandingsRow])
def standings(db: Session = Depends(get_db)) -> list[StandingsRow]:
    teams = db.scalars(select(Team).order_by(Team.name.asc())).all()
    finals = db.scalars(select(Game).where(Game.status == GameStatus.FINAL)).all()
    return compute_standings(teams, finals)


@app.get('/teams', response_model=list[TeamResponse])
def teams(db: Session = Depends(get_db)) -> list[Team]:
    return db.scalars(select(Team).order_by(Team.name.asc())).all()


@app.get('/teams/{team_id}', response_model=TeamDetailResponse)
def team_detail(team_id: UUID, db: Session = Depends(get_db)) -> TeamDetailResponse:
    team = db.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail='Team not found')

    roster = db.scalars(select(Player).where(Player.team_id == team_id).order_by(Player.name.asc())).all()
    return TeamDetailResponse(id=team.id, name=team.name, slug=team.slug, roster=[PlayerResponse.model_validate(p) for p in roster])


@app.get('/announcements', response_model=list[AnnouncementResponse])
def announcements(db: Session = Depends(get_db)) -> list[Announcement]:
    return db.scalars(select(Announcement).order_by(Announcement.created_at.desc())).all()


@app.post('/admin/games', response_model=GameResponse)
def create_game(
    payload: GameCreate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin_email),
) -> Game:
    game = Game(**payload.model_dump())
    db.add(game)
    db.commit()
    db.refresh(game)
    return game


@app.patch('/admin/games/{game_id}', response_model=GameResponse)
def update_game(
    game_id: UUID,
    payload: GameUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin_email),
) -> Game:
    game = db.get(Game, game_id)
    if not game:
        raise HTTPException(status_code=404, detail='Game not found')

    updates = payload.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(game, key, value)

    if game.status == GameStatus.FINAL and (game.home_score is None or game.away_score is None):
        raise HTTPException(status_code=400, detail='Final games require home_score and away_score')

    db.commit()
    db.refresh(game)
    return game


@app.post('/admin/announcements', response_model=AnnouncementResponse)
def create_announcement(
    payload: AnnouncementCreate,
    db: Session = Depends(get_db),
    admin_email: str = Depends(get_current_admin_email),
) -> Announcement:
    item = Announcement(**payload.model_dump(), created_by_email=admin_email)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.post('/admin/teams', response_model=TeamResponse)
def create_team(
    payload: TeamCreate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin_email),
) -> Team:
    team = Team(**payload.model_dump())
    db.add(team)
    db.commit()
    db.refresh(team)
    return team


@app.post('/admin/players', response_model=PlayerResponse)
def create_player(
    payload: PlayerCreate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin_email),
) -> Player:
    player = Player(**payload.model_dump())
    db.add(player)
    db.commit()
    db.refresh(player)
    return player


@app.patch('/admin/players/{player_id}', response_model=PlayerResponse)
def update_player(
    player_id: UUID,
    payload: PlayerUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin_email),
) -> Player:
    player = db.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail='Player not found')

    updates = payload.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(player, key, value)

    db.commit()
    db.refresh(player)
    return player
