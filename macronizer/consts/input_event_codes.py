from enum import IntEnum


# TODO: Migrate this file to Cython file

class EventType(IntEnum):
  """
  https://www.kernel.org/doc/html/v4.17/input/event-codes.html
  linux/input-event-codes.h
  """
  EV_SYN = 0x00
  EV_KEY = 0x01
  EV_REL = 0x02
  EV_ABS = 0x03
  EV_MSC = 0x04
  EV_SW = 0x05
  EV_LED = 0x11
  EV_SND = 0x12
  EV_REP = 0x14
  EV_FF = 0x15
  EV_PWR = 0x16
  EV_FF_STATUS = 0x17
  EV_MAX = 0x1f
  EV_CNT = (EV_MAX + 1)


class EventCode:
  pass


class KeyEventCode(EventCode, IntEnum):
  """
  See linux/input-event-codes.h
  """
  KEY_RESERVED = 0
  KEY_ESC = 1
  KEY_1 = 2
  KEY_2 = 3
  KEY_3 = 4
  KEY_4 = 5
  KEY_5 = 6
  KEY_6 = 7
  KEY_7 = 8
  KEY_8 = 9
  KEY_9 = 10
  KEY_0 = 11
  KEY_MINUS = 12
  KEY_EQUAL = 13
  KEY_BACKSPACE = 14
  KEY_TAB = 15
  KEY_Q = 16
  KEY_W = 17
  KEY_E = 18
  KEY_R = 19
  KEY_T = 20
  KEY_Y = 21
  KEY_U = 22
  KEY_I = 23
  KEY_O = 24
  KEY_P = 25
  KEY_LEFTBRACE = 26
  KEY_RIGHTBRACE = 27
  KEY_ENTER = 28
  KEY_LEFTCTRL = 29
  KEY_A = 30
  KEY_S = 31
  KEY_D = 32
  KEY_F = 33
  KEY_G = 34
  KEY_H = 35
  KEY_J = 36
  KEY_K = 37
  KEY_L = 38
  KEY_SEMICOLON = 39
  KEY_APOSTROPHE = 40
  KEY_GRAVE = 41
  KEY_LEFTSHIFT = 42
  KEY_BACKSLASH = 43
  KEY_Z = 44
  KEY_X = 45
  KEY_C = 46
  KEY_V = 47
  KEY_B = 48
  KEY_N = 49
  KEY_M = 50
  KEY_COMMA = 51
  KEY_DOT = 52
  KEY_SLASH = 53
  KEY_RIGHTSHIFT = 54
  KEY_KPASTERISK = 55
  KEY_LEFTALT = 56
  KEY_SPACE = 57
  KEY_CAPSLOCK = 58
  KEY_F1 = 59
  KEY_F2 = 60
  KEY_F3 = 61
  KEY_F4 = 62
  KEY_F5 = 63
  KEY_F6 = 64
  KEY_F7 = 65
  KEY_F8 = 66
  KEY_F9 = 67
  KEY_F10 = 68
  KEY_NUMLOCK = 69
  KEY_SCROLLLOCK = 70
  KEY_KP7 = 71
  KEY_KP8 = 72
  KEY_KP9 = 73
  KEY_KPMINUS = 74
  KEY_KP4 = 75
  KEY_KP5 = 76
  KEY_KP6 = 77
  KEY_KPPLUS = 78
  KEY_KP1 = 79
  KEY_KP2 = 80
  KEY_KP3 = 81
  KEY_KP0 = 82
  KEY_KPDOT = 83

  KEY_ZENKAKUHANKAKU = 85
  KEY_102ND = 86
  KEY_F11 = 87
  KEY_F12 = 88
  KEY_RO = 89
  KEY_KATAKANA = 90
  KEY_HIRAGANA = 91
  KEY_HENKAN = 92
  KEY_KATAKANAHIRAGANA = 93
  KEY_MUHENKAN = 94
  KEY_KPJPCOMMA = 95
  KEY_KPENTER = 96
  KEY_RIGHTCTRL = 97
  KEY_KPSLASH = 98
  KEY_SYSRQ = 99
  KEY_RIGHTALT = 100
  KEY_LINEFEED = 101
  KEY_HOME = 102
  KEY_UP = 103
  KEY_PAGEUP = 104
  KEY_LEFT = 105
  KEY_RIGHT = 106
  KEY_END = 107
  KEY_DOWN = 108
  KEY_PAGEDOWN = 109
  KEY_INSERT = 110
  KEY_DELETE = 111
  KEY_MACRO = 112
  KEY_MUTE = 113

  BTN_MISC = 0x100
  BTN_0 = 0x100
  BTN_1 = 0x101
  BTN_2 = 0x102
  BTN_3 = 0x103
  BTN_4 = 0x104
  BTN_5 = 0x105
  BTN_6 = 0x106
  BTN_7 = 0x107
  BTN_8 = 0x108
  BTN_9 = 0x109

  BTN_MOUSE = 0x110
  BTN_LEFT = 0x110
  BTN_RIGHT = 0x111
  BTN_MIDDLE = 0x112
  BTN_SIDE = 0x113
  BTN_EXTRA = 0x114
  BTN_FORWARD = 0x115
  BTN_BACK = 0x116
  BTN_TASK = 0x117

  BTN_JOYSTICK = 0x120
  BTN_TRIGGER = 0x120
  BTN_THUMB = 0x121
  BTN_THUMB2 = 0x122
  BTN_TOP = 0x123
  BTN_TOP2 = 0x124
  BTN_PINKIE = 0x125
  BTN_BASE = 0x126
  BTN_BASE2 = 0x127
  BTN_BASE3 = 0x128
  BTN_BASE4 = 0x129
  BTN_BASE5 = 0x12a
  BTN_BASE6 = 0x12b
  BTN_DEAD = 0x12f

  BTN_GAMEPAD = 0x130
  BTN_SOUTH = 0x130
  BTN_A = BTN_SOUTH
  BTN_EAST = 0x131
  BTN_B = BTN_EAST
  BTN_C = 0x132
  BTN_NORTH = 0x133
  BTN_X = BTN_NORTH
  BTN_WEST = 0x134
  BTN_Y = BTN_WEST
  BTN_Z = 0x135
  BTN_TL = 0x136
  BTN_TR = 0x137
  BTN_TL2 = 0x138
  BTN_TR2 = 0x139
  BTN_SELECT = 0x13a
  BTN_START = 0x13b
  BTN_MODE = 0x13c
  BTN_THUMBL = 0x13d
  BTN_THUMBR = 0x13e

  BTN_WHEEL = 0x150
  BTN_GEAR_DOWN = 0x150
  BTN_GEAR_UP = 0x151

  KEY_OK = 0x160
  KEY_SELECT = 0x161

  KEY_FN = 0x1d0
  KEY_FN_ESC = 0x1d1
  KEY_FN_F1 = 0x1d2
  KEY_FN_F2 = 0x1d3
  KEY_FN_F3 = 0x1d4
  KEY_FN_F4 = 0x1d5
  KEY_FN_F5 = 0x1d6
  KEY_FN_F6 = 0x1d7
  KEY_FN_F7 = 0x1d8
  KEY_FN_F8 = 0x1d9
  KEY_FN_F9 = 0x1da
  KEY_FN_F10 = 0x1db
  KEY_FN_F11 = 0x1dc
  KEY_FN_F12 = 0x1dd
  KEY_FN_1 = 0x1de
  KEY_FN_2 = 0x1df
  KEY_FN_D = 0x1e0
  KEY_FN_E = 0x1e1
  KEY_FN_F = 0x1e2
  KEY_FN_S = 0x1e3
  KEY_FN_B = 0x1e4

  KEY_NUMERIC_0 = 0x200 
  KEY_NUMERIC_1 = 0x201 
  KEY_NUMERIC_2 = 0x202
  KEY_NUMERIC_3 = 0x203
  KEY_NUMERIC_4 = 0x204
  KEY_NUMERIC_5 = 0x205
  KEY_NUMERIC_6 = 0x206
  KEY_NUMERIC_7 = 0x207
  KEY_NUMERIC_8 = 0x208
  KEY_NUMERIC_9 = 0x209
  KEY_NUMERIC_STAR = 0x20a
  KEY_NUMERIC_POUND = 0x20b

  KEY_MAX = 0x2ff
  KEY_CNT = (KEY_MAX + 1)


class AbsoluteEventCode(EventCode, IntEnum):
  ABS_X = 0x00
  ABS_Y = 0x01
  ABS_Z = 0x02
  ABS_RX = 0x03
  ABS_RY = 0x04
  ABS_RZ = 0x05
  ABS_THROTTLE = 0x06
  ABS_RUDDER = 0x07
  ABS_WHEEL = 0x08
  ABS_GAS = 0x09
  ABS_BRAKE = 0x0a
  ABS_HAT0X = 0x10
  ABS_HAT0Y = 0x11
  ABS_HAT1X = 0x12
  ABS_HAT1Y = 0x13
  ABS_HAT2X = 0x14
  ABS_HAT2Y = 0x15
  ABS_HAT3X = 0x16
  ABS_HAT3Y = 0x17
  ABS_PRESSURE = 0x18
  ABS_DISTANCE = 0x19
  ABS_TILT_X = 0x1a
  ABS_TILT_Y = 0x1b
  ABS_TOOL_WIDTH = 0x1c

  ABS_VOLUME = 0x20

  ABS_MISC = 0x28


class RelativeEventCode(EventCode, IntEnum):
  REL_X = 0x00
  REL_Y = 0x01
  REL_Z = 0x02
  REL_RX = 0x03
  REL_RY = 0x04
  REL_RZ = 0x05
  REL_HWHEEL = 0x06
  REL_DIAL = 0x07
  REL_WHEEL = 0x08
  REL_MISC = 0x09


class EventValue:
  pass


class KeyEventValue(EventValue, IntEnum):
  """
  Used when the type is EventType.EV_KEY
  """
  KEYUP = 0
  KEYDOWN = 1
  KEYPRESSED = 2
