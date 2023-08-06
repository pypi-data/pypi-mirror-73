from typing import *
from typing import Iterable as iterable
from typing import Iterator as iterator
from numpy import float64, float32, int32, uint8
import numpy
_Shape = Tuple[int, ...]
__all__  = [
"KillUnit",
"SetPlayerGas",
"SetPlayerMinerals",
"SetPlayerResearched",
"SetPlayerUpgradeLevel",
"SetUnitEnergy",
"SetUnitHealth",
"SetUnitShield",
"SpawnUnit",
"ids",
"names"
]
KillUnit = 0
SetPlayerGas = 5
SetPlayerMinerals = 4
SetPlayerResearched = 3
SetPlayerUpgradeLevel = 2
SetUnitEnergy = 8
SetUnitHealth = 6
SetUnitShield = 7
SpawnUnit = 1
ids = {0: 'KillUnit', 1: 'SpawnUnit', 2: 'SetPlayerUpgradeLevel', 3: 'SetPlayerResearched', 4: 'SetPlayerMinerals', 5: 'SetPlayerGas', 6: 'SetUnitHealth', 7: 'SetUnitShield', 8: 'SetUnitEnergy'}
names = {'KillUnit': 0, 'SpawnUnit': 1, 'SetPlayerUpgradeLevel': 2, 'SetPlayerResearched': 3, 'SetPlayerMinerals': 4, 'SetPlayerGas': 5, 'SetUnitHealth': 6, 'SetUnitShield': 7, 'SetUnitEnergy': 8}
