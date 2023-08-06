from typing import *
from typing import Iterable as iterable
from typing import Iterator as iterator
from numpy import float64, float32, int32, uint8
import numpy
_Shape = Tuple[int, ...]
__all__  = [
"AIPatrol",
"ArchonWarp",
"AtkMoveEP",
"Attack1",
"Attack2",
"AttackFixedRange",
"AttackMove",
"AttackTile",
"AttackUnit",
"BuildAddon",
"BuildNydusExit",
"BuildingLand",
"BuildingLiftOff",
"BunkerGuard",
"Burrowed",
"Burrowing",
"CTFCOP2",
"CTFCOPInit",
"CTFCOPStarted",
"Carrier",
"CarrierAttack",
"CarrierFight",
"CarrierHoldPosition",
"CarrierIgnore2",
"CarrierMoveToAttack",
"CarrierStop",
"CastConsume",
"CastDarkSwarm",
"CastDefensiveMatrix",
"CastDisruptionWeb",
"CastEMPShockwave",
"CastEnsnare",
"CastFeedback",
"CastHallucination",
"CastInfestation",
"CastIrradiate",
"CastLockdown",
"CastMaelstrom",
"CastMindControl",
"CastNuclearStrike",
"CastOpticalFlare",
"CastParasite",
"CastPlague",
"CastPsionicStorm",
"CastRecall",
"CastRestoration",
"CastScannerSweep",
"CastSpawnBroodlings",
"CastStasisField",
"Cloak",
"CloakNearbyUnits",
"CloseDoor",
"CompletingArchonSummon",
"ComputerAI",
"ComputerReturn",
"ConstructingBuilding",
"CreateProtossBuilding",
"Critter",
"DarkArchonMeld",
"Decloak",
"Die",
"DisableDoodad",
"DroneBuild",
"DroneLand",
"DroneLiftOff",
"DroneStartBuild",
"EnableDoodad",
"EnterNydusCanal",
"EnterTransport",
"Fatal",
"FireYamatoGun",
"Follow",
"Guard",
"GuardPost",
"GuardianAspect",
"Hallucination2",
"HarassMove",
"Harvest1",
"Harvest2",
"Harvest3",
"Harvest4",
"HarvestGas",
"HealMove",
"HiddenGun",
"HideTrap",
"HoldPosition",
"Hover",
"IncompleteBuilding",
"IncompleteMorphing",
"IncompleteWarping",
"InfestedCommandCenter",
"InfestingCommandCenter",
"InitCreepGrowth",
"InitializeArbiter",
"InitializePsiProvider",
"InterceptorAttack",
"InterceptorReturn",
"Interrupted",
"JunkYardDog",
"Larva",
"LiftingOff",
"MAX",
"Medic",
"MedicHeal",
"MedicHealToIdle",
"MedicHoldPosition",
"MiningMinerals",
"Move",
"MoveToFireYamatoGun",
"MoveToGas",
"MoveToInfest",
"MoveToMinerals",
"MoveToRepair",
"MoveUnload",
"Neutral",
"Nothing",
"NukeLaunch",
"NukePaint",
"NukeTrack",
"NukeTrain",
"NukeUnit",
"NukeWait",
"OpenDoor",
"Patrol",
"Pickup4",
"PickupBunker",
"PickupIdle",
"PickupTransport",
"PlaceAddon",
"PlaceBuilding",
"PlaceMine",
"PlaceProtossBuilding",
"PlayerGuard",
"PowerupIdle",
"QueenHoldPosition",
"RallyPointTile",
"RallyPointUnit",
"Reaver",
"ReaverAttack",
"ReaverCarrierMove",
"ReaverFight",
"ReaverHoldPosition",
"ReaverMoveToAttack",
"ReaverStop",
"RechargeShieldsBattery",
"RechargeShieldsUnit",
"Repair",
"RescuePassive",
"ResearchTech",
"ResetCollision",
"ResetHarvestCollision",
"ReturnGas",
"ReturnMinerals",
"RevealTrap",
"RightClickAction",
"Scanner",
"ScarabAttack",
"SelfDestructing",
"ShieldBattery",
"Sieging",
"SpawningLarva",
"SpreadCreep",
"StayInRange",
"Stop",
"StoppingCreepGrowth",
"SuicideHoldPosition",
"SuicideLocation",
"SuicideUnit",
"Teleport",
"TowerAttack",
"TowerGuard",
"Train",
"TrainFighter",
"TurretAttack",
"TurretGuard",
"Unburrowing",
"Unknown",
"Unload",
"Unsieging",
"UnusedNothing",
"UnusedPowerup",
"Unused_24",
"Upgrade",
"VultureMine",
"WaitForGas",
"WaitForMinerals",
"WarpIn",
"WatchTarget",
"ZergBirth",
"ZergBuildingMorph",
"ZergUnitMorph",
"ids",
"names"
]
AIPatrol = 159
ArchonWarp = 105
AtkMoveEP = 157
Attack1 = 8
Attack2 = 9
AttackFixedRange = 11
AttackMove = 14
AttackTile = 12
AttackUnit = 10
BuildAddon = 37
BuildNydusExit = 46
BuildingLand = 71
BuildingLiftOff = 72
BunkerGuard = 5
Burrowed = 117
Burrowing = 116
CTFCOP2 = 155
CTFCOPInit = 153
CTFCOPStarted = 154
Carrier = 50
CarrierAttack = 53
CarrierFight = 56
CarrierHoldPosition = 57
CarrierIgnore2 = 55
CarrierMoveToAttack = 54
CarrierStop = 52
CastConsume = 145
CastDarkSwarm = 119
CastDefensiveMatrix = 141
CastDisruptionWeb = 181
CastEMPShockwave = 122
CastEnsnare = 146
CastFeedback = 184
CastHallucination = 148
CastInfestation = 27
CastIrradiate = 143
CastLockdown = 115
CastMaelstrom = 186
CastMindControl = 182
CastNuclearStrike = 128
CastOpticalFlare = 185
CastParasite = 120
CastPlague = 144
CastPsionicStorm = 142
CastRecall = 137
CastRestoration = 180
CastScannerSweep = 139
CastSpawnBroodlings = 121
CastStasisField = 147
Cloak = 109
CloakNearbyUnits = 131
CloseDoor = 169
CompletingArchonSummon = 106
ComputerAI = 156
ComputerReturn = 163
ConstructingBuilding = 33
CreateProtossBuilding = 32
Critter = 166
DarkArchonMeld = 183
Decloak = 110
Die = 0
DisableDoodad = 173
DroneBuild = 26
DroneLand = 70
DroneLiftOff = 73
DroneStartBuild = 25
EnableDoodad = 172
EnterNydusCanal = 47
EnterTransport = 92
Fatal = 188
FireYamatoGun = 113
Follow = 49
Guard = 2
GuardPost = 160
GuardianAspect = 104
Hallucination2 = 149
HarassMove = 158
Harvest1 = 79
Harvest2 = 80
Harvest3 = 88
Harvest4 = 89
HarvestGas = 83
HealMove = 177
HiddenGun = 167
HideTrap = 170
HoldPosition = 107
Hover = 13
IncompleteBuilding = 44
IncompleteMorphing = 45
IncompleteWarping = 48
InfestedCommandCenter = 15
InfestingCommandCenter = 29
InitCreepGrowth = 101
InitializeArbiter = 130
InitializePsiProvider = 164
InterceptorAttack = 64
InterceptorReturn = 69
Interrupted = 91
JunkYardDog = 187
Larva = 77
LiftingOff = 74
MAX = 191
Medic = 175
MedicHeal = 176
MedicHealToIdle = 179
MedicHoldPosition = 178
MiningMinerals = 87
Move = 6
MoveToFireYamatoGun = 114
MoveToGas = 81
MoveToInfest = 28
MoveToMinerals = 85
MoveToRepair = 35
MoveUnload = 112
Neutral = 162
Nothing = 23
NukeLaunch = 125
NukePaint = 126
NukeTrack = 129
NukeTrain = 124
NukeUnit = 127
NukeWait = 123
OpenDoor = 168
Patrol = 152
Pickup4 = 96
PickupBunker = 95
PickupIdle = 93
PickupTransport = 94
PlaceAddon = 36
PlaceBuilding = 30
PlaceMine = 132
PlaceProtossBuilding = 31
PlayerGuard = 3
PowerupIdle = 97
QueenHoldPosition = 108
RallyPointTile = 40
RallyPointUnit = 39
Reaver = 58
ReaverAttack = 59
ReaverCarrierMove = 51
ReaverFight = 61
ReaverHoldPosition = 62
ReaverMoveToAttack = 60
ReaverStop = 7
RechargeShieldsBattery = 67
RechargeShieldsUnit = 66
Repair = 34
RescuePassive = 161
ResearchTech = 75
ResetCollision = 150
ResetHarvestCollision = 151
ReturnGas = 84
ReturnMinerals = 90
RevealTrap = 171
RightClickAction = 133
Scanner = 140
ScarabAttack = 65
SelfDestructing = 165
ShieldBattery = 68
Sieging = 98
SpawningLarva = 78
SpreadCreep = 102
StayInRange = 21
Stop = 1
StoppingCreepGrowth = 103
SuicideHoldPosition = 136
SuicideLocation = 135
SuicideUnit = 134
Teleport = 138
TowerAttack = 19
TowerGuard = 18
Train = 38
TrainFighter = 63
TurretAttack = 22
TurretGuard = 4
Unburrowing = 118
Unknown = 190
Unload = 111
Unsieging = 99
UnusedNothing = 16
UnusedPowerup = 17
Unused_24 = 24
Upgrade = 76
VultureMine = 20
WaitForGas = 82
WaitForMinerals = 86
WarpIn = 174
WatchTarget = 100
ZergBirth = 41
ZergBuildingMorph = 43
ZergUnitMorph = 42
ids = {0: 'Die', 1: 'Stop', 2: 'Guard', 3: 'PlayerGuard', 4: 'TurretGuard', 5: 'BunkerGuard', 6: 'Move', 7: 'ReaverStop', 8: 'Attack1', 9: 'Attack2', 10: 'AttackUnit', 11: 'AttackFixedRange', 12: 'AttackTile', 13: 'Hover', 14: 'AttackMove', 15: 'InfestedCommandCenter', 16: 'UnusedNothing', 17: 'UnusedPowerup', 18: 'TowerGuard', 19: 'TowerAttack', 20: 'VultureMine', 21: 'StayInRange', 22: 'TurretAttack', 23: 'Nothing', 24: 'Unused_24', 25: 'DroneStartBuild', 26: 'DroneBuild', 27: 'CastInfestation', 28: 'MoveToInfest', 29: 'InfestingCommandCenter', 30: 'PlaceBuilding', 31: 'PlaceProtossBuilding', 32: 'CreateProtossBuilding', 33: 'ConstructingBuilding', 34: 'Repair', 35: 'MoveToRepair', 36: 'PlaceAddon', 37: 'BuildAddon', 38: 'Train', 39: 'RallyPointUnit', 40: 'RallyPointTile', 41: 'ZergBirth', 42: 'ZergUnitMorph', 43: 'ZergBuildingMorph', 44: 'IncompleteBuilding', 45: 'IncompleteMorphing', 46: 'BuildNydusExit', 47: 'EnterNydusCanal', 48: 'IncompleteWarping', 49: 'Follow', 50: 'Carrier', 51: 'ReaverCarrierMove', 52: 'CarrierStop', 53: 'CarrierAttack', 54: 'CarrierMoveToAttack', 55: 'CarrierIgnore2', 56: 'CarrierFight', 57: 'CarrierHoldPosition', 58: 'Reaver', 59: 'ReaverAttack', 60: 'ReaverMoveToAttack', 61: 'ReaverFight', 62: 'ReaverHoldPosition', 63: 'TrainFighter', 64: 'InterceptorAttack', 65: 'ScarabAttack', 66: 'RechargeShieldsUnit', 67: 'RechargeShieldsBattery', 68: 'ShieldBattery', 69: 'InterceptorReturn', 70: 'DroneLand', 71: 'BuildingLand', 72: 'BuildingLiftOff', 73: 'DroneLiftOff', 74: 'LiftingOff', 75: 'ResearchTech', 76: 'Upgrade', 77: 'Larva', 78: 'SpawningLarva', 79: 'Harvest1', 80: 'Harvest2', 81: 'MoveToGas', 82: 'WaitForGas', 83: 'HarvestGas', 84: 'ReturnGas', 85: 'MoveToMinerals', 86: 'WaitForMinerals', 87: 'MiningMinerals', 88: 'Harvest3', 89: 'Harvest4', 90: 'ReturnMinerals', 91: 'Interrupted', 92: 'EnterTransport', 93: 'PickupIdle', 94: 'PickupTransport', 95: 'PickupBunker', 96: 'Pickup4', 97: 'PowerupIdle', 98: 'Sieging', 99: 'Unsieging', 100: 'WatchTarget', 101: 'InitCreepGrowth', 102: 'SpreadCreep', 103: 'StoppingCreepGrowth', 104: 'GuardianAspect', 105: 'ArchonWarp', 106: 'CompletingArchonSummon', 107: 'HoldPosition', 108: 'QueenHoldPosition', 109: 'Cloak', 110: 'Decloak', 111: 'Unload', 112: 'MoveUnload', 113: 'FireYamatoGun', 114: 'MoveToFireYamatoGun', 115: 'CastLockdown', 116: 'Burrowing', 117: 'Burrowed', 118: 'Unburrowing', 119: 'CastDarkSwarm', 120: 'CastParasite', 121: 'CastSpawnBroodlings', 122: 'CastEMPShockwave', 123: 'NukeWait', 124: 'NukeTrain', 125: 'NukeLaunch', 126: 'NukePaint', 127: 'NukeUnit', 128: 'CastNuclearStrike', 129: 'NukeTrack', 130: 'InitializeArbiter', 131: 'CloakNearbyUnits', 132: 'PlaceMine', 133: 'RightClickAction', 134: 'SuicideUnit', 135: 'SuicideLocation', 136: 'SuicideHoldPosition', 137: 'CastRecall', 138: 'Teleport', 139: 'CastScannerSweep', 140: 'Scanner', 141: 'CastDefensiveMatrix', 142: 'CastPsionicStorm', 143: 'CastIrradiate', 144: 'CastPlague', 145: 'CastConsume', 146: 'CastEnsnare', 147: 'CastStasisField', 148: 'CastHallucination', 149: 'Hallucination2', 150: 'ResetCollision', 151: 'ResetHarvestCollision', 152: 'Patrol', 153: 'CTFCOPInit', 154: 'CTFCOPStarted', 155: 'CTFCOP2', 156: 'ComputerAI', 157: 'AtkMoveEP', 158: 'HarassMove', 159: 'AIPatrol', 160: 'GuardPost', 161: 'RescuePassive', 162: 'Neutral', 163: 'ComputerReturn', 164: 'InitializePsiProvider', 165: 'SelfDestructing', 166: 'Critter', 167: 'HiddenGun', 168: 'OpenDoor', 169: 'CloseDoor', 170: 'HideTrap', 171: 'RevealTrap', 172: 'EnableDoodad', 173: 'DisableDoodad', 174: 'WarpIn', 175: 'Medic', 176: 'MedicHeal', 177: 'HealMove', 178: 'MedicHoldPosition', 179: 'MedicHealToIdle', 180: 'CastRestoration', 181: 'CastDisruptionWeb', 182: 'CastMindControl', 183: 'DarkArchonMeld', 184: 'CastFeedback', 185: 'CastOpticalFlare', 186: 'CastMaelstrom', 187: 'JunkYardDog', 188: 'Fatal', 189: 'None', 190: 'Unknown', 191: 'MAX'}
names = {'Die': 0, 'Stop': 1, 'Guard': 2, 'PlayerGuard': 3, 'TurretGuard': 4, 'BunkerGuard': 5, 'Move': 6, 'ReaverStop': 7, 'Attack1': 8, 'Attack2': 9, 'AttackUnit': 10, 'AttackFixedRange': 11, 'AttackTile': 12, 'Hover': 13, 'AttackMove': 14, 'InfestedCommandCenter': 15, 'UnusedNothing': 16, 'UnusedPowerup': 17, 'TowerGuard': 18, 'TowerAttack': 19, 'VultureMine': 20, 'StayInRange': 21, 'TurretAttack': 22, 'Nothing': 23, 'Unused_24': 24, 'DroneStartBuild': 25, 'DroneBuild': 26, 'CastInfestation': 27, 'MoveToInfest': 28, 'InfestingCommandCenter': 29, 'PlaceBuilding': 30, 'PlaceProtossBuilding': 31, 'CreateProtossBuilding': 32, 'ConstructingBuilding': 33, 'Repair': 34, 'MoveToRepair': 35, 'PlaceAddon': 36, 'BuildAddon': 37, 'Train': 38, 'RallyPointUnit': 39, 'RallyPointTile': 40, 'ZergBirth': 41, 'ZergUnitMorph': 42, 'ZergBuildingMorph': 43, 'IncompleteBuilding': 44, 'IncompleteMorphing': 45, 'BuildNydusExit': 46, 'EnterNydusCanal': 47, 'IncompleteWarping': 48, 'Follow': 49, 'Carrier': 50, 'ReaverCarrierMove': 51, 'CarrierStop': 52, 'CarrierAttack': 53, 'CarrierMoveToAttack': 54, 'CarrierIgnore2': 55, 'CarrierFight': 56, 'CarrierHoldPosition': 57, 'Reaver': 58, 'ReaverAttack': 59, 'ReaverMoveToAttack': 60, 'ReaverFight': 61, 'ReaverHoldPosition': 62, 'TrainFighter': 63, 'InterceptorAttack': 64, 'ScarabAttack': 65, 'RechargeShieldsUnit': 66, 'RechargeShieldsBattery': 67, 'ShieldBattery': 68, 'InterceptorReturn': 69, 'DroneLand': 70, 'BuildingLand': 71, 'BuildingLiftOff': 72, 'DroneLiftOff': 73, 'LiftingOff': 74, 'ResearchTech': 75, 'Upgrade': 76, 'Larva': 77, 'SpawningLarva': 78, 'Harvest1': 79, 'Harvest2': 80, 'MoveToGas': 81, 'WaitForGas': 82, 'HarvestGas': 83, 'ReturnGas': 84, 'MoveToMinerals': 85, 'WaitForMinerals': 86, 'MiningMinerals': 87, 'Harvest3': 88, 'Harvest4': 89, 'ReturnMinerals': 90, 'Interrupted': 91, 'EnterTransport': 92, 'PickupIdle': 93, 'PickupTransport': 94, 'PickupBunker': 95, 'Pickup4': 96, 'PowerupIdle': 97, 'Sieging': 98, 'Unsieging': 99, 'WatchTarget': 100, 'InitCreepGrowth': 101, 'SpreadCreep': 102, 'StoppingCreepGrowth': 103, 'GuardianAspect': 104, 'ArchonWarp': 105, 'CompletingArchonSummon': 106, 'HoldPosition': 107, 'QueenHoldPosition': 108, 'Cloak': 109, 'Decloak': 110, 'Unload': 111, 'MoveUnload': 112, 'FireYamatoGun': 113, 'MoveToFireYamatoGun': 114, 'CastLockdown': 115, 'Burrowing': 116, 'Burrowed': 117, 'Unburrowing': 118, 'CastDarkSwarm': 119, 'CastParasite': 120, 'CastSpawnBroodlings': 121, 'CastEMPShockwave': 122, 'NukeWait': 123, 'NukeTrain': 124, 'NukeLaunch': 125, 'NukePaint': 126, 'NukeUnit': 127, 'CastNuclearStrike': 128, 'NukeTrack': 129, 'InitializeArbiter': 130, 'CloakNearbyUnits': 131, 'PlaceMine': 132, 'RightClickAction': 133, 'SuicideUnit': 134, 'SuicideLocation': 135, 'SuicideHoldPosition': 136, 'CastRecall': 137, 'Teleport': 138, 'CastScannerSweep': 139, 'Scanner': 140, 'CastDefensiveMatrix': 141, 'CastPsionicStorm': 142, 'CastIrradiate': 143, 'CastPlague': 144, 'CastConsume': 145, 'CastEnsnare': 146, 'CastStasisField': 147, 'CastHallucination': 148, 'Hallucination2': 149, 'ResetCollision': 150, 'ResetHarvestCollision': 151, 'Patrol': 152, 'CTFCOPInit': 153, 'CTFCOPStarted': 154, 'CTFCOP2': 155, 'ComputerAI': 156, 'AtkMoveEP': 157, 'HarassMove': 158, 'AIPatrol': 159, 'GuardPost': 160, 'RescuePassive': 161, 'Neutral': 162, 'ComputerReturn': 163, 'InitializePsiProvider': 164, 'SelfDestructing': 165, 'Critter': 166, 'HiddenGun': 167, 'OpenDoor': 168, 'CloseDoor': 169, 'HideTrap': 170, 'RevealTrap': 171, 'EnableDoodad': 172, 'DisableDoodad': 173, 'WarpIn': 174, 'Medic': 175, 'MedicHeal': 176, 'HealMove': 177, 'MedicHoldPosition': 178, 'MedicHealToIdle': 179, 'CastRestoration': 180, 'CastDisruptionWeb': 181, 'CastMindControl': 182, 'DarkArchonMeld': 183, 'CastFeedback': 184, 'CastOpticalFlare': 185, 'CastMaelstrom': 186, 'JunkYardDog': 187, 'Fatal': 188, 'None': 189, 'Unknown': 190, 'MAX': 191}
