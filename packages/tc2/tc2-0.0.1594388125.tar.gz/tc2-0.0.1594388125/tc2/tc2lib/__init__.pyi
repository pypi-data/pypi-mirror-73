"""
      tc2lib documentation
  """
from . import Constants
from typing import *
from typing import Iterable as iterable
from typing import Iterator as iterator
from numpy import float64, float32, int32, uint8
import numpy
_Shape = Tuple[int, ...]
__all__  = [
"Action",
"Bullet",
"Client",
"Frame",
"GameMultiPlayer",
"GameOptions",
"GamePlayerOptions",
"GameSinglePlayer",
"GameType",
"Order",
"Replayer",
"Resources",
"State",
"Unit",
"UnitCommand",
"UnitFeatureData",
"featurize_buildability",
"featurize_creep",
"featurize_fog",
"featurize_ground_height",
"featurize_ground_height_onehot",
"featurize_map_dynamic",
"featurize_map_static",
"featurize_resources",
"featurize_start_locations",
"featurize_structures",
"featurize_tall_doodad",
"featurize_units",
"featurize_walkability",
"featurize_xygrid",
"set_paths",
"Constants",
"Melee",
"UseMapSettings",
"__version__"
]
class Action():
    def __init__(self) -> None: ...
    @property
    def action(self) -> List[int]:
        """
        :type: List[int]
        """
    @action.setter
    def action(self, arg0: List[int]) -> None:
        pass
    @property
    def aid(self) -> int:
        """
        :type: int
        """
    @aid.setter
    def aid(self, arg0: int) -> None:
        pass
    @property
    def uid(self) -> int:
        """
        :type: int
        """
    @uid.setter
    def uid(self, arg0: int) -> None:
        pass
    pass
class Bullet():
    def __init__(self) -> None: ...
    @property
    def type(self) -> int:
        """
        :type: int
        """
    @type.setter
    def type(self, arg0: int) -> None:
        pass
    @property
    def x(self) -> int:
        """
        :type: int
        """
    @x.setter
    def x(self, arg0: int) -> None:
        pass
    @property
    def y(self) -> int:
        """
        :type: int
        """
    @y.setter
    def y(self, arg0: int) -> None:
        pass
    pass
class Client():
    def __init__(self) -> None: ...
    def close(self) -> bool: ...
    @overload
    def connect(self, file_socket: str, timeout: int = -1) -> bool: ...
    @overload
    def connect(self, hostname: str, port: int = 11111, timeout: int = -1) -> bool: ...
    def connected(self) -> bool: ...
    def error(self) -> str: ...
    def init(self, window_size: Tuple[int, int] = (-1, -1), window_pos: Tuple[int, int] = (-1, -1), micro_battles: bool = False) -> object:
        """
        init(self: tc2lib.Client, window_size: Tuple[int, int] = (-1, -1), window_pos: Tuple[int, int] = (-1, -1), micro_battles: bool = False) -> object
        """
    def poll(self, arg0: int) -> bool: ...
    def recv(self) -> State: ...
    def send(self, arg0: List[List[object]]) -> bool: ...
    def state(self) -> State: ...
    pass
class Frame():
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, arg0: Frame) -> None: ...
    def combine(self, arg0: Frame) -> None: ...
    def creep_map(self) -> numpy.ndarray[uint8]: ...
    def deepEq(self, other: Frame, debug: bool = False) -> bool: ...
    def filter(self, arg0: int, arg1: int, arg2: Frame) -> None: ...
    def get_creep_at(self, arg0: int, arg1: int) -> bool: ...
    @property
    def actions(self) -> Dict[int, List[Action]]:
        """
        :type: Dict[int, List[Action]]
        """
    @actions.setter
    def actions(self, arg0: Dict[int, List[Action]]) -> None:
        pass
    @property
    def bullets(self) -> List[Bullet]:
        """
        :type: List[Bullet]
        """
    @bullets.setter
    def bullets(self, arg0: List[Bullet]) -> None:
        pass
    @property
    def height(self) -> int:
        """
        :type: int
        """
    @height.setter
    def height(self, arg0: int) -> None:
        pass
    @property
    def is_terminal(self) -> int:
        """
        :type: int
        """
    @is_terminal.setter
    def is_terminal(self, arg0: int) -> None:
        pass
    @property
    def resources(self) -> Dict[int, Resources]:
        """
        :type: Dict[int, Resources]
        """
    @resources.setter
    def resources(self, arg0: Dict[int, Resources]) -> None:
        pass
    @property
    def reward(self) -> int:
        """
        :type: int
        """
    @reward.setter
    def reward(self, arg0: int) -> None:
        pass
    @property
    def units(self) -> Dict[int, List[Unit]]:
        """
        :type: Dict[int, List[Unit]]
        """
    @units.setter
    def units(self, arg0: Dict[int, List[Unit]]) -> None:
        pass
    @property
    def width(self) -> int:
        """
        :type: int
        """
    @width.setter
    def width(self, arg0: int) -> None:
        pass
    pass
class GameMultiPlayer():
    def __init__(self, arg0: GameOptions, arg1: GamePlayerOptions, arg2: GamePlayerOptions) -> None: ...
    def make_client0(self) -> Client: ...
    def make_client1(self) -> Client: ...
    pass
class GameOptions():
    def __init__(self) -> None: ...
    def get_gametype(self) -> GameType: ...
    def get_gui(self) -> bool: ...
    def get_map(self) -> str: ...
    def get_replaypath(self) -> str: ...
    def set_gametype(self, arg0: GameType) -> GameOptions: ...
    def set_gui(self, arg0: bool) -> GameOptions: ...
    def set_map(self, arg0: str) -> GameOptions: ...
    def set_replaypath(self, arg0: str) -> GameOptions: ...
    @property
    def gametype(self) -> GameType:
        """
        :type: GameType
        """
    @gametype.setter
    def gametype(self, arg0: GameType) -> None:
        pass
    @property
    def gui(self) -> bool:
        """
        :type: bool
        """
    @gui.setter
    def gui(self, arg0: bool) -> None:
        pass
    @property
    def map(self) -> str:
        """
        :type: str
        """
    @map.setter
    def map(self, arg0: str) -> None:
        pass
    @property
    def replaypath(self) -> str:
        """
        :type: str
        """
    @replaypath.setter
    def replaypath(self, arg0: str) -> None:
        pass
    pass
class GamePlayerOptions():
    def __init__(self) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @name.setter
    def name(self, arg0: str) -> None:
        pass
    @property
    def race(self) -> str:
        """
        :type: str
        """
    @race.setter
    def race(self, arg0: str) -> None:
        pass
    pass
class GameSinglePlayer():
    def __init__(self, arg0: GameOptions, arg1: GamePlayerOptions, arg2: GamePlayerOptions) -> None: ...
    def make_client0(self) -> Client: ...
    pass
class GameType():
    """
    Members:

      Melee

      UseMapSettings
    """
    def __init__(self, arg0: int) -> None: ...
    def __int__(self) -> int: ...
    @property
    def name(self) -> str:
        """
        (self: handle) -> str

        :type: str
        """
    Melee: GameType # value = GameType.Melee
    UseMapSettings: GameType # value = GameType.UseMapSettings
    __entries: dict # value = {'Melee': (GameType.Melee, None), 'UseMapSettings': (GameType.UseMapSettings, None)}
    __members__: dict # value = {'Melee': GameType.Melee, 'UseMapSettings': GameType.UseMapSettings}
    pass
class Order():
    def __eq__(self, other) -> bool: ...
    def __init__(self) -> None: ...
    @property
    def first_frame(self) -> int:
        """
        :type: int
        """
    @first_frame.setter
    def first_frame(self, arg0: int) -> None:
        pass
    @property
    def targetId(self) -> int:
        """
        :type: int
        """
    @targetId.setter
    def targetId(self, arg0: int) -> None:
        pass
    @property
    def targetX(self) -> int:
        """
        :type: int
        """
    @targetX.setter
    def targetX(self, arg0: int) -> None:
        pass
    @property
    def targetY(self) -> int:
        """
        :type: int
        """
    @targetY.setter
    def targetY(self, arg0: int) -> None:
        pass
    @property
    def type(self) -> int:
        """
        :type: int
        """
    @type.setter
    def type(self, arg0: int) -> None:
        pass
    pass
class Replayer():
    def __init__(self) -> None: ...
    def __len__(self) -> int: ...
    def getFrame(self, arg0: int) -> Frame: ...
    def getKeyFrame(self) -> int: ...
    def getMap(self) -> dict: ...
    def getNumUnits(self, arg0: int) -> int: ...
    def load(self, path: str) -> None: ...
    def push(self, arg0: Frame) -> None: ...
    def save(self, path: str, compressed: bool = True) -> None: ...
    def setKeyFrame(self, arg0: int) -> None: ...
    def setMap(self, arg0: dict) -> None: ...
    def setMapFromState(self, arg0) -> None: ...
    def setNumUnits(self) -> None: ...
    pass
class Resources():
    def __init__(self) -> None: ...
    @property
    def gas(self) -> int:
        """
        :type: int
        """
    @gas.setter
    def gas(self, arg0: int) -> None:
        pass
    @property
    def ore(self) -> int:
        """
        :type: int
        """
    @ore.setter
    def ore(self, arg0: int) -> None:
        pass
    @property
    def techs(self) -> int:
        """
        :type: int
        """
    @techs.setter
    def techs(self, arg0: int) -> None:
        pass
    @property
    def total_psi(self) -> int:
        """
        :type: int
        """
    @total_psi.setter
    def total_psi(self, arg0: int) -> None:
        pass
    @property
    def upgrades(self) -> int:
        """
        :type: int
        """
    @upgrades.setter
    def upgrades(self, arg0: int) -> None:
        pass
    @property
    def upgrades_level(self) -> int:
        """
        :type: int
        """
    @upgrades_level.setter
    def upgrades_level(self, arg0: int) -> None:
        pass
    @property
    def used_psi(self) -> int:
        """
        :type: int
        """
    @used_psi.setter
    def used_psi(self, arg0: int) -> None:
        pass
    pass
class State():
    class PlayerInfo():
        def __init__(self) -> None: ...
        def __repr__(self) -> str: ...
        @property
        def has_left(self) -> bool:
            """
            :type: bool
            """
        @has_left.setter
        def has_left(self, arg0: bool) -> None:
            pass
        @property
        def id(self) -> int:
            """
            :type: int
            """
        @id.setter
        def id(self, arg0: int) -> None:
            pass
        @property
        def is_enemy(self) -> bool:
            """
            :type: bool
            """
        @is_enemy.setter
        def is_enemy(self, arg0: bool) -> None:
            pass
        @property
        def name(self) -> str:
            """
            :type: str
            """
        @name.setter
        def name(self, arg0: str) -> None:
            pass
        @property
        def race(self) -> int:
            """
            :type: int
            """
        @race.setter
        def race(self, arg1: int) -> None:
            pass
        pass
    class Position():
        @overload
        def __init__(self, arg0: int, arg1: int) -> None: ...
        @overload
        def __init__(self) -> None: ...
        @property
        def x(self) -> int:
            """
            :type: int
            """
        @x.setter
        def x(self, arg0: int) -> None:
            pass
        @property
        def y(self) -> int:
            """
            :type: int
            """
        @y.setter
        def y(self, arg0: int) -> None:
            pass
        pass
    def __init__(self) -> None: ...
    def clone(self) -> State: ...
    def reset(self) -> None: ...
    @property
    def all_units(self) -> List[Unit]:
        """
        :type: List[Unit]
        """
    @all_units.setter
    def all_units(self, arg0: List[Unit]) -> None:
        pass
    @property
    def buildable_data(self) -> List[int]:
        """
        :type: List[int]
        """
    @buildable_data.setter
    def buildable_data(self, arg0: List[int]) -> None:
        pass
    @property
    def deaths(self) -> List[int]:
        """
        :type: List[int]
        """
    @deaths.setter
    def deaths(self, arg0: List[int]) -> None:
        pass
    @property
    def frame(self) -> Frame:
        """
        :type: Frame
        """
    @property
    def frame_from_bwapi(self) -> int:
        """
        :type: int
        """
    @frame_from_bwapi.setter
    def frame_from_bwapi(self, arg0: int) -> None:
        pass
    @property
    def game_ended(self) -> bool:
        """
        :type: bool
        """
    @game_ended.setter
    def game_ended(self, arg0: bool) -> None:
        pass
    @property
    def game_won(self) -> bool:
        """
        :type: bool
        """
    @game_won.setter
    def game_won(self, arg0: bool) -> None:
        pass
    @property
    def ground_height_data(self) -> List[int]:
        """
        :type: List[int]
        """
    @ground_height_data.setter
    def ground_height_data(self, arg0: List[int]) -> None:
        pass
    @property
    def image(self) -> List[int]:
        """
        :type: List[int]
        """
    @image.setter
    def image(self, arg0: List[int]) -> None:
        pass
    @property
    def image_size(self) -> tuple:
        """
        :type: tuple
        """
    @image_size.setter
    def image_size(self, arg1: Tuple[int, int]) -> None:
        pass
    @property
    def img_mode(self) -> str:
        """
        :type: str
        """
    @img_mode.setter
    def img_mode(self, arg0: str) -> None:
        pass
    @property
    def lag_frames(self) -> int:
        """
        :type: int
        """
    @lag_frames.setter
    def lag_frames(self, arg0: int) -> None:
        pass
    @property
    def map_name(self) -> str:
        """
        :type: str
        """
    @map_name.setter
    def map_name(self, arg0: str) -> None:
        pass
    @property
    def map_size(self) -> tuple:
        """
        :type: tuple
        """
    @property
    def map_title(self) -> str:
        """
        :type: str
        """
    @map_title.setter
    def map_title(self, arg0: str) -> None:
        pass
    @property
    def neutral_id(self) -> int:
        """
        :type: int
        """
    @neutral_id.setter
    def neutral_id(self, arg0: int) -> None:
        pass
    @property
    def player_id(self) -> int:
        """
        :type: int
        """
    @player_id.setter
    def player_id(self, arg0: int) -> None:
        pass
    @property
    def player_info(self) -> Dict[int, State.PlayerInfo]:
        """
        :type: Dict[int, State.PlayerInfo]
        """
    @player_info.setter
    def player_info(self, arg0: Dict[int, State.PlayerInfo]) -> None:
        pass
    @property
    def replay(self) -> bool:
        """
        :type: bool
        """
    @replay.setter
    def replay(self, arg0: bool) -> None:
        pass
    @property
    def screen_position(self) -> tuple:
        """
        :type: tuple
        """
    @screen_position.setter
    def screen_position(self, arg1: Tuple[int, int]) -> None:
        pass
    @property
    def start_locations(self) -> List[State.Position]:
        """
        :type: List[State.Position]
        """
    @start_locations.setter
    def start_locations(self, arg0: List[State.Position]) -> None:
        pass
    @property
    def units(self) -> Dict[int, List[Unit]]:
        """
        :type: Dict[int, List[Unit]]
        """
    @units.setter
    def units(self, arg0: Dict[int, List[Unit]]) -> None:
        pass
    @property
    def visibility(self) -> List[int]:
        """
        :type: List[int]
        """
    @visibility.setter
    def visibility(self, arg0: List[int]) -> None:
        pass
    @property
    def visibility_size(self) -> tuple:
        """
        :type: tuple
        """
    @visibility_size.setter
    def visibility_size(self, arg1: Tuple[int, int]) -> None:
        pass
    @property
    def walkable_data(self) -> List[int]:
        """
        :type: List[int]
        """
    @walkable_data.setter
    def walkable_data(self, arg0: List[int]) -> None:
        pass
    pass
class Unit():
    def __init__(self) -> None: ...
    def __repr__(self) -> str: ...
    def getFlag(self, arg0) -> bool: ...
    def setFlag(self, arg0, arg1: bool) -> None: ...
    @property
    def accelerating(self) -> bool:
        """
        :type: bool
        """
    @accelerating.setter
    def accelerating(self, arg1: bool) -> None:
        pass
    @property
    def airATK(self) -> int:
        """
        :type: int
        """
    @airATK.setter
    def airATK(self, arg0: int) -> None:
        pass
    @property
    def airCD(self) -> int:
        """
        :type: int
        """
    @airCD.setter
    def airCD(self, arg0: int) -> None:
        pass
    @property
    def airDmgType(self) -> int:
        """
        :type: int
        """
    @airDmgType.setter
    def airDmgType(self, arg0: int) -> None:
        pass
    @property
    def airRange(self) -> int:
        """
        :type: int
        """
    @airRange.setter
    def airRange(self, arg0: int) -> None:
        pass
    @property
    def armor(self) -> int:
        """
        :type: int
        """
    @armor.setter
    def armor(self, arg0: int) -> None:
        pass
    @property
    def attack_frame(self) -> bool:
        """
        :type: bool
        """
    @attack_frame.setter
    def attack_frame(self, arg1: bool) -> None:
        pass
    @property
    def attacking(self) -> bool:
        """
        :type: bool
        """
    @attacking.setter
    def attacking(self, arg1: bool) -> None:
        pass
    @property
    def being_constructed(self) -> bool:
        """
        :type: bool
        """
    @being_constructed.setter
    def being_constructed(self, arg1: bool) -> None:
        pass
    @property
    def being_gathered(self) -> bool:
        """
        :type: bool
        """
    @being_gathered.setter
    def being_gathered(self, arg1: bool) -> None:
        pass
    @property
    def being_healed(self) -> bool:
        """
        :type: bool
        """
    @being_healed.setter
    def being_healed(self, arg1: bool) -> None:
        pass
    @property
    def blind(self) -> bool:
        """
        :type: bool
        """
    @blind.setter
    def blind(self, arg1: bool) -> None:
        pass
    @property
    def braking(self) -> bool:
        """
        :type: bool
        """
    @braking.setter
    def braking(self, arg1: bool) -> None:
        pass
    @property
    def burrowed(self) -> bool:
        """
        :type: bool
        """
    @burrowed.setter
    def burrowed(self, arg1: bool) -> None:
        pass
    @property
    def carrying_gas(self) -> bool:
        """
        :type: bool
        """
    @carrying_gas.setter
    def carrying_gas(self, arg1: bool) -> None:
        pass
    @property
    def carrying_minerals(self) -> bool:
        """
        :type: bool
        """
    @carrying_minerals.setter
    def carrying_minerals(self, arg1: bool) -> None:
        pass
    @property
    def cloaked(self) -> bool:
        """
        :type: bool
        """
    @cloaked.setter
    def cloaked(self, arg1: bool) -> None:
        pass
    @property
    def command(self) -> UnitCommand:
        """
        :type: UnitCommand
        """
    @command.setter
    def command(self, arg0: UnitCommand) -> None:
        pass
    @property
    def completed(self) -> bool:
        """
        :type: bool
        """
    @completed.setter
    def completed(self, arg1: bool) -> None:
        pass
    @property
    def constructing(self) -> bool:
        """
        :type: bool
        """
    @constructing.setter
    def constructing(self, arg1: bool) -> None:
        pass
    @property
    def defense_matrixed(self) -> bool:
        """
        :type: bool
        """
    @defense_matrixed.setter
    def defense_matrixed(self, arg1: bool) -> None:
        pass
    @property
    def detected(self) -> bool:
        """
        :type: bool
        """
    @detected.setter
    def detected(self, arg1: bool) -> None:
        pass
    @property
    def energy(self) -> int:
        """
        :type: int
        """
    @energy.setter
    def energy(self, arg0: int) -> None:
        pass
    @property
    def ensnared(self) -> bool:
        """
        :type: bool
        """
    @ensnared.setter
    def ensnared(self, arg1: bool) -> None:
        pass
    @property
    def flags(self) -> int:
        """
        :type: int
        """
    @flags.setter
    def flags(self, arg0: int) -> None:
        pass
    @property
    def flying(self) -> bool:
        """
        :type: bool
        """
    @flying.setter
    def flying(self, arg1: bool) -> None:
        pass
    @property
    def following(self) -> bool:
        """
        :type: bool
        """
    @following.setter
    def following(self, arg1: bool) -> None:
        pass
    @property
    def gathering_gas(self) -> bool:
        """
        :type: bool
        """
    @gathering_gas.setter
    def gathering_gas(self, arg1: bool) -> None:
        pass
    @property
    def gathering_minerals(self) -> bool:
        """
        :type: bool
        """
    @gathering_minerals.setter
    def gathering_minerals(self, arg1: bool) -> None:
        pass
    @property
    def groundATK(self) -> int:
        """
        :type: int
        """
    @groundATK.setter
    def groundATK(self, arg0: int) -> None:
        pass
    @property
    def groundCD(self) -> int:
        """
        :type: int
        """
    @groundCD.setter
    def groundCD(self, arg0: int) -> None:
        pass
    @property
    def groundDmgType(self) -> int:
        """
        :type: int
        """
    @groundDmgType.setter
    def groundDmgType(self, arg0: int) -> None:
        pass
    @property
    def groundRange(self) -> int:
        """
        :type: int
        """
    @groundRange.setter
    def groundRange(self, arg0: int) -> None:
        pass
    @property
    def hallucination(self) -> bool:
        """
        :type: bool
        """
    @hallucination.setter
    def hallucination(self, arg1: bool) -> None:
        pass
    @property
    def health(self) -> int:
        """
        :type: int
        """
    @health.setter
    def health(self, arg0: int) -> None:
        pass
    @property
    def holding_position(self) -> bool:
        """
        :type: bool
        """
    @holding_position.setter
    def holding_position(self, arg1: bool) -> None:
        pass
    @property
    def id(self) -> int:
        """
        :type: int
        """
    @id.setter
    def id(self, arg0: int) -> None:
        pass
    @property
    def idle(self) -> bool:
        """
        :type: bool
        """
    @idle.setter
    def idle(self, arg1: bool) -> None:
        pass
    @property
    def interruptible(self) -> bool:
        """
        :type: bool
        """
    @interruptible.setter
    def interruptible(self, arg1: bool) -> None:
        pass
    @property
    def invincible(self) -> bool:
        """
        :type: bool
        """
    @invincible.setter
    def invincible(self, arg1: bool) -> None:
        pass
    @property
    def irradiated(self) -> bool:
        """
        :type: bool
        """
    @irradiated.setter
    def irradiated(self, arg1: bool) -> None:
        pass
    @property
    def lifted(self) -> bool:
        """
        :type: bool
        """
    @lifted.setter
    def lifted(self, arg1: bool) -> None:
        pass
    @property
    def loaded(self) -> bool:
        """
        :type: bool
        """
    @loaded.setter
    def loaded(self, arg1: bool) -> None:
        pass
    @property
    def locked_down(self) -> bool:
        """
        :type: bool
        """
    @locked_down.setter
    def locked_down(self, arg1: bool) -> None:
        pass
    @property
    def maelstrommed(self) -> bool:
        """
        :type: bool
        """
    @maelstrommed.setter
    def maelstrommed(self, arg1: bool) -> None:
        pass
    @property
    def maxCD(self) -> int:
        """
        :type: int
        """
    @maxCD.setter
    def maxCD(self, arg0: int) -> None:
        pass
    @property
    def max_health(self) -> int:
        """
        :type: int
        """
    @max_health.setter
    def max_health(self, arg0: int) -> None:
        pass
    @property
    def max_shield(self) -> int:
        """
        :type: int
        """
    @max_shield.setter
    def max_shield(self, arg0: int) -> None:
        pass
    @property
    def morphing(self) -> bool:
        """
        :type: bool
        """
    @morphing.setter
    def morphing(self, arg1: bool) -> None:
        pass
    @property
    def moving(self) -> bool:
        """
        :type: bool
        """
    @moving.setter
    def moving(self, arg1: bool) -> None:
        pass
    @property
    def orders(self) -> List[Order]:
        """
        :type: List[Order]
        """
    @orders.setter
    def orders(self, arg0: List[Order]) -> None:
        pass
    @property
    def parasited(self) -> bool:
        """
        :type: bool
        """
    @parasited.setter
    def parasited(self, arg1: bool) -> None:
        pass
    @property
    def patrolling(self) -> bool:
        """
        :type: bool
        """
    @patrolling.setter
    def patrolling(self, arg1: bool) -> None:
        pass
    @property
    def pixel_size_x(self) -> int:
        """
        :type: int
        """
    @pixel_size_x.setter
    def pixel_size_x(self, arg0: int) -> None:
        pass
    @property
    def pixel_size_y(self) -> int:
        """
        :type: int
        """
    @pixel_size_y.setter
    def pixel_size_y(self, arg0: int) -> None:
        pass
    @property
    def pixel_x(self) -> int:
        """
        :type: int
        """
    @pixel_x.setter
    def pixel_x(self, arg0: int) -> None:
        pass
    @property
    def pixel_y(self) -> int:
        """
        :type: int
        """
    @pixel_y.setter
    def pixel_y(self, arg0: int) -> None:
        pass
    @property
    def plagued(self) -> bool:
        """
        :type: bool
        """
    @plagued.setter
    def plagued(self, arg1: bool) -> None:
        pass
    @property
    def playerId(self) -> int:
        """
        :type: int
        """
    @playerId.setter
    def playerId(self, arg0: int) -> None:
        pass
    @property
    def powered(self) -> bool:
        """
        :type: bool
        """
    @powered.setter
    def powered(self, arg1: bool) -> None:
        pass
    @property
    def repairing(self) -> bool:
        """
        :type: bool
        """
    @repairing.setter
    def repairing(self, arg1: bool) -> None:
        pass
    @property
    def researching(self) -> bool:
        """
        :type: bool
        """
    @researching.setter
    def researching(self, arg1: bool) -> None:
        pass
    @property
    def resources(self) -> int:
        """
        :type: int
        """
    @resources.setter
    def resources(self, arg0: int) -> None:
        pass
    @property
    def selected(self) -> bool:
        """
        :type: bool
        """
    @selected.setter
    def selected(self, arg1: bool) -> None:
        pass
    @property
    def shield(self) -> int:
        """
        :type: int
        """
    @shield.setter
    def shield(self, arg0: int) -> None:
        pass
    @property
    def shieldArmor(self) -> int:
        """
        :type: int
        """
    @shieldArmor.setter
    def shieldArmor(self, arg0: int) -> None:
        pass
    @property
    def sieged(self) -> bool:
        """
        :type: bool
        """
    @sieged.setter
    def sieged(self, arg1: bool) -> None:
        pass
    @property
    def size(self) -> int:
        """
        :type: int
        """
    @size.setter
    def size(self, arg0: int) -> None:
        pass
    @property
    def starting_attack(self) -> bool:
        """
        :type: bool
        """
    @starting_attack.setter
    def starting_attack(self, arg1: bool) -> None:
        pass
    @property
    def stasised(self) -> bool:
        """
        :type: bool
        """
    @stasised.setter
    def stasised(self, arg1: bool) -> None:
        pass
    @property
    def stimmed(self) -> bool:
        """
        :type: bool
        """
    @stimmed.setter
    def stimmed(self, arg1: bool) -> None:
        pass
    @property
    def stuck(self) -> bool:
        """
        :type: bool
        """
    @stuck.setter
    def stuck(self, arg1: bool) -> None:
        pass
    @property
    def targetable(self) -> bool:
        """
        :type: bool
        """
    @targetable.setter
    def targetable(self, arg1: bool) -> None:
        pass
    @property
    def training(self) -> bool:
        """
        :type: bool
        """
    @training.setter
    def training(self, arg1: bool) -> None:
        pass
    @property
    def type(self) -> int:
        """
        :type: int
        """
    @type.setter
    def type(self, arg0: int) -> None:
        pass
    @property
    def under_attack(self) -> bool:
        """
        :type: bool
        """
    @under_attack.setter
    def under_attack(self, arg1: bool) -> None:
        pass
    @property
    def under_dark_swarm(self) -> bool:
        """
        :type: bool
        """
    @under_dark_swarm.setter
    def under_dark_swarm(self, arg1: bool) -> None:
        pass
    @property
    def under_disruption_web(self) -> bool:
        """
        :type: bool
        """
    @under_disruption_web.setter
    def under_disruption_web(self, arg1: bool) -> None:
        pass
    @property
    def under_storm(self) -> bool:
        """
        :type: bool
        """
    @under_storm.setter
    def under_storm(self, arg1: bool) -> None:
        pass
    @property
    def upgrading(self) -> bool:
        """
        :type: bool
        """
    @upgrading.setter
    def upgrading(self, arg1: bool) -> None:
        pass
    @property
    def velocityX(self) -> float:
        """
        :type: float
        """
    @velocityX.setter
    def velocityX(self, arg0: float) -> None:
        pass
    @property
    def velocityY(self) -> float:
        """
        :type: float
        """
    @velocityY.setter
    def velocityY(self, arg0: float) -> None:
        pass
    @property
    def visible(self) -> int:
        """
        :type: int
        """
    @visible.setter
    def visible(self, arg0: int) -> None:
        pass
    @property
    def x(self) -> int:
        """
        :type: int
        """
    @x.setter
    def x(self, arg0: int) -> None:
        pass
    @property
    def y(self) -> int:
        """
        :type: int
        """
    @y.setter
    def y(self, arg0: int) -> None:
        pass
    pass
class UnitCommand():
    def __eq__(self, other) -> bool: ...
    def __init__(self) -> None: ...
    @property
    def extra(self) -> int:
        """
        :type: int
        """
    @extra.setter
    def extra(self, arg0: int) -> None:
        pass
    @property
    def frame(self) -> int:
        """
        :type: int
        """
    @frame.setter
    def frame(self, arg0: int) -> None:
        pass
    @property
    def targetId(self) -> int:
        """
        :type: int
        """
    @targetId.setter
    def targetId(self, arg0: int) -> None:
        pass
    @property
    def targetX(self) -> int:
        """
        :type: int
        """
    @targetX.setter
    def targetX(self, arg0: int) -> None:
        pass
    @property
    def targetY(self) -> int:
        """
        :type: int
        """
    @targetY.setter
    def targetY(self, arg0: int) -> None:
        pass
    @property
    def type(self) -> int:
        """
        :type: int
        """
    @type.setter
    def type(self, arg0: int) -> None:
        pass
    pass
class UnitFeatureData():
    def __init__(self) -> None: ...
    def data(self) -> numpy.ndarray[float32]: ...
    def ids(self) -> numpy.ndarray[int32]: ...
    def positions(self) -> numpy.ndarray[int32]: ...
    pass
def featurize_buildability(arg0: State) -> List[numpy.ndarray[float32]]:
    pass
def featurize_creep(arg0: State) -> List[numpy.ndarray[float32]]:
    pass
def featurize_fog(arg0: State) -> List[numpy.ndarray[float32]]:
    pass
def featurize_ground_height(arg0: State) -> List[numpy.ndarray[float32]]:
    pass
def featurize_ground_height_onehot(arg0: State) -> List[numpy.ndarray[float32]]:
    pass
def featurize_map_dynamic(arg0: State) -> List[numpy.ndarray[float32]]:
    pass
def featurize_map_static(arg0: State) -> List[numpy.ndarray[float32]]:
    pass
def featurize_resources(arg0: State) -> List[numpy.ndarray[float32]]:
    pass
def featurize_start_locations(arg0: State) -> List[numpy.ndarray[float32]]:
    pass
def featurize_structures(arg0: State) -> List[numpy.ndarray[float32]]:
    pass
def featurize_tall_doodad(arg0: State) -> List[numpy.ndarray[float32]]:
    pass
def featurize_units(arg0: State, arg1: int) -> UnitFeatureData:
    pass
def featurize_walkability(arg0: State) -> List[numpy.ndarray[float32]]:
    pass
def featurize_xygrid(arg0: State) -> List[numpy.ndarray[float32]]:
    pass
def set_paths(bwenv: str = '', bwapilauncher: str = '', mpq: str = '') -> None:
    """
    Sets various paths (bwenv, bwapilauncher, mpq)
    """
Melee: GameType # value = GameType.Melee
UseMapSettings: GameType # value = GameType.UseMapSettings
__version__ = '0.0.0'
