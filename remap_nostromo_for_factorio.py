import asyncio
import logging

from macronizer.consts.input_event_codes import EventType, KeyEventCode
from macronizer.device.uinput_device import UInputDevice
from macronizer.device_config.razer import RazerNostromo
from macronizer.pipeline.pipeline import DestNode, SourceNode
from macronizer.pipeline.remapper import RemapConfig, Remapper

logging.basicConfig(level=logging.DEBUG)

Code = RazerNostromo.KeyCode
modifiers = [
  Code.KEY_LEFT,
  Code.KEY_RIGHT,
  Code.KEY_UP,
  Code.KEY_DOWN,
]

KEY_SHIFT = KeyEventCode.KEY_LEFTSHIFT
KEY_CTRL = KeyEventCode.KEY_LEFTCTRL

rules = {
  (): {
    Code.KEY_01: KeyEventCode.KEY_Q,
    Code.KEY_02: KeyEventCode.BTN_LEFT,
    Code.KEY_03: KeyEventCode.KEY_W,
    Code.KEY_04: KeyEventCode.BTN_RIGHT,
    Code.KEY_05: KeyEventCode.KEY_R,

    Code.KEY_06: KEY_CTRL,
    Code.KEY_07: KeyEventCode.KEY_A,
    Code.KEY_08: KeyEventCode.KEY_S,
    Code.KEY_09: KeyEventCode.KEY_D,
    Code.KEY_10: KeyEventCode.KEY_F,

    Code.KEY_11: KeyEventCode.KEY_ESC,
    Code.KEY_12: KeyEventCode.KEY_T,
    Code.KEY_13: None,
    Code.KEY_14: KeyEventCode.KEY_E,
    Code.KEY_15: KeyEventCode.KEY_SPACE,

    Code.KEY_SMALL: KEY_SHIFT
  },
  (Code.KEY_LEFT): {
    Code.KEY_01: KeyEventCode.KEY_1,
    Code.KEY_02: KeyEventCode.KEY_2,
    Code.KEY_03: KeyEventCode.KEY_3,
    Code.KEY_04: KeyEventCode.KEY_4,
    Code.KEY_05: KeyEventCode.KEY_5,

    Code.KEY_06: KeyEventCode.KEY_6,
    Code.KEY_07: KeyEventCode.KEY_7,
    Code.KEY_08: KeyEventCode.KEY_8,
    Code.KEY_09: KeyEventCode.KEY_9,
    Code.KEY_10: KeyEventCode.KEY_0,
  },
  (Code.KEY_RIGHT): {
    Code.KEY_01: (KEY_SHIFT, KeyEventCode.KEY_1),
    Code.KEY_02: (KEY_SHIFT, KeyEventCode.KEY_2),
    Code.KEY_03: (KEY_SHIFT, KeyEventCode.KEY_3),
    Code.KEY_04: (KEY_SHIFT, KeyEventCode.KEY_4),
    Code.KEY_05: (KEY_SHIFT, KeyEventCode.KEY_5),

    Code.KEY_06: (KEY_SHIFT, KeyEventCode.KEY_6),
    Code.KEY_07: (KEY_SHIFT, KeyEventCode.KEY_7),
    Code.KEY_08: (KEY_SHIFT, KeyEventCode.KEY_8),
    Code.KEY_09: (KEY_SHIFT, KeyEventCode.KEY_9),
    Code.KEY_10: (KEY_SHIFT, KeyEventCode.KEY_0),
  },
}


def main():
  input_device = RazerNostromo.get_input_devices()[0]
  source_node = SourceNode([input_device])
  config = RemapConfig(modifiers, rules)
  remap_node = Remapper(config)
  output_device = UInputDevice.create(
    support_events={
      EventType.EV_KEY: list(config.get_possible_output_keys()),
    },
  )
  dest_node = DestNode(output_device)

  source_node.add_subscriber(remap_node)
  remap_node.add_subscriber(dest_node)

  with input_device.grab(), output_device.open():
    loop = asyncio.get_event_loop()

    coros = [
      source_node.run(loop),
      remap_node.run(),
      dest_node.run(),
    ]
    for c in coros:
      loop.create_task(c)

    try:
      loop.run_forever()
    except KeyboardInterrupt:
      pass
    finally:
      loop.run_until_complete(loop.shutdown_asyncgens())


if __name__ == '__main__':
  main()
