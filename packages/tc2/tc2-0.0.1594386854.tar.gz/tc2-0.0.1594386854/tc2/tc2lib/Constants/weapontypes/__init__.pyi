from typing import *
from typing import Iterable as iterable
from typing import Iterator as iterator
from numpy import float64, float32, int32, uint8
import numpy
_Shape = Tuple[int, ...]
__all__  = [
"ATA_Laser_Battery",
"ATA_Laser_Battery_Hero",
"ATA_Laser_Battery_Hyperion",
"ATS_Laser_Battery",
"ATS_Laser_Battery_Hero",
"ATS_Laser_Battery_Hyperion",
"Acid_Spore",
"Acid_Spore_Kukulza",
"Anti_Matter_Missiles",
"Anti_Matter_Missiles_Artanis",
"Anti_Matter_Missiles_Mojo",
"Arclite_Cannon",
"Arclite_Cannon_Edmund_Duke",
"Arclite_Shock_Cannon",
"Arclite_Shock_Cannon_Edmund_Duke",
"Burst_Lasers",
"Burst_Lasers_Tom_Kazansky",
"C_10_Canister_Rifle",
"C_10_Canister_Rifle_Alexei_Stukov",
"C_10_Canister_Rifle_Infested_Duran",
"C_10_Canister_Rifle_Samir_Duran",
"C_10_Canister_Rifle_Sarah_Kerrigan",
"Claws",
"Claws_Devouring_One",
"Claws_Infested_Kerrigan",
"Consume",
"Corrosive_Acid",
"Dark_Swarm",
"Disruption_Web",
"Dual_Photon_Blasters",
"Dual_Photon_Blasters_Artanis",
"Dual_Photon_Blasters_Mojo",
"EMP_Shockwave",
"Ensnare",
"Feedback",
"Flame_Thrower",
"Flame_Thrower_Gui_Montag",
"Flame_Thrower_Wall_Trap",
"Fragmentation_Grenade",
"Fragmentation_Grenade_Jim_Raynor",
"Fusion_Cutter",
"Gauss_Rifle",
"Gauss_Rifle_Jim_Raynor",
"Gemini_Missiles",
"Gemini_Missiles_Tom_Kazansky",
"Glave_Wurm",
"Glave_Wurm_Kukulza",
"Halo_Rockets",
"Hellfire_Missile_Pack",
"Hellfire_Missile_Pack_Alan_Schezar",
"Hellfire_Missile_Pack_Floor_Trap",
"Hellfire_Missile_Pack_Wall_Trap",
"Independant_Laser_Battery",
"Irradiate",
"Kaiser_Blades",
"Kaiser_Blades_Torrasque",
"Lockdown",
"Longbolt_Missile",
"MAX",
"Maelstrom",
"Mind_Control",
"Needle_Spines",
"Needle_Spines_Hunter_Killer",
"Neutron_Flare",
"Nuclear_Strike",
"Optical_Flare",
"Parasite",
"Particle_Beam",
"Phase_Disruptor",
"Phase_Disruptor_Cannon",
"Phase_Disruptor_Cannon_Danimoth",
"Phase_Disruptor_Fenix",
"Plague",
"Platform_Laser_Battery",
"Psi_Assault",
"Psi_Blades",
"Psi_Blades_Fenix",
"Psionic_Shockwave",
"Psionic_Shockwave_TZ_Archon",
"Psionic_Storm",
"Pulse_Cannon",
"Restoration",
"STA_Photon_Cannon",
"STS_Photon_Cannon",
"Scarab",
"Seeker_Spores",
"Spawn_Broodlings",
"Spider_Mines",
"Spines",
"Stasis_Field",
"Subterranean_Spines",
"Subterranean_Tentacle",
"Suicide_Infested_Terran",
"Suicide_Scourge",
"Toxic_Spores",
"Twin_Autocannons",
"Twin_Autocannons_Alan_Schezar",
"Twin_Autocannons_Floor_Trap",
"Unknown",
"Warp_Blades",
"Warp_Blades_Hero",
"Warp_Blades_Zeratul",
"Yamato_Gun",
"ids",
"names"
]
ATA_Laser_Battery = 20
ATA_Laser_Battery_Hero = 22
ATA_Laser_Battery_Hyperion = 24
ATS_Laser_Battery = 19
ATS_Laser_Battery_Hero = 21
ATS_Laser_Battery_Hyperion = 23
Acid_Spore = 46
Acid_Spore_Kukulza = 47
Anti_Matter_Missiles = 74
Anti_Matter_Missiles_Artanis = 115
Anti_Matter_Missiles_Mojo = 76
Arclite_Cannon = 11
Arclite_Cannon_Edmund_Duke = 12
Arclite_Shock_Cannon = 27
Arclite_Shock_Cannon_Edmund_Duke = 28
Burst_Lasers = 16
Burst_Lasers_Tom_Kazansky = 18
C_10_Canister_Rifle = 2
C_10_Canister_Rifle_Alexei_Stukov = 116
C_10_Canister_Rifle_Infested_Duran = 113
C_10_Canister_Rifle_Samir_Duran = 112
C_10_Canister_Rifle_Sarah_Kerrigan = 3
Claws = 35
Claws_Devouring_One = 36
Claws_Infested_Kerrigan = 37
Consume = 61
Corrosive_Acid = 104
Dark_Swarm = 59
Disruption_Web = 101
Dual_Photon_Blasters = 73
Dual_Photon_Blasters_Artanis = 114
Dual_Photon_Blasters_Mojo = 75
EMP_Shockwave = 33
Ensnare = 58
Feedback = 106
Flame_Thrower = 25
Flame_Thrower_Gui_Montag = 26
Flame_Thrower_Wall_Trap = 98
Fragmentation_Grenade = 4
Fragmentation_Grenade_Jim_Raynor = 5
Fusion_Cutter = 13
Gauss_Rifle = 0
Gauss_Rifle_Jim_Raynor = 1
Gemini_Missiles = 15
Gemini_Missiles_Tom_Kazansky = 17
Glave_Wurm = 48
Glave_Wurm_Kukulza = 49
Halo_Rockets = 103
Hellfire_Missile_Pack = 8
Hellfire_Missile_Pack_Alan_Schezar = 10
Hellfire_Missile_Pack_Floor_Trap = 99
Hellfire_Missile_Pack_Wall_Trap = 97
Independant_Laser_Battery = 93
Irradiate = 34
Kaiser_Blades = 40
Kaiser_Blades_Torrasque = 41
Lockdown = 32
Longbolt_Missile = 29
MAX = 132
Maelstrom = 108
Mind_Control = 105
Needle_Spines = 38
Needle_Spines_Hunter_Killer = 39
Neutron_Flare = 100
Nuclear_Strike = 31
Optical_Flare = 107
Parasite = 56
Particle_Beam = 62
Phase_Disruptor = 66
Phase_Disruptor_Cannon = 77
Phase_Disruptor_Cannon_Danimoth = 78
Phase_Disruptor_Fenix = 67
Plague = 60
Platform_Laser_Battery = 92
Psi_Assault = 69
Psi_Blades = 64
Psi_Blades_Fenix = 65
Psionic_Shockwave = 70
Psionic_Shockwave_TZ_Archon = 71
Psionic_Storm = 84
Pulse_Cannon = 79
Restoration = 102
STA_Photon_Cannon = 81
STS_Photon_Cannon = 80
Scarab = 82
Seeker_Spores = 52
Spawn_Broodlings = 57
Spider_Mines = 6
Spines = 43
Stasis_Field = 83
Subterranean_Spines = 109
Subterranean_Tentacle = 53
Suicide_Infested_Terran = 54
Suicide_Scourge = 55
Toxic_Spores = 42
Twin_Autocannons = 7
Twin_Autocannons_Alan_Schezar = 9
Twin_Autocannons_Floor_Trap = 96
Unknown = 131
Warp_Blades = 111
Warp_Blades_Hero = 86
Warp_Blades_Zeratul = 85
Yamato_Gun = 30
ids = {0: 'Gauss_Rifle', 1: 'Gauss_Rifle_Jim_Raynor', 2: 'C_10_Canister_Rifle', 3: 'C_10_Canister_Rifle_Sarah_Kerrigan', 4: 'Fragmentation_Grenade', 5: 'Fragmentation_Grenade_Jim_Raynor', 6: 'Spider_Mines', 7: 'Twin_Autocannons', 8: 'Hellfire_Missile_Pack', 9: 'Twin_Autocannons_Alan_Schezar', 10: 'Hellfire_Missile_Pack_Alan_Schezar', 11: 'Arclite_Cannon', 12: 'Arclite_Cannon_Edmund_Duke', 13: 'Fusion_Cutter', 15: 'Gemini_Missiles', 16: 'Burst_Lasers', 17: 'Gemini_Missiles_Tom_Kazansky', 18: 'Burst_Lasers_Tom_Kazansky', 19: 'ATS_Laser_Battery', 20: 'ATA_Laser_Battery', 21: 'ATS_Laser_Battery_Hero', 22: 'ATA_Laser_Battery_Hero', 23: 'ATS_Laser_Battery_Hyperion', 24: 'ATA_Laser_Battery_Hyperion', 25: 'Flame_Thrower', 26: 'Flame_Thrower_Gui_Montag', 27: 'Arclite_Shock_Cannon', 28: 'Arclite_Shock_Cannon_Edmund_Duke', 29: 'Longbolt_Missile', 30: 'Yamato_Gun', 31: 'Nuclear_Strike', 32: 'Lockdown', 33: 'EMP_Shockwave', 34: 'Irradiate', 35: 'Claws', 36: 'Claws_Devouring_One', 37: 'Claws_Infested_Kerrigan', 38: 'Needle_Spines', 39: 'Needle_Spines_Hunter_Killer', 40: 'Kaiser_Blades', 41: 'Kaiser_Blades_Torrasque', 42: 'Toxic_Spores', 43: 'Spines', 46: 'Acid_Spore', 47: 'Acid_Spore_Kukulza', 48: 'Glave_Wurm', 49: 'Glave_Wurm_Kukulza', 52: 'Seeker_Spores', 53: 'Subterranean_Tentacle', 54: 'Suicide_Infested_Terran', 55: 'Suicide_Scourge', 56: 'Parasite', 57: 'Spawn_Broodlings', 58: 'Ensnare', 59: 'Dark_Swarm', 60: 'Plague', 61: 'Consume', 62: 'Particle_Beam', 64: 'Psi_Blades', 65: 'Psi_Blades_Fenix', 66: 'Phase_Disruptor', 67: 'Phase_Disruptor_Fenix', 69: 'Psi_Assault', 70: 'Psionic_Shockwave', 71: 'Psionic_Shockwave_TZ_Archon', 73: 'Dual_Photon_Blasters', 74: 'Anti_Matter_Missiles', 75: 'Dual_Photon_Blasters_Mojo', 76: 'Anti_Matter_Missiles_Mojo', 77: 'Phase_Disruptor_Cannon', 78: 'Phase_Disruptor_Cannon_Danimoth', 79: 'Pulse_Cannon', 80: 'STS_Photon_Cannon', 81: 'STA_Photon_Cannon', 82: 'Scarab', 83: 'Stasis_Field', 84: 'Psionic_Storm', 85: 'Warp_Blades_Zeratul', 86: 'Warp_Blades_Hero', 92: 'Platform_Laser_Battery', 93: 'Independant_Laser_Battery', 96: 'Twin_Autocannons_Floor_Trap', 97: 'Hellfire_Missile_Pack_Wall_Trap', 98: 'Flame_Thrower_Wall_Trap', 99: 'Hellfire_Missile_Pack_Floor_Trap', 100: 'Neutron_Flare', 101: 'Disruption_Web', 102: 'Restoration', 103: 'Halo_Rockets', 104: 'Corrosive_Acid', 105: 'Mind_Control', 106: 'Feedback', 107: 'Optical_Flare', 108: 'Maelstrom', 109: 'Subterranean_Spines', 111: 'Warp_Blades', 112: 'C_10_Canister_Rifle_Samir_Duran', 113: 'C_10_Canister_Rifle_Infested_Duran', 114: 'Dual_Photon_Blasters_Artanis', 115: 'Anti_Matter_Missiles_Artanis', 116: 'C_10_Canister_Rifle_Alexei_Stukov', 130: 'None', 131: 'Unknown', 132: 'MAX'}
names = {'Gauss_Rifle': 0, 'Gauss_Rifle_Jim_Raynor': 1, 'C_10_Canister_Rifle': 2, 'C_10_Canister_Rifle_Sarah_Kerrigan': 3, 'Fragmentation_Grenade': 4, 'Fragmentation_Grenade_Jim_Raynor': 5, 'Spider_Mines': 6, 'Twin_Autocannons': 7, 'Hellfire_Missile_Pack': 8, 'Twin_Autocannons_Alan_Schezar': 9, 'Hellfire_Missile_Pack_Alan_Schezar': 10, 'Arclite_Cannon': 11, 'Arclite_Cannon_Edmund_Duke': 12, 'Fusion_Cutter': 13, 'Gemini_Missiles': 15, 'Burst_Lasers': 16, 'Gemini_Missiles_Tom_Kazansky': 17, 'Burst_Lasers_Tom_Kazansky': 18, 'ATS_Laser_Battery': 19, 'ATA_Laser_Battery': 20, 'ATS_Laser_Battery_Hero': 21, 'ATA_Laser_Battery_Hero': 22, 'ATS_Laser_Battery_Hyperion': 23, 'ATA_Laser_Battery_Hyperion': 24, 'Flame_Thrower': 25, 'Flame_Thrower_Gui_Montag': 26, 'Arclite_Shock_Cannon': 27, 'Arclite_Shock_Cannon_Edmund_Duke': 28, 'Longbolt_Missile': 29, 'Yamato_Gun': 30, 'Nuclear_Strike': 31, 'Lockdown': 32, 'EMP_Shockwave': 33, 'Irradiate': 34, 'Claws': 35, 'Claws_Devouring_One': 36, 'Claws_Infested_Kerrigan': 37, 'Needle_Spines': 38, 'Needle_Spines_Hunter_Killer': 39, 'Kaiser_Blades': 40, 'Kaiser_Blades_Torrasque': 41, 'Toxic_Spores': 42, 'Spines': 43, 'Acid_Spore': 46, 'Acid_Spore_Kukulza': 47, 'Glave_Wurm': 48, 'Glave_Wurm_Kukulza': 49, 'Seeker_Spores': 52, 'Subterranean_Tentacle': 53, 'Suicide_Infested_Terran': 54, 'Suicide_Scourge': 55, 'Parasite': 56, 'Spawn_Broodlings': 57, 'Ensnare': 58, 'Dark_Swarm': 59, 'Plague': 60, 'Consume': 61, 'Particle_Beam': 62, 'Psi_Blades': 64, 'Psi_Blades_Fenix': 65, 'Phase_Disruptor': 66, 'Phase_Disruptor_Fenix': 67, 'Psi_Assault': 69, 'Psionic_Shockwave': 70, 'Psionic_Shockwave_TZ_Archon': 71, 'Dual_Photon_Blasters': 73, 'Anti_Matter_Missiles': 74, 'Dual_Photon_Blasters_Mojo': 75, 'Anti_Matter_Missiles_Mojo': 76, 'Phase_Disruptor_Cannon': 77, 'Phase_Disruptor_Cannon_Danimoth': 78, 'Pulse_Cannon': 79, 'STS_Photon_Cannon': 80, 'STA_Photon_Cannon': 81, 'Scarab': 82, 'Stasis_Field': 83, 'Psionic_Storm': 84, 'Warp_Blades_Zeratul': 85, 'Warp_Blades_Hero': 86, 'Platform_Laser_Battery': 92, 'Independant_Laser_Battery': 93, 'Twin_Autocannons_Floor_Trap': 96, 'Hellfire_Missile_Pack_Wall_Trap': 97, 'Flame_Thrower_Wall_Trap': 98, 'Hellfire_Missile_Pack_Floor_Trap': 99, 'Neutron_Flare': 100, 'Disruption_Web': 101, 'Restoration': 102, 'Halo_Rockets': 103, 'Corrosive_Acid': 104, 'Mind_Control': 105, 'Feedback': 106, 'Optical_Flare': 107, 'Maelstrom': 108, 'Subterranean_Spines': 109, 'Warp_Blades': 111, 'C_10_Canister_Rifle_Samir_Duran': 112, 'C_10_Canister_Rifle_Infested_Duran': 113, 'Dual_Photon_Blasters_Artanis': 114, 'Anti_Matter_Missiles_Artanis': 115, 'C_10_Canister_Rifle_Alexei_Stukov': 116, 'None': 130, 'Unknown': 131, 'MAX': 132}
