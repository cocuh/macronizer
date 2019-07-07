import abc
from typing import List, Type

from macronizer.consts.input_event_codes import EventCode
from macronizer.device.input_device import InputDevice


class DeviceSetting(abc.ABC):
  @abc.abstractmethod
  @classmethod
  def get_key_code_type(self) -> Type[EventCode]:
    pass

  @abc.abstractmethod
  @classmethod
  def get_input_devices(self) -> List[InputDevice]:
    pass
