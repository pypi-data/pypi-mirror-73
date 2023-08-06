import time

from tuyaha.devices.base import TuyaDevice


class TuyaSwitch(TuyaDevice):
    def state(self):
        state = self.data.get("state")
        if state is None:
            return None
        return state

    def turn_on(self):
        success, _response = self.api.device_control(self.obj_id, "turnOnOff", {"value": "1"})

        if success:
            self.data["state"] = True

    def turn_off(self):
        success, _response = self.api.device_control(self.obj_id, "turnOnOff", {"value": "0"})

        if success:
            self.data["state"] = False

    # workaround for https://github.com/PaulAnnekov/tuyaha/issues/3
    def update(self):
        """Avoid get cache value after control."""
        time.sleep(0.5)
        devices = self.api.discovery()
        if not devices:
            return
        for device in devices:
            if device["id"] == self.obj_id:
                self.data = device["data"]
                return True
