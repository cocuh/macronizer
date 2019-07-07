from __future__ import annotations

import asyncio
from typing import Generic, List, TypeVar

T = TypeVar('T')


class PublisherMixin(Generic[T]):
  _subscribers: List[SubscriberMixin[T]]

  def __init__(self):
    super(PublisherMixin, self).__init__()
    self._subscribers = []

  def add_subscriber(self, subscriber: SubscriberMixin[T]):
    self._subscribers.append(subscriber)

  def publish(self, message: T):
    for sub in self._subscribers:
      sub.enqueue(message)


class SubscriberMixin(Generic[T]):
  queue: asyncio.Queue[T]

  def __init__(self):
    super(SubscriberMixin, self).__init__()
    self.queue = asyncio.Queue()

  def enqueue(self, message: T):
    self.queue.put_nowait(message)
