import abc
from typing import List, Type

from macronizer.consts.input_event_codes import EventCode
from macronizer.device.input_device import InputDevice


class DeviceConfig(abc.ABC):

  @classmethod
  @abc.abstractmethod
  def get_key_code_type(self) -> Type[EventCode]:
    pass

  @classmethod
  @abc.abstractmethod
  def get_input_devices(self) -> List[InputDevice]:
    pass
