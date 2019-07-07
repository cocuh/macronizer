import abc
import logging

from macronizer.device.structures import InputEvent
from macronizer.pipeline.pubsub import PublisherMixin, SubscriberMixin

logger = logging.getLogger(__name__)



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
