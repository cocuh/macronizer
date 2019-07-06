import abc
import logging
from typing import Dict, List, Optional, Set

from macronizer.consts.input_event_codes import EventType, KeyEventCode, KeyEventValue
from macronizer.pubsub import PublisherMixin, SubscriberMixin
from macronizer.structures import InputEvent, TimeVal

logger = logging.getLogger(__name__)


class KeyboardState:
  pressed_time: Dict[KeyEventCode, TimeVal]

  def __init__(self, monitoring_codes: Optional[List[KeyEventCode]] = None):
    self.monitoring_codes = monitoring_codes
    self.pressed_time = {}

  def on_key(self, event: InputEvent):
    if event.type != EventType.EV_KEY:
      logger.error(f"Invalid event type: {event!r}")
      return

    code: KeyEventCode = KeyEventCode(event.code)
    value: KeyEventValue = KeyEventValue(event.value)

    if self.monitoring_codes is not None \
        and code not in self.monitoring_codes:
      # key code is not monitoring target.
      return

    if value == KeyEventValue.KEYUP:
      self.pressed_time.pop(code, None)
    elif value == KeyEventValue.KEYDOWN:
      self.pressed_time[code] = event.time

  def is_pressing(self, code: KeyEventCode):
    return code in self.pressed_time


class BaseTransformer(
  abc.ABC,
  PublisherMixin[InputEvent], SubscriberMixin[InputEvent]):

  @abc.abstractmethod
  async def run(self) -> None:
    pass


class Transformer(BaseTransformer):
  def __init__(self, modifiers: Set[KeyEventCode] = None):
    super().__init__()
    if modifiers is None:
      modifiers = []
    self.state = KeyboardState(modifiers)

  async def run(self) -> None:
    while True:
      event: InputEvent = await self.queue.get()
      if event.type == EventType.EV_KEY:
        self.state.on_key(event)

      # TODO: write here
      self.publish(event)


class NoOpTransformer(BaseTransformer):
  async def run(self) -> None:
    while True:
      self.publish(await self.queue.get())
