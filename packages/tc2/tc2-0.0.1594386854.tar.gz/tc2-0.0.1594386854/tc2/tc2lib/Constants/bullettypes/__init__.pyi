from typing import *
from typing import Iterable as iterable
from typing import Iterator as iterator
from numpy import float64, float32, int32, uint8
import numpy
_Shape = Tuple[int, ...]
__all__  = [
"ATS_ATA_Laser_Battery",
"Acid_Spore",
"Anti_Matter_Missile",
"Arclite_Shock_Cannon_Hit",
"Burst_Lasers",
"C_10_Canister_Rifle_Hit",
"Consume",
"Corrosive_Acid_Hit",
"Corrosive_Acid_Shot",
"Dual_Photon_Blasters_Hit",
"EMP_Missile",
"Ensnare",
"Fragmentation_Grenade",
"Fusion_Cutter_Hit",
"Gauss_Rifle_Hit",
"Gemini_Missiles",
"Glave_Wurm",
"Halo_Rockets",
"Invisible",
"Longbolt_Missile",
"MAX",
"Melee",
"Needle_Spine_Hit",
"Neutron_Flare",
"Optical_Flare_Grenade",
"Particle_Beam_Hit",
"Phase_Disruptor",
"Plague_Cloud",
"Plasma_Drip_Unused",
"Psionic_Shockwave_Hit",
"Psionic_Storm",
"Pulse_Cannon",
"Queen_Spell_Carrier",
"STA_STS_Cannon_Overlay",
"Seeker_Spores",
"Subterranean_Spines",
"Sunken_Colony_Tentacle",
"Unknown",
"Unused_Lockdown",
"Venom_Unused",
"Yamato_Gun",
"ids",
"names"
]
ATS_ATA_Laser_Battery = 148
Acid_Spore = 163
Anti_Matter_Missile = 154
Arclite_Shock_Cannon_Hit = 150
Burst_Lasers = 149
C_10_Canister_Rifle_Hit = 143
Consume = 169
Corrosive_Acid_Hit = 205
Corrosive_Acid_Shot = 204
Dual_Photon_Blasters_Hit = 152
EMP_Missile = 151
Ensnare = 170
Fragmentation_Grenade = 145
Fusion_Cutter_Hit = 141
Gauss_Rifle_Hit = 142
Gemini_Missiles = 144
Glave_Wurm = 165
Halo_Rockets = 202
Invisible = 172
Longbolt_Missile = 146
MAX = 211
Melee = 0
Needle_Spine_Hit = 171
Neutron_Flare = 206
Optical_Flare_Grenade = 201
Particle_Beam_Hit = 153
Phase_Disruptor = 159
Plague_Cloud = 168
Plasma_Drip_Unused = 164
Psionic_Shockwave_Hit = 156
Psionic_Storm = 157
Pulse_Cannon = 155
Queen_Spell_Carrier = 167
STA_STS_Cannon_Overlay = 160
Seeker_Spores = 166
Subterranean_Spines = 203
Sunken_Colony_Tentacle = 161
Unknown = 210
Unused_Lockdown = 147
Venom_Unused = 162
Yamato_Gun = 158
ids = {0: 'Melee', 141: 'Fusion_Cutter_Hit', 142: 'Gauss_Rifle_Hit', 143: 'C_10_Canister_Rifle_Hit', 144: 'Gemini_Missiles', 145: 'Fragmentation_Grenade', 146: 'Longbolt_Missile', 147: 'Unused_Lockdown', 148: 'ATS_ATA_Laser_Battery', 149: 'Burst_Lasers', 150: 'Arclite_Shock_Cannon_Hit', 151: 'EMP_Missile', 152: 'Dual_Photon_Blasters_Hit', 153: 'Particle_Beam_Hit', 154: 'Anti_Matter_Missile', 155: 'Pulse_Cannon', 156: 'Psionic_Shockwave_Hit', 157: 'Psionic_Storm', 158: 'Yamato_Gun', 159: 'Phase_Disruptor', 160: 'STA_STS_Cannon_Overlay', 161: 'Sunken_Colony_Tentacle', 162: 'Venom_Unused', 163: 'Acid_Spore', 164: 'Plasma_Drip_Unused', 165: 'Glave_Wurm', 166: 'Seeker_Spores', 167: 'Queen_Spell_Carrier', 168: 'Plague_Cloud', 169: 'Consume', 170: 'Ensnare', 171: 'Needle_Spine_Hit', 172: 'Invisible', 201: 'Optical_Flare_Grenade', 202: 'Halo_Rockets', 203: 'Subterranean_Spines', 204: 'Corrosive_Acid_Shot', 205: 'Corrosive_Acid_Hit', 206: 'Neutron_Flare', 209: 'None', 210: 'Unknown', 211: 'MAX'}
names = {'Melee': 0, 'Fusion_Cutter_Hit': 141, 'Gauss_Rifle_Hit': 142, 'C_10_Canister_Rifle_Hit': 143, 'Gemini_Missiles': 144, 'Fragmentation_Grenade': 145, 'Longbolt_Missile': 146, 'Unused_Lockdown': 147, 'ATS_ATA_Laser_Battery': 148, 'Burst_Lasers': 149, 'Arclite_Shock_Cannon_Hit': 150, 'EMP_Missile': 151, 'Dual_Photon_Blasters_Hit': 152, 'Particle_Beam_Hit': 153, 'Anti_Matter_Missile': 154, 'Pulse_Cannon': 155, 'Psionic_Shockwave_Hit': 156, 'Psionic_Storm': 157, 'Yamato_Gun': 158, 'Phase_Disruptor': 159, 'STA_STS_Cannon_Overlay': 160, 'Sunken_Colony_Tentacle': 161, 'Venom_Unused': 162, 'Acid_Spore': 163, 'Plasma_Drip_Unused': 164, 'Glave_Wurm': 165, 'Seeker_Spores': 166, 'Queen_Spell_Carrier': 167, 'Plague_Cloud': 168, 'Consume': 169, 'Ensnare': 170, 'Needle_Spine_Hit': 171, 'Invisible': 172, 'Optical_Flare_Grenade': 201, 'Halo_Rockets': 202, 'Subterranean_Spines': 203, 'Corrosive_Acid_Shot': 204, 'Corrosive_Acid_Hit': 205, 'Neutron_Flare': 206, 'None': 209, 'Unknown': 210, 'MAX': 211}
