"""Model class definitions."""

from dataclasses import dataclass
from datetime import timedelta, datetime
from typing import Any, TypedDict
from mgz.fast import Action as ActionEnum
from mgz.fast import Age as AgeEnum
from mgz.fast.actions import ActionPayload
from mgz.util import Version


class EnrichedActionPayload(ActionPayload, total=False):
    """Action payload after model-layer enrichment (see enrich_action).

    Extends the raw parser payload with name lookups for id keys; each is
    None when the id is missing from the dataset/consts tables. enrich_action
    also deletes `x`/`y` (promoted to Action.position) and parse_match
    deletes `player_id` (promoted to Action.player).
    """

    technology: str | None
    formation: str | None
    stance: str | None
    building: str | None
    unit: str | None
    command: str | None
    order: str | None
    resource: str | None


class ChatInputPayload(TypedDict):
    """Payload of a Chat-type Input."""

    message: str


@dataclass
class Position:
    """Represents a coordinate."""

    x: float
    y: float

    def hash(self):
        return hash((self.x, self.y))


@dataclass
class Object:
    """Represents an object."""

    name: str
    class_id: int
    object_id: int
    instance_id: int
    index: int
    position: Position


class StartingResources(TypedDict):
    """Starting resource stockpile, read from the recorded game header."""

    food: int
    wood: int
    stone: int
    gold: int


@dataclass
class TimeseriesRow:
    """Represents a timeseries row."""

    timestamp: timedelta
    total_resources: int
    total_objects: int


@dataclass
class Player:
    """Represents a player."""

    number: int
    name: str
    color: str
    color_id: int
    civilization: str
    civilization_id: int
    position: Position
    objects: list
    profile_id: int
    timeseries: list[TimeseriesRow]
    prefer_random: bool = None  # type: ignore
    handicap: int = 100
    team: list = None  # type: ignore
    team_id: int = None  # type: ignore
    winner: bool = False
    eapm: int = None  # type: ignore
    rate_snapshot: int = None  # type: ignore
    starting_resources: StartingResources | None = None

    def __repr__(self):
        return self.name

    def __hash__(self):
        return self.number


@dataclass
class Action:
    """Represents an abstract action."""

    timestamp: timedelta
    type: ActionEnum
    payload: EnrichedActionPayload
    player: Player = None  # type: ignore
    position: Position = None  # type: ignore


@dataclass
class Input:
    """Represents a player input."""

    timestamp: timedelta
    type: str
    param: str
    payload: EnrichedActionPayload | ChatInputPayload
    player: Player = None  # type: ignore
    position: Position = None  # type: ignore


@dataclass
class Viewlock:
    """Represents player view."""

    timestamp: timedelta
    position: Position
    player: Player


@dataclass
class Tile:
    """Represents a map tile."""

    terrain: int
    elevation: int
    position: Position


@dataclass
class Map:
    """Represents a map."""

    id: int
    name: str
    dimension: int
    size: str
    custom: bool
    seed: int
    mod_id: int
    zr: bool
    modes: dict
    tiles: list

    def __repr__(self):
        return self.name

@dataclass
class File:
    """Represents the recorded game file."""

    encoding: str
    language: str
    hash: str
    size: int
    device_type: int
    perspective: Player
    viewlocks: list


@dataclass
class Chat:
    """Represents a chat message."""

    timestamp: timedelta
    message: str
    origination: str
    audience: str
    player: Player

    def __repr__(self):
        return f'[{self.timestamp}] {self.player}: {self.message}'

@dataclass
class Uptime:
    """Represents an advanced to age event."""

    timestamp: timedelta
    age: AgeEnum
    player: Player

    def __repr__(self):
        return f'[{self.timestamp}] {self.player} -> {self.age}'


@dataclass
class Match:
    """Represents a match.

    Fields typed `| None` are unavailable for some game versions — most are
    DE-only (guid, lobby, rated, build_version, timestamp, spec_delay,
    allow_specs, hidden_civs, private, hash, team_together, lock_speed,
    all_technologies, multiqueue, starting_age).
    """

    players: list[Player]
    teams: list[list[Player]]
    gaia: list[Object]
    map: Map
    file: File
    restored: bool
    restored_at: timedelta
    speed: str
    speed_id: int
    cheats: bool
    lock_teams: bool
    population: int
    chat: list[Chat]
    guid: str | None
    lobby: str | None
    rated: bool | None
    dataset: str
    type: str
    type_id: int
    map_reveal: str
    map_reveal_id: int
    difficulty: str | None
    difficulty_id: int
    starting_age: str | None
    starting_age_id: int | None
    team_together: bool | None
    lock_speed: bool | None
    all_technologies: bool | None
    multiqueue: bool | None
    duration: timedelta
    diplomacy_type: str
    completed: bool
    dataset_id: int
    version: Version
    game_version: str
    save_version: float
    log_version: int | None
    build_version: int | None
    timestamp: datetime | None
    spec_delay: timedelta | None
    allow_specs: bool | None
    hidden_civs: bool | None
    private: bool | None
    hash: Any  # _hashlib.HASH for DE recs (serialize() calls .hexdigest()), else None
    actions: list[Action]
    inputs: list[Input]
    uptimes: list[Uptime]
