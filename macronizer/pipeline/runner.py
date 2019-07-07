import asyncio
import logging

from macronizer.consts.input_event_codes import EventType, KeyEventCode
from macronizer.device.input_device import InputDevice
from macronizer.device.uinput_device import UInputDevice
from macronizer.pipeline.key_remapper import RemapConfig, Remapper

logging.basicConfig(level=logging.DEBUG)


def get_factorio_remap_config():
  rules = {
    KeyEventCode.KEY_TAB: KeyEventCode.KEY_1,
    KeyEventCode.KEY_Q: KeyEventCode.KEY_2,
    KeyEventCode.KEY_W: KeyEventCode.KEY_W,
    KeyEventCode.KEY_E: KeyEventCode.KEY_3,
    KeyEventCode.KEY_R: KeyEventCode.KEY_R,

    KeyEventCode.KEY_CAPSLOCK: KeyEventCode.KEY_4,
    KeyEventCode.KEY_A: KeyEventCode.KEY_A,
    KeyEventCode.KEY_S: KeyEventCode.KEY_S,
    KeyEventCode.KEY_D: KeyEventCode.KEY_D,
    KeyEventCode.KEY_F: KeyEventCode.KEY_5,

    KeyEventCode.KEY_LEFTSHIFT: KeyEventCode.KEY_ESC,
    KeyEventCode.KEY_Z: KeyEventCode.KEY_F,
    KeyEventCode.KEY_X: KeyEventCode.KEY_P,
    KeyEventCode.KEY_C: KeyEventCode.KEY_LEFTCTRL,

    KeyEventCode.KEY_LEFT: KeyEventCode.BTN_LEFT,
    KeyEventCode.KEY_RIGHT: KeyEventCode.BTN_RIGHT,
    KeyEventCode.KEY_UP: KeyEventCode.KEY_T,
    KeyEventCode.KEY_DOWN: KeyEventCode.KEY_E,

    KeyEventCode.KEY_SPACE: KeyEventCode.KEY_SPACE,

    KeyEventCode.KEY_LEFTALT: KeyEventCode.KEY_LEFTSHIFT,
  }
  return RemapConfig(
    modifiers=(),
    rules={
      k: {(): v}
      for k, v in rules.items()
    },
  )


def run():
  config = get_factorio_remap_config()

  input_device = InputDevice.create_by_id()
  remapper = Remapper(config)
  output_device = UInputDevice.create(support_events={
    EventType.EV_KEY: config.get_possible_output_keys()
  })

  input_device.add_subscriber(remapper)
  remapper.add_subscriber(output_device)

  with input_device.grab(), output_device.open():
    loop = asyncio.get_event_loop()

    co_input = input_device.run(loop)
    co_remapper = remapper.run()
    co_output = output_device.run()

    loop.create_task(co_input)
    loop.create_task(co_remapper)
    loop.create_task(co_output)

    try:
      loop.run_forever()
    except KeyboardInterrupt:
      print("exiting...")
      co_input.close()
      co_remapper.close()
      co_output.close()


if __name__ == '__main__':
  run()
