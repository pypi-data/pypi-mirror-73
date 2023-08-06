from typing import *
from typing import Iterable as iterable
from typing import Iterator as iterator
from numpy import float64, float32, int32, uint8
import numpy
_Shape = Tuple[int, ...]
__all__  = [
"Independent",
"Large",
"Medium",
"Small",
"ids",
"names"
]
Independent = 0
Large = 3
Medium = 2
Small = 1
ids = {0: 'Independent', 1: 'Small', 2: 'Medium', 3: 'Large'}
names = {'Independent': 0, 'Small': 1, 'Medium': 2, 'Large': 3}
