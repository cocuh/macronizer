from __future__ import annotations

import ctypes
import time as time_module
from typing import Optional

from macronizer.consts.input_event_codes import EventCode, EventType, EventValue


class TimeVal(ctypes.Structure):
  _fields_ = [
    ('sec', ctypes.c_ulong),
    ('usec', ctypes.c_ulong),
  ]

  @classmethod
  def create(cls, sec: int, usec: int) -> TimeVal:
    return cls(sec, usec)


class InputEvent(ctypes.Structure):
  _fields_ = [
    ('time', TimeVal),
    ('type', ctypes.c_ushort),
    ('code', ctypes.c_ushort),
    ('value', ctypes.c_uint),
  ]

  @classmethod
  def create(cls, type: EventType, code: EventCode, value: EventValue, time: Optional[TimeVal] = None) -> InputEvent:
    if time is None:
      timestamp: float = time_module.time()
      timestamp_s: int = int(timestamp)
      timestamp_us: int = int((timestamp - timestamp_s) * 1000000)
      time = TimeVal.create(sec=timestamp_s, usec=timestamp_us)
    return cls(time=time, type=type, code=code, value=value)

  def __repr__(self):
    return f'<Event type={self.type:#04x} code={self.code:#06x} value={self.value:#08x} ' \
      f'sec={self.time.sec} usec={self.time.usec}>'


class InputId(ctypes.Structure):
  _fields_ = [
    ('bustype', ctypes.c_uint16),
    ('vendor', ctypes.c_uint16),
    ('product', ctypes.c_uint16),
    ('version', ctypes.c_uint16),
  ]


class UInputUserDev(ctypes.Structure):
  _fields_ = [
    ('name', ctypes.c_char * 80),
    ('id', InputId),
    ('ff_effects_max', ctypes.c_uint32),
    ('absmax', ctypes.c_int32 * 64),
    ('absmin', ctypes.c_int32 * 64),
    ('absfuzz', ctypes.c_int32 * 64),
    ('absflat', ctypes.c_int32 * 64),
  ]

  @classmethod
  def create(cls, name: bytes, id: InputId):
    Int32Array64 = ctypes.c_int32 * 64
    zeros = Int32Array64(*[0 for _ in range(64)])
    return cls(
      name=name,
      id=id,
      ff_effects_max=0x0,
      absmax=zeros,
      absmin=zeros,
      absfuzz=zeros,
      absflat=zeros,
    )
