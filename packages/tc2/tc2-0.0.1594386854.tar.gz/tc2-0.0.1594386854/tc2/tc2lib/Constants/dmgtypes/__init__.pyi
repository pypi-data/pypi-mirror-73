from typing import *
from typing import Iterable as iterable
from typing import Iterator as iterator
from numpy import float64, float32, int32, uint8
import numpy
_Shape = Tuple[int, ...]
__all__  = [
"Concussive",
"Explosive",
"Ignore_Armor",
"Independent",
"Normal",
"ids",
"names"
]
Concussive = 2
Explosive = 1
Ignore_Armor = 4
Independent = 0
Normal = 3
ids = {0: 'Independent', 1: 'Explosive', 2: 'Concussive', 3: 'Normal', 4: 'Ignore_Armor', 5: 'None'}
names = {'Independent': 0, 'Explosive': 1, 'Concussive': 2, 'Normal': 3, 'Ignore_Armor': 4, 'None': 5}
