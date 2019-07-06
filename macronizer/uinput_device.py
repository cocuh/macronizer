import contextlib
import fcntl
import logging
import os
import time
from pathlib import Path
from typing import Dict, List, Union

from macronizer.consts.input_event_codes import (
  AbsoluteEventCode,
  EventCode,
  KeyEventCode,
  KeyEventValue,
  RelativeEventCode
)
from macronizer.pubsub import SubscriberMixin
from macronizer.structures import EventType, InputEvent, InputId, UInputUserDev

logger = logging.getLogger(__name__)


class UInputDevice(SubscriberMixin):
  def __init__(self, path: Union[str, Path]):
    super().__init__()
    self.fd = os.open(path, os.O_RDWR | os.O_NONBLOCK)

  def write(self, event: InputEvent):
    logger.debug(f"UInputWrite: {event!r}")
    os.write(self.fd, bytes(event))

  def sync(self):
    os.write(self.fd, InputEvent.create(EventType.EV_SYN, 0, 0))

  async def run(self):
    while True:
      event = await self.queue.get()
      self.write(event)
      if self.queue.empty():
        self.sync()

  @contextlib.contextmanager
  def open(self):
    self._create_device(self.fd)
    yield
    self._destroy_device(self.fd)

  @classmethod
  def create(cls,
      path="/dev/uinput", device_name: str = "PyKeyPad",
      support_events: Dict[EventType, List[EventCode]] = None
  ):
    input_id = InputId(
      bustype=0x03,
      vendor=0x01,
      pid=0x01,
      version=0x01,
    )
    settings = UInputUserDev.create(
      name=device_name.encode('utf-8'),
      id=input_id,
    )

    device = cls(path=path)
    os.write(device.fd, bytes(settings))
    cls._enable_event_support(device.fd, event_dict=support_events)
    return device

  @classmethod
  def _create_device(cls, fd: int):
    UI_DEV_CREATE = 0x5501
    return fcntl.ioctl(fd, UI_DEV_CREATE)

  @classmethod
  def _destroy_device(cls, fd: int):
    UI_DEV_DESTROY = 0x5502
    return fcntl.ioctl(fd, UI_DEV_DESTROY)

  @classmethod
  def _enable_event_support(cls, fd: int, event_dict: Dict[EventType, List[EventCode]] = None):
    """
    Change uinput setting to handle applied event type and event code. If event_dict is not given, all event type/code 
    for EV_KEY, EV_REL and EV_ABS will be initialized. 
    """

    if event_dict is None:
      event_dict = {
        EventType.EV_KEY: list(set(KeyEventCode)),
        EventType.EV_ABS: list(AbsoluteEventCode),
        EventType.EV_REL: list(RelativeEventCode),
      }

    UI_SET_EVBIT = 0x40045564
    for event_type, event_codes in event_dict.items():
      fcntl.ioctl(fd, UI_SET_EVBIT, event_type)
      for code in event_codes:
        try:
          fcntl.ioctl(fd, UI_SET_EVBIT + event_type, code)
        except OSError as e:
          logger.error(f'Invalid argument:\n  EventType: {event_type}\n  Code: {code}', exc_info=True)


def __debug():
  youjo_codes = [
    KeyEventCode.KEY_Y,
    KeyEventCode.KEY_O,
    KeyEventCode.KEY_U,
    KeyEventCode.KEY_J,
    KeyEventCode.KEY_O,
  ]
  support_events = {
    EventType.EV_KEY: list(set(youjo_codes))
  }
  device = UInputDevice.create(support_events=support_events)
  with device.open():
    time.sleep(1)
    for key_code in youjo_codes:
      device.write(InputEvent.create(EventType.EV_KEY, key_code, KeyEventValue.KEYDOWN))
      device.write(InputEvent.create(EventType.EV_KEY, key_code, KeyEventValue.KEYUP))
    device.sync()


if __name__ == '__main__':
  __debug()
