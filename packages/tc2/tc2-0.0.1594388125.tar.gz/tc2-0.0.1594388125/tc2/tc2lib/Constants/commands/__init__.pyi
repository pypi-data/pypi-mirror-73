from typing import *
from typing import Iterable as iterable
from typing import Iterator as iterator
from numpy import float64, float32, int32, uint8
import numpy
_Shape = Tuple[int, ...]
__all__  = [
"MAX",
"command_openbw",
"command_unit",
"command_unit_protected",
"command_user",
"draw_circle",
"draw_line",
"draw_text",
"draw_text_screen",
"draw_unit_circle",
"draw_unit_line",
"draw_unit_pos_line",
"exit_process",
"ids",
"map_hack",
"names",
"noop",
"quit",
"request_image",
"restart",
"set_blocking",
"set_cmd_optim",
"set_combine_frames",
"set_frameskip",
"set_gui",
"set_log",
"set_map",
"set_max_frame_time_ms",
"set_multi",
"set_speed"
]
MAX = 27
command_openbw = 19
command_unit = 16
command_unit_protected = 17
command_user = 18
draw_circle = 23
draw_line = 20
draw_text = 25
draw_text_screen = 26
draw_unit_circle = 24
draw_unit_line = 21
draw_unit_pos_line = 22
exit_process = 4
ids = {0: 'quit', 1: 'restart', 2: 'map_hack', 3: 'request_image', 4: 'exit_process', 5: 'noop', 6: 'set_speed', 7: 'set_log', 8: 'set_gui', 9: 'set_frameskip', 10: 'set_cmd_optim', 11: 'set_combine_frames', 12: 'set_map', 13: 'set_multi', 14: 'set_blocking', 15: 'set_max_frame_time_ms', 16: 'command_unit', 17: 'command_unit_protected', 18: 'command_user', 19: 'command_openbw', 20: 'draw_line', 21: 'draw_unit_line', 22: 'draw_unit_pos_line', 23: 'draw_circle', 24: 'draw_unit_circle', 25: 'draw_text', 26: 'draw_text_screen', 27: 'MAX'}
map_hack = 2
names = {'quit': 0, 'restart': 1, 'map_hack': 2, 'request_image': 3, 'exit_process': 4, 'noop': 5, 'set_speed': 6, 'set_log': 7, 'set_gui': 8, 'set_frameskip': 9, 'set_cmd_optim': 10, 'set_combine_frames': 11, 'set_map': 12, 'set_multi': 13, 'set_blocking': 14, 'set_max_frame_time_ms': 15, 'command_unit': 16, 'command_unit_protected': 17, 'command_user': 18, 'command_openbw': 19, 'draw_line': 20, 'draw_unit_line': 21, 'draw_unit_pos_line': 22, 'draw_circle': 23, 'draw_unit_circle': 24, 'draw_text': 25, 'draw_text_screen': 26, 'MAX': 27}
noop = 5
quit = 0
request_image = 3
restart = 1
set_blocking = 14
set_cmd_optim = 10
set_combine_frames = 11
set_frameskip = 9
set_gui = 8
set_log = 7
set_map = 12
set_max_frame_time_ms = 15
set_multi = 13
set_speed = 6
