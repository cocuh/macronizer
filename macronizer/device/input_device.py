import asyncio
import contextlib
import fcntl
import logging
import os
import select
from asyncio import AbstractEventLoop
from ctypes import sizeof
from pathlib import Path
from typing import AsyncGenerator, List, Optional, Union

from macronizer.device.structures import InputEvent, InputId

logger = logging.getLogger(__name__)


class InputDevice:
  fd: int
  info: InputId
  name: str

  _partial_read_data: bytes

  def __init__(self, path: Union[Path, str]):
    super().__init__()
    self.fd = os.open(path, os.O_RDWR | os.O_NONBLOCK)
    self.info = self._get_device_info(self.fd)
    self.name = self._get_device_name(self.fd)
    self._partial_read_data = b''

  def read(self) -> List[InputEvent]:
    result = []
    while True:
      data = self._maybe_read_once()
      if data is None:
        # No extra data to read
        return result
      result.append(data)

  async def read_async(self, loop: AbstractEventLoop) \
      -> AsyncGenerator[InputEvent, None, None]:
    while True:
      await self._watch(loop)
      for event in self.read():
        logger.debug(f"{event!r}")
        yield event

  async def _watch(self, loop: AbstractEventLoop):
    future = asyncio.Future()
    loop.add_reader(self.fd, future.set_result, None)
    future.add_done_callback(lambda _: loop.remove_reader(self.fd))
    await future

  def print_event(self):
    while True:
      r, _, _ = select.select([self.fd], [], [])
      for event in self.read():
        print(event)

  def debug(self):
    with self.grab():
      self.print_event()

  def _maybe_read_once(self) -> Optional[InputEvent]:
    bytes_to_read = sizeof(InputEvent) - len(self._partial_read_data)

    try:
      _data = os.read(self.fd, bytes_to_read)
      data: bytes = self._partial_read_data + _data
    except BlockingIOError:
      # No data to read
      return None
    self._partial_read_data = b''

    if len(data) < sizeof(InputEvent):
      assert len(data) == 0, 'if triggered partial read is required'
      self._partial_read_data = data
      return None
    else:
      # len(data) == EventData.size
      return InputEvent.from_buffer_copy(data[:sizeof(InputEvent)])

  @staticmethod
  def _get_device_info(fd: int) -> InputId:
    EVIOCGID = ~int(~0x80084502 & 0xFFFFFFFF)
    # https://elixir.bootlin.com/linux/latest/source/include/uapi/linux/input.h#L129

    value = fcntl.ioctl(fd, EVIOCGID, '\0' * sizeof(InputId))
    info = InputId.from_buffer_copy(value)
    return info

  @staticmethod
  def _get_device_name(fd: int) -> str:
    EVIOCGNAME = ~int(~0x82004506 & 0xFFFFFFFF)
    # https://elixir.bootlin.com/linux/latest/source/include/uapi/linux/input.h#L138

    EVIOCGNAME_BUFFER = '\0' * 512
    name: bytes = fcntl.ioctl(fd, EVIOCGNAME, EVIOCGNAME_BUFFER)
    return name.decode('utf-8').rstrip('\0')

  @classmethod
  def create_by_id(cls, id: str):
    return cls(path=Path('/dev/input/by-id') / id)

  @contextlib.contextmanager
  def grab(self):
    """
    Grab the control of input device.
    """
    self._grab(True)
    yield
    self._grab(False)

  def _grab(self, grab: bool):
    EVIOCGRAB = ~int(~0x40044590 & 0xFFFFFFFF)
    fcntl.ioctl(self.fd, EVIOCGRAB, int(grab))


def __debug():
  global device
  device = InputDevice.create_by_id()
  with device.grab():
    device.print_event()


if __name__ == '__main__':
  __debug()
