import abc
import logging
from asyncio import AbstractEventLoop
from typing import List

from macronizer.device.input_device import InputDevice
from macronizer.device.structures import InputEvent
from macronizer.device.uinput_device import UInputDevice
from macronizer.pipeline.pubsub import PublisherMixin, SubscriberMixin

logger = logging.getLogger(__name__)


class SourceNode(PublisherMixin[InputEvent]):
  def __init__(self, input_devices: List[InputDevice]):
    assert len(input_devices) == 1, "This feature is not implemented. Welcome PR!"
    self.input_devices = input_devices
    super(SourceNode, self).__init__()

  async def run(self, loop: AbstractEventLoop) -> None:
    reader = self.input_devices[0].read_async(loop)
    while True:
      event = await reader.asend(None)
      self.publish(event)


class DestNode(SubscriberMixin[InputEvent]):
  def __init__(self, output_device: UInputDevice):
    super(DestNode, self).__init__()
    self.output_device = output_device

  async def run(self) -> None:
    while True:
      event = await self.queue.get()
      self.output_device.write(event)
      self.output_device.sync()


class BaseTransformer(
  PublisherMixin[InputEvent], SubscriberMixin[InputEvent], abc.ABC):
  def __init__(self):
    super(BaseTransformer, self).__init__()

  @abc.abstractmethod
  async def run(self) -> None:
    pass


class NoOpTransformer(BaseTransformer):
  async def run(self) -> None:
    while True:
      event = await self.queue.get()
      logger.debug(f"NoOpTransformer: {event!r}")
      self.publish(event)
