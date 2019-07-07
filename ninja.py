import asyncio
import logging

from macronizer.consts.input_event_codes import EventType, KeyEventCode
from macronizer.device.input_device import InputDevice
from macronizer.device.uinput_device import UInputDevice
from macronizer.pipeline.transformer import NoOpTransformer

logging.basicConfig(level=logging.DEBUG)

input_device = InputDevice.create_by_id()
noop_transformer = NoOpTransformer()
output_device = UInputDevice.create(support_events={
  EventType.EV_KEY: [
    KeyEventCode.KEY_W,
    KeyEventCode.KEY_A,
    KeyEventCode.KEY_S,
    KeyEventCode.KEY_D,
  ]
})

input_device.add_subscriber(noop_transformer)
noop_transformer.add_subscriber(output_device)

with input_device.grab(), output_device.open():
  loop = asyncio.get_event_loop()

  task_input = input_device.run(loop)
  task_transformer = noop_transformer.run()
  task_output = output_device.run()

  loop.create_task(task_input)
  loop.create_task(task_transformer)
  loop.create_task(task_output)

  try:
    loop.run_forever()
  except KeyboardInterrupt:
    print("exiting...")
    task_input.close()
    task_transformer.close()
    task_output.close()
