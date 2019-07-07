from enum import IntEnum
from typing import List, Type

from macronizer.consts.input_event_codes import EventCode, KeyEventCode
from macronizer.device.input_device import InputDevice
from macronizer.device_config.base import DeviceConfig


class RazerNostromo(DeviceConfig):
  class KeyCode(EventCode, IntEnum):
    KEY_01 = KeyEventCode.KEY_TAB
    KEY_02 = KeyEventCode.KEY_Q
    KEY_03 = KeyEventCode.KEY_W
    KEY_04 = KeyEventCode.KEY_E
    KEY_05 = KeyEventCode.KEY_R

    KEY_06 = KeyEventCode.KEY_CAPSLOCK
    KEY_07 = KeyEventCode.KEY_A
    KEY_08 = KeyEventCode.KEY_S
    KEY_09 = KeyEventCode.KEY_D
    KEY_10 = KeyEventCode.KEY_F

    KEY_11 = KeyEventCode.KEY_LEFTSHIFT
    KEY_12 = KeyEventCode.KEY_Z
    KEY_13 = KeyEventCode.KEY_X
    KEY_14 = KeyEventCode.KEY_C

    KEY_15 = KeyEventCode.KEY_SPACE

    KEY_SMALL = KeyEventCode.KEY_LEFTALT

    KEY_UP = KeyEventCode.KEY_UP
    KEY_DOWN = KeyEventCode.KEY_DOWN
    KEY_RIGHT = KeyEventCode.KEY_RIGHT
    KEY_LEFT = KeyEventCode.KEY_LEFT

  @classmethod
  def get_key_code_type(self) -> Type[EventCode]:
    return self.KeyCode

  @classmethod
  def get_input_devices(self) -> List[InputDevice]:
    return [
      InputDevice.create_by_id(id='usb-Razer_Razer_Nostromo-event-kbd')
    ]
