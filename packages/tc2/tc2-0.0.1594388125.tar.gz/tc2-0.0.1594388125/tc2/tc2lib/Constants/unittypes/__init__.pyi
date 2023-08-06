from typing import *
from typing import Iterable as iterable
from typing import Iterator as iterator
from numpy import float64, float32, int32, uint8
import numpy
_Shape = Tuple[int, ...]
__all__  = [
"Critter_Bengalaas",
"Critter_Kakaru",
"Critter_Ragnasaur",
"Critter_Rhynadon",
"Critter_Scantid",
"Critter_Ursadon",
"MAX",
"Protoss_Arbiter",
"Protoss_Arbiter_Tribunal",
"Protoss_Archon",
"Protoss_Assimilator",
"Protoss_Carrier",
"Protoss_Citadel_of_Adun",
"Protoss_Corsair",
"Protoss_Cybernetics_Core",
"Protoss_Dark_Archon",
"Protoss_Dark_Templar",
"Protoss_Dragoon",
"Protoss_Fleet_Beacon",
"Protoss_Forge",
"Protoss_Gateway",
"Protoss_High_Templar",
"Protoss_Interceptor",
"Protoss_Nexus",
"Protoss_Observatory",
"Protoss_Observer",
"Protoss_Photon_Cannon",
"Protoss_Probe",
"Protoss_Pylon",
"Protoss_Reaver",
"Protoss_Robotics_Facility",
"Protoss_Robotics_Support_Bay",
"Protoss_Scarab",
"Protoss_Scout",
"Protoss_Shield_Battery",
"Protoss_Shuttle",
"Protoss_Stargate",
"Protoss_Templar_Archives",
"Protoss_Zealot",
"Resource_Mineral_Field",
"Resource_Mineral_Field_Type_2",
"Resource_Mineral_Field_Type_3",
"Resource_Vespene_Geyser",
"Special_Pit_Door",
"Special_Right_Pit_Door",
"Spell_Dark_Swarm",
"Spell_Disruption_Web",
"Spell_Scanner_Sweep",
"Terran_Academy",
"Terran_Armory",
"Terran_Barracks",
"Terran_Battlecruiser",
"Terran_Bunker",
"Terran_Civilian",
"Terran_Command_Center",
"Terran_Comsat_Station",
"Terran_Control_Tower",
"Terran_Covert_Ops",
"Terran_Dropship",
"Terran_Engineering_Bay",
"Terran_Factory",
"Terran_Firebat",
"Terran_Ghost",
"Terran_Goliath",
"Terran_Machine_Shop",
"Terran_Marine",
"Terran_Medic",
"Terran_Missile_Turret",
"Terran_Nuclear_Missile",
"Terran_Nuclear_Silo",
"Terran_Physics_Lab",
"Terran_Refinery",
"Terran_SCV",
"Terran_Science_Facility",
"Terran_Science_Vessel",
"Terran_Siege_Tank_Siege_Mode",
"Terran_Siege_Tank_Tank_Mode",
"Terran_Starport",
"Terran_Supply_Depot",
"Terran_Valkyrie",
"Terran_Vulture",
"Terran_Vulture_Spider_Mine",
"Terran_Wraith",
"Zerg_Broodling",
"Zerg_Cocoon",
"Zerg_Creep_Colony",
"Zerg_Defiler",
"Zerg_Defiler_Mound",
"Zerg_Devourer",
"Zerg_Drone",
"Zerg_Egg",
"Zerg_Evolution_Chamber",
"Zerg_Extractor",
"Zerg_Greater_Spire",
"Zerg_Guardian",
"Zerg_Hatchery",
"Zerg_Hive",
"Zerg_Hydralisk",
"Zerg_Hydralisk_Den",
"Zerg_Infested_Command_Center",
"Zerg_Infested_Terran",
"Zerg_Lair",
"Zerg_Larva",
"Zerg_Lurker",
"Zerg_Lurker_Egg",
"Zerg_Mutalisk",
"Zerg_Nydus_Canal",
"Zerg_Overlord",
"Zerg_Queen",
"Zerg_Queens_Nest",
"Zerg_Scourge",
"Zerg_Spawning_Pool",
"Zerg_Spire",
"Zerg_Spore_Colony",
"Zerg_Sunken_Colony",
"Zerg_Ultralisk",
"Zerg_Ultralisk_Cavern",
"Zerg_Zergling",
"ids",
"names"
]
Critter_Bengalaas = 90
Critter_Kakaru = 94
Critter_Ragnasaur = 95
Critter_Rhynadon = 89
Critter_Scantid = 93
Critter_Ursadon = 96
MAX = 233
Protoss_Arbiter = 71
Protoss_Arbiter_Tribunal = 170
Protoss_Archon = 68
Protoss_Assimilator = 157
Protoss_Carrier = 72
Protoss_Citadel_of_Adun = 163
Protoss_Corsair = 60
Protoss_Cybernetics_Core = 164
Protoss_Dark_Archon = 63
Protoss_Dark_Templar = 61
Protoss_Dragoon = 66
Protoss_Fleet_Beacon = 169
Protoss_Forge = 166
Protoss_Gateway = 160
Protoss_High_Templar = 67
Protoss_Interceptor = 73
Protoss_Nexus = 154
Protoss_Observatory = 159
Protoss_Observer = 84
Protoss_Photon_Cannon = 162
Protoss_Probe = 64
Protoss_Pylon = 156
Protoss_Reaver = 83
Protoss_Robotics_Facility = 155
Protoss_Robotics_Support_Bay = 171
Protoss_Scarab = 85
Protoss_Scout = 70
Protoss_Shield_Battery = 172
Protoss_Shuttle = 69
Protoss_Stargate = 167
Protoss_Templar_Archives = 165
Protoss_Zealot = 65
Resource_Mineral_Field = 176
Resource_Mineral_Field_Type_2 = 177
Resource_Mineral_Field_Type_3 = 178
Resource_Vespene_Geyser = 188
Special_Pit_Door = 207
Special_Right_Pit_Door = 208
Spell_Dark_Swarm = 202
Spell_Disruption_Web = 105
Spell_Scanner_Sweep = 33
Terran_Academy = 112
Terran_Armory = 123
Terran_Barracks = 111
Terran_Battlecruiser = 12
Terran_Bunker = 125
Terran_Civilian = 15
Terran_Command_Center = 106
Terran_Comsat_Station = 107
Terran_Control_Tower = 115
Terran_Covert_Ops = 117
Terran_Dropship = 11
Terran_Engineering_Bay = 122
Terran_Factory = 113
Terran_Firebat = 32
Terran_Ghost = 1
Terran_Goliath = 3
Terran_Machine_Shop = 120
Terran_Marine = 0
Terran_Medic = 34
Terran_Missile_Turret = 124
Terran_Nuclear_Missile = 14
Terran_Nuclear_Silo = 108
Terran_Physics_Lab = 118
Terran_Refinery = 110
Terran_SCV = 7
Terran_Science_Facility = 116
Terran_Science_Vessel = 9
Terran_Siege_Tank_Siege_Mode = 30
Terran_Siege_Tank_Tank_Mode = 5
Terran_Starport = 114
Terran_Supply_Depot = 109
Terran_Valkyrie = 58
Terran_Vulture = 2
Terran_Vulture_Spider_Mine = 13
Terran_Wraith = 8
Zerg_Broodling = 40
Zerg_Cocoon = 59
Zerg_Creep_Colony = 143
Zerg_Defiler = 46
Zerg_Defiler_Mound = 136
Zerg_Devourer = 62
Zerg_Drone = 41
Zerg_Egg = 36
Zerg_Evolution_Chamber = 139
Zerg_Extractor = 149
Zerg_Greater_Spire = 137
Zerg_Guardian = 44
Zerg_Hatchery = 131
Zerg_Hive = 133
Zerg_Hydralisk = 38
Zerg_Hydralisk_Den = 135
Zerg_Infested_Command_Center = 130
Zerg_Infested_Terran = 50
Zerg_Lair = 132
Zerg_Larva = 35
Zerg_Lurker = 103
Zerg_Lurker_Egg = 97
Zerg_Mutalisk = 43
Zerg_Nydus_Canal = 134
Zerg_Overlord = 42
Zerg_Queen = 45
Zerg_Queens_Nest = 138
Zerg_Scourge = 47
Zerg_Spawning_Pool = 142
Zerg_Spire = 141
Zerg_Spore_Colony = 144
Zerg_Sunken_Colony = 146
Zerg_Ultralisk = 39
Zerg_Ultralisk_Cavern = 140
Zerg_Zergling = 37
ids = {0: 'Terran_Marine', 1: 'Terran_Ghost', 2: 'Terran_Vulture', 3: 'Terran_Goliath', 5: 'Terran_Siege_Tank_Tank_Mode', 7: 'Terran_SCV', 8: 'Terran_Wraith', 9: 'Terran_Science_Vessel', 11: 'Terran_Dropship', 12: 'Terran_Battlecruiser', 13: 'Terran_Vulture_Spider_Mine', 14: 'Terran_Nuclear_Missile', 15: 'Terran_Civilian', 30: 'Terran_Siege_Tank_Siege_Mode', 32: 'Terran_Firebat', 33: 'Spell_Scanner_Sweep', 34: 'Terran_Medic', 35: 'Zerg_Larva', 36: 'Zerg_Egg', 37: 'Zerg_Zergling', 38: 'Zerg_Hydralisk', 39: 'Zerg_Ultralisk', 40: 'Zerg_Broodling', 41: 'Zerg_Drone', 42: 'Zerg_Overlord', 43: 'Zerg_Mutalisk', 44: 'Zerg_Guardian', 45: 'Zerg_Queen', 46: 'Zerg_Defiler', 47: 'Zerg_Scourge', 50: 'Zerg_Infested_Terran', 58: 'Terran_Valkyrie', 59: 'Zerg_Cocoon', 60: 'Protoss_Corsair', 61: 'Protoss_Dark_Templar', 62: 'Zerg_Devourer', 63: 'Protoss_Dark_Archon', 64: 'Protoss_Probe', 65: 'Protoss_Zealot', 66: 'Protoss_Dragoon', 67: 'Protoss_High_Templar', 68: 'Protoss_Archon', 69: 'Protoss_Shuttle', 70: 'Protoss_Scout', 71: 'Protoss_Arbiter', 72: 'Protoss_Carrier', 73: 'Protoss_Interceptor', 83: 'Protoss_Reaver', 84: 'Protoss_Observer', 85: 'Protoss_Scarab', 89: 'Critter_Rhynadon', 90: 'Critter_Bengalaas', 93: 'Critter_Scantid', 94: 'Critter_Kakaru', 95: 'Critter_Ragnasaur', 96: 'Critter_Ursadon', 97: 'Zerg_Lurker_Egg', 103: 'Zerg_Lurker', 105: 'Spell_Disruption_Web', 106: 'Terran_Command_Center', 107: 'Terran_Comsat_Station', 108: 'Terran_Nuclear_Silo', 109: 'Terran_Supply_Depot', 110: 'Terran_Refinery', 111: 'Terran_Barracks', 112: 'Terran_Academy', 113: 'Terran_Factory', 114: 'Terran_Starport', 115: 'Terran_Control_Tower', 116: 'Terran_Science_Facility', 117: 'Terran_Covert_Ops', 118: 'Terran_Physics_Lab', 120: 'Terran_Machine_Shop', 122: 'Terran_Engineering_Bay', 123: 'Terran_Armory', 124: 'Terran_Missile_Turret', 125: 'Terran_Bunker', 130: 'Zerg_Infested_Command_Center', 131: 'Zerg_Hatchery', 132: 'Zerg_Lair', 133: 'Zerg_Hive', 134: 'Zerg_Nydus_Canal', 135: 'Zerg_Hydralisk_Den', 136: 'Zerg_Defiler_Mound', 137: 'Zerg_Greater_Spire', 138: 'Zerg_Queens_Nest', 139: 'Zerg_Evolution_Chamber', 140: 'Zerg_Ultralisk_Cavern', 141: 'Zerg_Spire', 142: 'Zerg_Spawning_Pool', 143: 'Zerg_Creep_Colony', 144: 'Zerg_Spore_Colony', 146: 'Zerg_Sunken_Colony', 149: 'Zerg_Extractor', 154: 'Protoss_Nexus', 155: 'Protoss_Robotics_Facility', 156: 'Protoss_Pylon', 157: 'Protoss_Assimilator', 159: 'Protoss_Observatory', 160: 'Protoss_Gateway', 162: 'Protoss_Photon_Cannon', 163: 'Protoss_Citadel_of_Adun', 164: 'Protoss_Cybernetics_Core', 165: 'Protoss_Templar_Archives', 166: 'Protoss_Forge', 167: 'Protoss_Stargate', 169: 'Protoss_Fleet_Beacon', 170: 'Protoss_Arbiter_Tribunal', 171: 'Protoss_Robotics_Support_Bay', 172: 'Protoss_Shield_Battery', 176: 'Resource_Mineral_Field', 177: 'Resource_Mineral_Field_Type_2', 178: 'Resource_Mineral_Field_Type_3', 188: 'Resource_Vespene_Geyser', 202: 'Spell_Dark_Swarm', 207: 'Special_Pit_Door', 208: 'Special_Right_Pit_Door', 233: 'MAX'}
names = {'Terran_Marine': 0, 'Terran_Ghost': 1, 'Terran_Vulture': 2, 'Terran_Goliath': 3, 'Terran_Siege_Tank_Tank_Mode': 5, 'Terran_SCV': 7, 'Terran_Wraith': 8, 'Terran_Science_Vessel': 9, 'Terran_Dropship': 11, 'Terran_Battlecruiser': 12, 'Terran_Vulture_Spider_Mine': 13, 'Terran_Nuclear_Missile': 14, 'Terran_Civilian': 15, 'Terran_Siege_Tank_Siege_Mode': 30, 'Terran_Firebat': 32, 'Spell_Scanner_Sweep': 33, 'Terran_Medic': 34, 'Zerg_Larva': 35, 'Zerg_Egg': 36, 'Zerg_Zergling': 37, 'Zerg_Hydralisk': 38, 'Zerg_Ultralisk': 39, 'Zerg_Broodling': 40, 'Zerg_Drone': 41, 'Zerg_Overlord': 42, 'Zerg_Mutalisk': 43, 'Zerg_Guardian': 44, 'Zerg_Queen': 45, 'Zerg_Defiler': 46, 'Zerg_Scourge': 47, 'Zerg_Infested_Terran': 50, 'Terran_Valkyrie': 58, 'Zerg_Cocoon': 59, 'Protoss_Corsair': 60, 'Protoss_Dark_Templar': 61, 'Zerg_Devourer': 62, 'Protoss_Dark_Archon': 63, 'Protoss_Probe': 64, 'Protoss_Zealot': 65, 'Protoss_Dragoon': 66, 'Protoss_High_Templar': 67, 'Protoss_Archon': 68, 'Protoss_Shuttle': 69, 'Protoss_Scout': 70, 'Protoss_Arbiter': 71, 'Protoss_Carrier': 72, 'Protoss_Interceptor': 73, 'Protoss_Reaver': 83, 'Protoss_Observer': 84, 'Protoss_Scarab': 85, 'Critter_Rhynadon': 89, 'Critter_Bengalaas': 90, 'Critter_Scantid': 93, 'Critter_Kakaru': 94, 'Critter_Ragnasaur': 95, 'Critter_Ursadon': 96, 'Zerg_Lurker_Egg': 97, 'Zerg_Lurker': 103, 'Spell_Disruption_Web': 105, 'Terran_Command_Center': 106, 'Terran_Comsat_Station': 107, 'Terran_Nuclear_Silo': 108, 'Terran_Supply_Depot': 109, 'Terran_Refinery': 110, 'Terran_Barracks': 111, 'Terran_Academy': 112, 'Terran_Factory': 113, 'Terran_Starport': 114, 'Terran_Control_Tower': 115, 'Terran_Science_Facility': 116, 'Terran_Covert_Ops': 117, 'Terran_Physics_Lab': 118, 'Terran_Machine_Shop': 120, 'Terran_Engineering_Bay': 122, 'Terran_Armory': 123, 'Terran_Missile_Turret': 124, 'Terran_Bunker': 125, 'Zerg_Infested_Command_Center': 130, 'Zerg_Hatchery': 131, 'Zerg_Lair': 132, 'Zerg_Hive': 133, 'Zerg_Nydus_Canal': 134, 'Zerg_Hydralisk_Den': 135, 'Zerg_Defiler_Mound': 136, 'Zerg_Greater_Spire': 137, 'Zerg_Queens_Nest': 138, 'Zerg_Evolution_Chamber': 139, 'Zerg_Ultralisk_Cavern': 140, 'Zerg_Spire': 141, 'Zerg_Spawning_Pool': 142, 'Zerg_Creep_Colony': 143, 'Zerg_Spore_Colony': 144, 'Zerg_Sunken_Colony': 146, 'Zerg_Extractor': 149, 'Protoss_Nexus': 154, 'Protoss_Robotics_Facility': 155, 'Protoss_Pylon': 156, 'Protoss_Assimilator': 157, 'Protoss_Observatory': 159, 'Protoss_Gateway': 160, 'Protoss_Photon_Cannon': 162, 'Protoss_Citadel_of_Adun': 163, 'Protoss_Cybernetics_Core': 164, 'Protoss_Templar_Archives': 165, 'Protoss_Forge': 166, 'Protoss_Stargate': 167, 'Protoss_Fleet_Beacon': 169, 'Protoss_Arbiter_Tribunal': 170, 'Protoss_Robotics_Support_Bay': 171, 'Protoss_Shield_Battery': 172, 'Resource_Mineral_Field': 176, 'Resource_Mineral_Field_Type_2': 177, 'Resource_Mineral_Field_Type_3': 178, 'Resource_Vespene_Geyser': 188, 'Spell_Dark_Swarm': 202, 'Special_Pit_Door': 207, 'Special_Right_Pit_Door': 208, 'MAX': 233}
