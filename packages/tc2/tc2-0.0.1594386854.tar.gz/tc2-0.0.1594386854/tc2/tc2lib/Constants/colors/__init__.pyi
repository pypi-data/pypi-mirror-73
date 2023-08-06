from typing import *
from typing import Iterable as iterable
from typing import Iterator as iterator
from numpy import float64, float32, int32, uint8
import numpy
_Shape = Tuple[int, ...]
__all__  = [
"Black",
"Blue",
"Brown",
"Cyan",
"Green",
"Grey",
"Orange",
"Purple",
"Red",
"Teal",
"White",
"Yellow",
"ids",
"names"
]
Black = 0
Blue = 165
Brown = 19
Cyan = 128
Green = 117
Grey = 74
Orange = -179
Purple = 164
Red = 111
Teal = 159
White = 255
Yellow = 135
ids = {0: 'Black', 19: 'Brown', 74: 'Grey', 111: 'Red', 117: 'Green', 128: 'Cyan', 135: 'Yellow', 159: 'Teal', 164: 'Purple', 165: 'Blue', -179: 'Orange', 255: 'White'}
names = {'Black': 0, 'Brown': 19, 'Grey': 74, 'Red': 111, 'Green': 117, 'Cyan': 128, 'Yellow': 135, 'Teal': 159, 'Purple': 164, 'Blue': 165, 'Orange': -179, 'White': 255}
