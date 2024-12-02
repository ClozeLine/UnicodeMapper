import json
import keyboard
import time

from GetResourcePath import get_resource_path


class ShortcutHandler:
    def __init__(self, mappings):
        self.mappings = mappings
        self.sequence = []
        self.alt_key_pressed = False

    def on_key_event(self, event):

        if event.name == "alt" and event.event_type == "down" and not self.alt_key_pressed:
            self.alt_key_pressed = True
            self.sequence = []
        elif event.name == "alt" and event.event_type == "up":
            self.alt_key_pressed = False

            if self.sequence:
                try:
                    code = "".join(self.sequence)

                    if code in self.mappings:
                        keyboard.release('alt')
                        time.sleep(0.025)
                        keyboard.write(self.mappings[code], delay=0.1)
                except ValueError:
                    pass
            self.sequence = []
        elif self.alt_key_pressed and event.event_type == 'down' and event.name.isdigit():
            self.sequence.append(event.name)


def main():
    json_mappings_path = get_resource_path(filename="Mappings.json")
    with open(json_mappings_path, "r", encoding="utf-8") as f:
        shortcut_mappings = json.load(f)

    handler = ShortcutHandler(mappings=shortcut_mappings)
    keyboard.hook(handler.on_key_event)
    keyboard.wait("esc")


if __name__ == "__main__":
    main()
