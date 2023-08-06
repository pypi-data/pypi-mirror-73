from typing import *
from typing import Iterable as iterable
from typing import Iterator as iterator
from numpy import float64, float32, int32, uint8
import numpy
_Shape = Tuple[int, ...]
__all__  = [
"Attack_Move",
"Attack_Unit",
"Build",
"Build_Addon",
"Burrow",
"Cancel_Addon",
"Cancel_Construction",
"Cancel_Morph",
"Cancel_Research",
"Cancel_Train",
"Cancel_Train_Slot",
"Cancel_Upgrade",
"Cloak",
"Decloak",
"Follow",
"Gather",
"Halt_Construction",
"Hold_Position",
"Land",
"Lift",
"Load",
"MAX",
"Morph",
"Move",
"Patrol",
"Place_COP",
"Repair",
"Research",
"Return_Cargo",
"Right_Click_Position",
"Right_Click_Unit",
"Set_Rally_Position",
"Set_Rally_Unit",
"Siege",
"Stop",
"Train",
"Unburrow",
"Unknown",
"Unload",
"Unload_All",
"Unload_All_Position",
"Unsiege",
"Upgrade",
"Use_Tech",
"Use_Tech_Position",
"Use_Tech_Unit",
"ids",
"names"
]
Attack_Move = 0
Attack_Unit = 1
Build = 2
Build_Addon = 3
Burrow = 18
Cancel_Addon = 34
Cancel_Construction = 33
Cancel_Morph = 37
Cancel_Research = 38
Cancel_Train = 35
Cancel_Train_Slot = 36
Cancel_Upgrade = 39
Cloak = 20
Decloak = 21
Follow = 14
Gather = 15
Halt_Construction = 32
Hold_Position = 12
Land = 25
Lift = 24
Load = 26
MAX = 46
Morph = 5
Move = 10
Patrol = 11
Place_COP = 43
Repair = 17
Research = 6
Return_Cargo = 16
Right_Click_Position = 30
Right_Click_Unit = 31
Set_Rally_Position = 8
Set_Rally_Unit = 9
Siege = 22
Stop = 13
Train = 4
Unburrow = 19
Unknown = 45
Unload = 27
Unload_All = 28
Unload_All_Position = 29
Unsiege = 23
Upgrade = 7
Use_Tech = 40
Use_Tech_Position = 41
Use_Tech_Unit = 42
ids = {0: 'Attack_Move', 1: 'Attack_Unit', 2: 'Build', 3: 'Build_Addon', 4: 'Train', 5: 'Morph', 6: 'Research', 7: 'Upgrade', 8: 'Set_Rally_Position', 9: 'Set_Rally_Unit', 10: 'Move', 11: 'Patrol', 12: 'Hold_Position', 13: 'Stop', 14: 'Follow', 15: 'Gather', 16: 'Return_Cargo', 17: 'Repair', 18: 'Burrow', 19: 'Unburrow', 20: 'Cloak', 21: 'Decloak', 22: 'Siege', 23: 'Unsiege', 24: 'Lift', 25: 'Land', 26: 'Load', 27: 'Unload', 28: 'Unload_All', 29: 'Unload_All_Position', 30: 'Right_Click_Position', 31: 'Right_Click_Unit', 32: 'Halt_Construction', 33: 'Cancel_Construction', 34: 'Cancel_Addon', 35: 'Cancel_Train', 36: 'Cancel_Train_Slot', 37: 'Cancel_Morph', 38: 'Cancel_Research', 39: 'Cancel_Upgrade', 40: 'Use_Tech', 41: 'Use_Tech_Position', 42: 'Use_Tech_Unit', 43: 'Place_COP', 44: 'None', 45: 'Unknown', 46: 'MAX'}
names = {'Attack_Move': 0, 'Attack_Unit': 1, 'Build': 2, 'Build_Addon': 3, 'Train': 4, 'Morph': 5, 'Research': 6, 'Upgrade': 7, 'Set_Rally_Position': 8, 'Set_Rally_Unit': 9, 'Move': 10, 'Patrol': 11, 'Hold_Position': 12, 'Stop': 13, 'Follow': 14, 'Gather': 15, 'Return_Cargo': 16, 'Repair': 17, 'Burrow': 18, 'Unburrow': 19, 'Cloak': 20, 'Decloak': 21, 'Siege': 22, 'Unsiege': 23, 'Lift': 24, 'Land': 25, 'Load': 26, 'Unload': 27, 'Unload_All': 28, 'Unload_All_Position': 29, 'Right_Click_Position': 30, 'Right_Click_Unit': 31, 'Halt_Construction': 32, 'Cancel_Construction': 33, 'Cancel_Addon': 34, 'Cancel_Train': 35, 'Cancel_Train_Slot': 36, 'Cancel_Morph': 37, 'Cancel_Research': 38, 'Cancel_Upgrade': 39, 'Use_Tech': 40, 'Use_Tech_Position': 41, 'Use_Tech_Unit': 42, 'Place_COP': 43, 'None': 44, 'Unknown': 45, 'MAX': 46}
