from __future__ import annotations

import ctypes
import time as time_module
from typing import Optional

from macronizer.consts.input_event_codes import EventCode, EventType, EventValue


class TimeVal(ctypes.Structure):
  sec: int
  usec: int

  _fields_ = [
    ('sec', ctypes.c_ulong),
    ('usec', ctypes.c_ulong),
  ]

  @classmethod
  def create(cls, sec: int, usec: int) -> TimeVal:
    return cls(sec, usec)

  @classmethod
  def now(cls):
    timestamp: float = time_module.time()
    timestamp_s: int = int(timestamp)
    timestamp_us: int = int((timestamp - timestamp_s) * 10 ** 6)
    return TimeVal.create(sec=timestamp_s, usec=timestamp_us)

  def delta_usec_from(self, time_val: TimeVal):
    delta_sec = self.sec - time_val.sec
    delta_usec = self.usec - time_val.usec + delta_sec * 10 ** 6
    return delta_usec


class InputEvent(ctypes.Structure):
  time: TimeVal
  type: int
  code: int
  value: int

  _fields_ = [
    ('time', TimeVal),
    ('type', ctypes.c_ushort),
    ('code', ctypes.c_ushort),
    ('value', ctypes.c_uint),
  ]

  @classmethod
  def create(cls, type: EventType, code: EventCode, value: EventValue, time: Optional[TimeVal] = None) -> InputEvent:
    if time is None:
      time = TimeVal.now()
    return cls(time=time, type=type, code=code, value=value)

  def __repr__(self):
    return f'<Event type={self.type:#04x} code={self.code:#06x} value={self.value:#08x} ' \
      f'sec={self.time.sec} usec={self.time.usec}>'


class InputId(ctypes.Structure):
  bustype: int
  vendor: int
  product: int
  version: int
  _fields_ = [
    ('bustype', ctypes.c_uint16),
    ('vendor', ctypes.c_uint16),
    ('product', ctypes.c_uint16),
    ('version', ctypes.c_uint16),
  ]


class UInputUserDev(ctypes.Structure):
  name: bytes
  id: InputId

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
