"""
Ideas:
- use up/down to cycle between brightness
- use left/right to cycle between patterns
- think about how to "play" multiple patterns
    maybe use adam's code with generators as inspiration
    check out examples from Adam https://github.com/agfor/PyCon2019/blob/master/Attendee_Examples/music_and_lights_using_generators.py
- find code with various patterns in backup
"""

import board
import neopixel
import random
import time

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.color_packet import ColorPacket
from adafruit_bluefruit_connect.button_packet import ButtonPacket

ble = BLERadio()
uart_service = UARTService()
advertisement = ProvideServicesAdvertisement(uart_service)



num_pixels = 5

pixels = neopixel.NeoPixel(
    board.D12,
    num_pixels,
    # brightness=1,
)
onboard_pixel = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.01)

print("Starting...")

def chance(odds):
    return random.random() < odds

# odds_to_trigger = 0.25
odds_to_trigger = 0.3



color_list = [(0, 0, 255), (0, 255, 255), (255, 255, 0), (255, 0, 255)]
led_color_list = []
brightness_list = []

brightness_list = [0.0] * num_pixels
led_color_list = [0] * num_pixels

def pattern(loop_sleep=0.2):
    # Display random pattern with jewel tones
    for pixel in range(num_pixels):
        is_triggered = chance(odds_to_trigger)
        if is_triggered:
            brightness_list[pixel] = 1.0
            led_color_list[pixel] = random.randint(0, len(color_list) - 1)
        else:
            b = brightness_list[pixel] * 0.5
            brightness_list[pixel] = b
            this_color = color_list[led_color_list[pixel]]
            r = int(b * this_color[0])
            g = int(b * this_color[1])
            b = int(b * this_color[2])

            pixels[pixel] = (r, g, b)
            # print("setting pixel %s" % pixel)

        # time.sleep(random.random() * 0.1 + 0.01)
        time.sleep(random.random() * 0.065 + 0.01)

    # time.sleep(0.02)
    time.sleep(loop_sleep)

while True:
    print("at ntop of loop")

    # Advertise when not connected.
    ble.start_advertising(advertisement)

    while not ble.connected:
        pattern()
        onboard_pixel.fill((128, 0, 0))
        # for val in (0, 64, 0, 128, 0, 192, 0, 255):
            # onboard_pixel.fill((val, 0, 0))
            # time.sleep(0.5)
    while ble.connected:
        # onboard_pixel.fill((0, 255, 0))
        pattern(loop_sleep=0)
        # print("BLE connected")
        packet = Packet.from_stream(uart_service)
        if isinstance(packet, ColorPacket):
            print("Color Picked", packet.color)
            # onboard_pixel.fill(packet.color)
            pixels.fill((0, 0, 0))
            color_list = [packet.color] * 4
            onboard_pixel.fill(packet.color)

        if isinstance(packet, ButtonPacket):
            if packet.pressed:
                if packet.button == ButtonPacket.BUTTON_1:
                    # The 1 button was pressed.
                    print("1 button pressed!")
                    # reset colors
                    color_list = [(0, 0, 255), (0, 255, 255), (255, 255, 0), (255, 0, 255)]
                elif packet.button == ButtonPacket.UP:
                    # The UP button was pressed.
                    print("UP button pressed!")


