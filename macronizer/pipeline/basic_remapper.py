import dataclasses
import logging
from typing import Dict, Optional, Set, Tuple

from macronizer.consts.input_event_codes import EventType, KeyEventCode, KeyEventValue
from macronizer.device.structures import InputEvent, TimeVal
from macronizer.pipeline.transformer import BaseTransformer

logger = logging.getLogger(__name__)


class KeyboardState:
  pressed_time: Dict[KeyEventCode, TimeVal]

  def __init__(self, monitoring_codes: Optional[Tuple[KeyEventCode]] = None):
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

  def pressing_keys(self) -> Set[KeyEventCode]:
    return set(self.pressed_time.keys())


Modifiers = Tuple[KeyEventCode]

Rule = Dict[
  Modifiers,
  KeyEventCode,
]


@dataclasses.dataclass
class BasicRemapConfig:
  modifiers: Tuple[KeyEventCode, ...]
  rules: Dict[KeyEventCode, Rule]

  def get_possible_output_keys(self):
    return set(
      code
        for rule in self.rules.values()
        for code in rule.values()
    )


class BasicRemapper(BaseTransformer):
  mapping: BasicRemapConfig

  def __init__(self, mapping: BasicRemapConfig):
    super().__init__()
    self.state = KeyboardState(mapping.modifiers)
    self.mapping = mapping

  async def run(self) -> None:
    while True:
      event: InputEvent = await self.queue.get()
      if event.type != EventType.EV_KEY:
        continue
      self.state.on_key(event)

      self.process(event, self.state.pressing_keys())

  def emit(self, event: InputEvent):
    self.publish(event)

  def process(self, event: InputEvent, modifiers: Set[KeyEventCode]):
    """
    Call self.emit(event) to emit the event
    """
    rule: Rule = self.mapping.rules.get(event.code)
    if rule is None or len(rule) == 0:
      return

    candidates = sorted(
      [
        (
          len(modifiers - set(mod)),
          (mod, remap)
        )
        for mod, remap in rule.items()
        if set(mod) == modifiers or set(mod) in modifiers
      ],
      key=lambda t: t[0],
    )
    if len(candidates) == 0:
      return
    remap: KeyEventCode = candidates[0][1][1]
    self.emit(
      InputEvent.create(
        type=EventType.EV_KEY,
        code=remap,
        value=KeyEventValue(event.value),
      )
    )
