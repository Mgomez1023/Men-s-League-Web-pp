from datetime import datetime, date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models import GameStatus


class TeamBase(BaseModel):
    name: str
    slug: str


class TeamCreate(TeamBase):
    pass


class TeamResponse(TeamBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class PlayerBase(BaseModel):
    team_id: UUID
    name: str
    number: Optional[int] = None
    position: Optional[str] = None


class PlayerCreate(PlayerBase):
    pass


class PlayerUpdate(BaseModel):
    name: Optional[str] = None
    number: Optional[int] = None
    position: Optional[str] = None


class PlayerResponse(BaseModel):
    id: UUID
    team_id: UUID
    name: str
    number: Optional[int]
    position: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class GameCreate(BaseModel):
    home_team_id: UUID
    away_team_id: UUID
    start_time: datetime
    field: str
    status: GameStatus = GameStatus.SCHEDULED
    home_score: Optional[int] = None
    away_score: Optional[int] = None

    @model_validator(mode='after')
    def validate_teams(self) -> 'GameCreate':
        if self.home_team_id == self.away_team_id:
            raise ValueError('home_team_id and away_team_id must differ')
        return self


class GameUpdate(BaseModel):
    start_time: Optional[datetime] = None
    field: Optional[str] = None
    status: Optional[GameStatus] = None
    home_score: Optional[int] = Field(default=None)
    away_score: Optional[int] = Field(default=None)


class GameResponse(BaseModel):
    id: UUID
    home_team_id: UUID
    away_team_id: UUID
    start_time: datetime
    field: str
    status: GameStatus
    home_score: Optional[int]
    away_score: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class ScheduleGameResponse(GameResponse):
    home_team_name: str
    away_team_name: str


class AnnouncementCreate(BaseModel):
    title: str
    body: str


class AnnouncementResponse(BaseModel):
    id: UUID
    title: str
    body: str
    created_at: datetime
    created_by_email: str

    model_config = ConfigDict(from_attributes=True)


class TeamDetailResponse(TeamResponse):
    roster: list[PlayerResponse]


class StandingsRow(BaseModel):
    team_id: UUID
    team_name: str
    wins: int
    losses: int
    games_played: int
    runs_for: int
    runs_against: int


class ScheduleFilter(BaseModel):
    from_date: Optional[date] = None
    to_date: Optional[date] = None
