from typing import *
from typing import Iterable as iterable
from typing import Iterator as iterator
from numpy import float64, float32, int32, uint8
import numpy
_Shape = Tuple[int, ...]
__all__  = [
"Archon_Warp",
"Burrowing",
"Cloaking_Field",
"Consume",
"Dark_Archon_Meld",
"Dark_Swarm",
"Defensive_Matrix",
"Disruption_Web",
"EMP_Shockwave",
"Ensnare",
"Feedback",
"Hallucination",
"Healing",
"Infestation",
"Irradiate",
"Lockdown",
"Lurker_Aspect",
"MAX",
"Maelstrom",
"Mind_Control",
"Nuclear_Strike",
"Optical_Flare",
"Parasite",
"Personnel_Cloaking",
"Plague",
"Psionic_Storm",
"Recall",
"Restoration",
"Scanner_Sweep",
"Spawn_Broodlings",
"Spider_Mines",
"Stasis_Field",
"Stim_Packs",
"Tank_Siege_Mode",
"Unknown",
"Unused_26",
"Unused_33",
"Yamato_Gun",
"ids",
"names"
]
Archon_Warp = 23
Burrowing = 11
Cloaking_Field = 9
Consume = 16
Dark_Archon_Meld = 28
Dark_Swarm = 14
Defensive_Matrix = 6
Disruption_Web = 25
EMP_Shockwave = 2
Ensnare = 17
Feedback = 29
Hallucination = 20
Healing = 34
Infestation = 12
Irradiate = 7
Lockdown = 1
Lurker_Aspect = 32
MAX = 47
Maelstrom = 31
Mind_Control = 27
Nuclear_Strike = 45
Optical_Flare = 30
Parasite = 18
Personnel_Cloaking = 10
Plague = 15
Psionic_Storm = 19
Recall = 21
Restoration = 24
Scanner_Sweep = 4
Spawn_Broodlings = 13
Spider_Mines = 3
Stasis_Field = 22
Stim_Packs = 0
Tank_Siege_Mode = 5
Unknown = 46
Unused_26 = 26
Unused_33 = 33
Yamato_Gun = 8
ids = {0: 'Stim_Packs', 1: 'Lockdown', 2: 'EMP_Shockwave', 3: 'Spider_Mines', 4: 'Scanner_Sweep', 5: 'Tank_Siege_Mode', 6: 'Defensive_Matrix', 7: 'Irradiate', 8: 'Yamato_Gun', 9: 'Cloaking_Field', 10: 'Personnel_Cloaking', 11: 'Burrowing', 12: 'Infestation', 13: 'Spawn_Broodlings', 14: 'Dark_Swarm', 15: 'Plague', 16: 'Consume', 17: 'Ensnare', 18: 'Parasite', 19: 'Psionic_Storm', 20: 'Hallucination', 21: 'Recall', 22: 'Stasis_Field', 23: 'Archon_Warp', 24: 'Restoration', 25: 'Disruption_Web', 26: 'Unused_26', 27: 'Mind_Control', 28: 'Dark_Archon_Meld', 29: 'Feedback', 30: 'Optical_Flare', 31: 'Maelstrom', 32: 'Lurker_Aspect', 33: 'Unused_33', 34: 'Healing', 44: 'None', 45: 'Nuclear_Strike', 46: 'Unknown', 47: 'MAX'}
names = {'Stim_Packs': 0, 'Lockdown': 1, 'EMP_Shockwave': 2, 'Spider_Mines': 3, 'Scanner_Sweep': 4, 'Tank_Siege_Mode': 5, 'Defensive_Matrix': 6, 'Irradiate': 7, 'Yamato_Gun': 8, 'Cloaking_Field': 9, 'Personnel_Cloaking': 10, 'Burrowing': 11, 'Infestation': 12, 'Spawn_Broodlings': 13, 'Dark_Swarm': 14, 'Plague': 15, 'Consume': 16, 'Ensnare': 17, 'Parasite': 18, 'Psionic_Storm': 19, 'Hallucination': 20, 'Recall': 21, 'Stasis_Field': 22, 'Archon_Warp': 23, 'Restoration': 24, 'Disruption_Web': 25, 'Unused_26': 26, 'Mind_Control': 27, 'Dark_Archon_Meld': 28, 'Feedback': 29, 'Optical_Flare': 30, 'Maelstrom': 31, 'Lurker_Aspect': 32, 'Unused_33': 33, 'Healing': 34, 'None': 44, 'Nuclear_Strike': 45, 'Unknown': 46, 'MAX': 47}
