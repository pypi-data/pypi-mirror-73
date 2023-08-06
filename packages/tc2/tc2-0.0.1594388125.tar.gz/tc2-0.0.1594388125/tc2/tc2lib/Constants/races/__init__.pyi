from typing import *
from typing import Iterable as iterable
from typing import Iterator as iterator
from numpy import float64, float32, int32, uint8
import numpy
_Shape = Tuple[int, ...]
__all__  = [
"MAX",
"Other",
"Protoss",
"Random",
"Select",
"Terran",
"Unknown",
"Unused",
"Zerg",
"ids",
"names"
]
MAX = 9
Other = 3
Protoss = 2
Random = 6
Select = 5
Terran = 1
Unknown = 8
Unused = 4
Zerg = 0
ids = {0: 'Zerg', 1: 'Terran', 2: 'Protoss', 3: 'Other', 4: 'Unused', 5: 'Select', 6: 'Random', 7: 'None', 8: 'Unknown', 9: 'MAX'}
names = {'Zerg': 0, 'Terran': 1, 'Protoss': 2, 'Other': 3, 'Unused': 4, 'Select': 5, 'Random': 6, 'None': 7, 'Unknown': 8, 'MAX': 9}
