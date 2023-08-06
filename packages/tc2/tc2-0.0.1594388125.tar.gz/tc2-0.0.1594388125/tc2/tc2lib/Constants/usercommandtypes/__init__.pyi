from typing import *
from typing import Iterable as iterable
from typing import Iterator as iterator
from numpy import float64, float32, int32, uint8
import numpy
_Shape = Tuple[int, ...]
__all__  = [
"Move_Screen_Down",
"Move_Screen_Left",
"Move_Screen_Right",
"Move_Screen_To_Pos",
"Move_Screen_Up",
"Right_Click",
"USER_COMMAND_END",
"ids",
"names"
]
Move_Screen_Down = 1
Move_Screen_Left = 2
Move_Screen_Right = 3
Move_Screen_To_Pos = 4
Move_Screen_Up = 0
Right_Click = 5
USER_COMMAND_END = 6
ids = {0: 'Move_Screen_Up', 1: 'Move_Screen_Down', 2: 'Move_Screen_Left', 3: 'Move_Screen_Right', 4: 'Move_Screen_To_Pos', 5: 'Right_Click', 6: 'USER_COMMAND_END'}
names = {'Move_Screen_Up': 0, 'Move_Screen_Down': 1, 'Move_Screen_Left': 2, 'Move_Screen_Right': 3, 'Move_Screen_To_Pos': 4, 'Right_Click': 5, 'USER_COMMAND_END': 6}
