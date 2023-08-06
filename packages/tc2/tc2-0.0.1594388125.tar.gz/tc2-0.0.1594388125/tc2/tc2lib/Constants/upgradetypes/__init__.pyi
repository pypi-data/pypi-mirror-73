from typing import *
from typing import Iterable as iterable
from typing import Iterator as iterator
from numpy import float64, float32, int32, uint8
import numpy
_Shape = Tuple[int, ...]
__all__  = [
"Adrenal_Glands",
"Anabolic_Synthesis",
"Antennae",
"Apial_Sensors",
"Apollo_Reactor",
"Argus_Jewel",
"Argus_Talisman",
"Caduceus_Reactor",
"Carrier_Capacity",
"Charon_Boosters",
"Chitinous_Plating",
"Colossus_Reactor",
"Gamete_Meiosis",
"Gravitic_Boosters",
"Gravitic_Drive",
"Gravitic_Thrusters",
"Grooved_Spines",
"Ion_Thrusters",
"Khaydarin_Amulet",
"Khaydarin_Core",
"Leg_Enhancements",
"MAX",
"Metabolic_Boost",
"Metasynaptic_Node",
"Moebius_Reactor",
"Muscular_Augments",
"Ocular_Implants",
"Pneumatized_Carapace",
"Protoss_Air_Armor",
"Protoss_Air_Weapons",
"Protoss_Ground_Armor",
"Protoss_Ground_Weapons",
"Protoss_Plasma_Shields",
"Reaver_Capacity",
"Scarab_Damage",
"Sensor_Array",
"Singularity_Charge",
"Terran_Infantry_Armor",
"Terran_Infantry_Weapons",
"Terran_Ship_Plating",
"Terran_Ship_Weapons",
"Terran_Vehicle_Plating",
"Terran_Vehicle_Weapons",
"Titan_Reactor",
"U_238_Shells",
"Unknow",
"Upgrade_60",
"Ventral_Sacs",
"Zerg_Carapace",
"Zerg_Flyer_Attacks",
"Zerg_Flyer_Carapace",
"Zerg_Melee_Attacks",
"Zerg_Missile_Attacks",
"ids",
"names"
]
Adrenal_Glands = 28
Anabolic_Synthesis = 53
Antennae = 25
Apial_Sensors = 41
Apollo_Reactor = 22
Argus_Jewel = 47
Argus_Talisman = 49
Caduceus_Reactor = 51
Carrier_Capacity = 43
Charon_Boosters = 54
Chitinous_Plating = 52
Colossus_Reactor = 23
Gamete_Meiosis = 31
Gravitic_Boosters = 39
Gravitic_Drive = 37
Gravitic_Thrusters = 42
Grooved_Spines = 30
Ion_Thrusters = 17
Khaydarin_Amulet = 40
Khaydarin_Core = 44
Leg_Enhancements = 34
MAX = 63
Metabolic_Boost = 27
Metasynaptic_Node = 32
Moebius_Reactor = 21
Muscular_Augments = 29
Ocular_Implants = 20
Pneumatized_Carapace = 26
Protoss_Air_Armor = 6
Protoss_Air_Weapons = 14
Protoss_Ground_Armor = 5
Protoss_Ground_Weapons = 13
Protoss_Plasma_Shields = 15
Reaver_Capacity = 36
Scarab_Damage = 35
Sensor_Array = 38
Singularity_Charge = 33
Terran_Infantry_Armor = 0
Terran_Infantry_Weapons = 7
Terran_Ship_Plating = 2
Terran_Ship_Weapons = 9
Terran_Vehicle_Plating = 1
Terran_Vehicle_Weapons = 8
Titan_Reactor = 19
U_238_Shells = 16
Unknow = 62
Upgrade_60 = 60
Ventral_Sacs = 24
Zerg_Carapace = 3
Zerg_Flyer_Attacks = 12
Zerg_Flyer_Carapace = 4
Zerg_Melee_Attacks = 10
Zerg_Missile_Attacks = 11
ids = {0: 'Terran_Infantry_Armor', 1: 'Terran_Vehicle_Plating', 2: 'Terran_Ship_Plating', 3: 'Zerg_Carapace', 4: 'Zerg_Flyer_Carapace', 5: 'Protoss_Ground_Armor', 6: 'Protoss_Air_Armor', 7: 'Terran_Infantry_Weapons', 8: 'Terran_Vehicle_Weapons', 9: 'Terran_Ship_Weapons', 10: 'Zerg_Melee_Attacks', 11: 'Zerg_Missile_Attacks', 12: 'Zerg_Flyer_Attacks', 13: 'Protoss_Ground_Weapons', 14: 'Protoss_Air_Weapons', 15: 'Protoss_Plasma_Shields', 16: 'U_238_Shells', 17: 'Ion_Thrusters', 19: 'Titan_Reactor', 20: 'Ocular_Implants', 21: 'Moebius_Reactor', 22: 'Apollo_Reactor', 23: 'Colossus_Reactor', 24: 'Ventral_Sacs', 25: 'Antennae', 26: 'Pneumatized_Carapace', 27: 'Metabolic_Boost', 28: 'Adrenal_Glands', 29: 'Muscular_Augments', 30: 'Grooved_Spines', 31: 'Gamete_Meiosis', 32: 'Metasynaptic_Node', 33: 'Singularity_Charge', 34: 'Leg_Enhancements', 35: 'Scarab_Damage', 36: 'Reaver_Capacity', 37: 'Gravitic_Drive', 38: 'Sensor_Array', 39: 'Gravitic_Boosters', 40: 'Khaydarin_Amulet', 41: 'Apial_Sensors', 42: 'Gravitic_Thrusters', 43: 'Carrier_Capacity', 44: 'Khaydarin_Core', 47: 'Argus_Jewel', 49: 'Argus_Talisman', 51: 'Caduceus_Reactor', 52: 'Chitinous_Plating', 53: 'Anabolic_Synthesis', 54: 'Charon_Boosters', 60: 'Upgrade_60', 61: 'None', 62: 'Unknow', 63: 'MAX'}
names = {'Terran_Infantry_Armor': 0, 'Terran_Vehicle_Plating': 1, 'Terran_Ship_Plating': 2, 'Zerg_Carapace': 3, 'Zerg_Flyer_Carapace': 4, 'Protoss_Ground_Armor': 5, 'Protoss_Air_Armor': 6, 'Terran_Infantry_Weapons': 7, 'Terran_Vehicle_Weapons': 8, 'Terran_Ship_Weapons': 9, 'Zerg_Melee_Attacks': 10, 'Zerg_Missile_Attacks': 11, 'Zerg_Flyer_Attacks': 12, 'Protoss_Ground_Weapons': 13, 'Protoss_Air_Weapons': 14, 'Protoss_Plasma_Shields': 15, 'U_238_Shells': 16, 'Ion_Thrusters': 17, 'Titan_Reactor': 19, 'Ocular_Implants': 20, 'Moebius_Reactor': 21, 'Apollo_Reactor': 22, 'Colossus_Reactor': 23, 'Ventral_Sacs': 24, 'Antennae': 25, 'Pneumatized_Carapace': 26, 'Metabolic_Boost': 27, 'Adrenal_Glands': 28, 'Muscular_Augments': 29, 'Grooved_Spines': 30, 'Gamete_Meiosis': 31, 'Metasynaptic_Node': 32, 'Singularity_Charge': 33, 'Leg_Enhancements': 34, 'Scarab_Damage': 35, 'Reaver_Capacity': 36, 'Gravitic_Drive': 37, 'Sensor_Array': 38, 'Gravitic_Boosters': 39, 'Khaydarin_Amulet': 40, 'Apial_Sensors': 41, 'Gravitic_Thrusters': 42, 'Carrier_Capacity': 43, 'Khaydarin_Core': 44, 'Argus_Jewel': 47, 'Argus_Talisman': 49, 'Caduceus_Reactor': 51, 'Chitinous_Plating': 52, 'Anabolic_Synthesis': 53, 'Charon_Boosters': 54, 'Upgrade_60': 60, 'None': 61, 'Unknow': 62, 'MAX': 63}
