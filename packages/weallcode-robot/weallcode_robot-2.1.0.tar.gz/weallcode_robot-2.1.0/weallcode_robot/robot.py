import asyncio
import paho.mqtt.client as mqtt
import requests
import time

DOMAIN = "robot-hub.danielmconrad.com"
PORT   = 1883
USER   = "commander"
PASS   = "locutusofborg"

class Robot:
    def __init__(
        self,
        name=None,
        domain=DOMAIN,
        left_mod=1.0,
        right_mod=1.0,
        verbose=False,
    ):
        self.domain = domain
        self.commands = []
        self.left_mod = left_mod
        self.name = name
        self.right_mod = right_mod
        self.verbose = verbose
        self.client = mqtt.Client()
        self.client.username_pw_set(USER, PASS)
        self.client.connect(DOMAIN, PORT)

    # Public

    # Wheels have been temporarily reversed until the board code is updated.
    # Left = right, Right = left, etc etc.
    def wheels(self, left, right):
        l = round(left * self.left_mod)
        r = round(right * self.right_mod)
        self._queue("w=%d,%d" % (l, r))

    def stop(self):
        self.wheels(0, 0)

    def led(self, r, g, b):
        self._queue("l=%d,%d,%d" % (r, g, b))

    def buzzer(self, note=1000, duty_cycle=512):
        self._queue("b=%d,%d" % (note, duty_cycle))

    def buzzer_off(self):
        self._queue("b=off")

    def sleep(self, t):
        self._queue("s=%d" % (t * 1000))

    def done(self):
        self._clean_and_send_commands()

    # Private

    def _clean_and_send_commands(self):
        self.stop()
        self.led(0, 0, 0)
        self.buzzer_off()
        self._send_commands()

    def _get_topic(self):
        return "robot/%s/command" % self.name

    def _queue(self, message):
        self.commands.append(message)

    def _send_commands(self):
        body = bytearray("\r\n".join(self.commands), 'utf-8')

        if len(body) > 2000:
            return print("Too many instructions.")

        if self.verbose:
            print(body)

        self.client.publish(self._get_topic(), body)
