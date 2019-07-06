from unittest import TestCase

from macronizer.pubsub import PublisherMixin, SubscriberMixin


class TestPubSub(TestCase):
  def test_it(self):
    publisher = PublisherMixin()
    subscriber1 = SubscriberMixin()
    subscriber2 = SubscriberMixin()

    publisher.add_subscriber(subscriber1)
    publisher.add_subscriber(subscriber2)

    messages = ['ninja', 'youjo', 'samurai']

    for msg in messages:
      publisher.publish(msg)

    self.assertEqual(subscriber1.queue.get_nowait(), 'ninja')
    self.assertEqual(subscriber1.queue.get_nowait(), 'youjo')
    self.assertEqual(subscriber1.queue.get_nowait(), 'samurai')
    self.assertTrue(subscriber1.queue.empty())
    self.assertEqual(subscriber2.queue.get_nowait(), 'ninja')
    self.assertEqual(subscriber2.queue.get_nowait(), 'youjo')
    self.assertEqual(subscriber2.queue.get_nowait(), 'samurai')
    self.assertTrue(subscriber2.queue.empty())
