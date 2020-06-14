"""
Copyright 2020 Nina Zakharenko

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
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
)
onboard_pixel = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.01)

print("Starting...")

def chance(odds):
    return random.random() < odds

odds_to_trigger = 0.3

color_list = [(0, 0, 255), (0, 255, 255), (255, 255, 0), (255, 0, 255)]
led_color_list = []
brightness_list = []

brightness_list = [0.0] * num_pixels
led_color_list = [0] * num_pixels

def pattern():
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
        time.sleep(random.random() * 0.065 + 0.01)

    time.sleep(random.random() * 0.02 + 0.01)

while True:
    # Advertise when not connected.
    ble.start_advertising(advertisement)

    while not ble.connected:
        pattern()
        onboard_pixel.fill((128, 0, 0))

    ble.stop_advertising()

    while ble.connected:
        pattern()
        if uart_service.in_waiting:
            packet = Packet.from_stream(uart_service)

            if isinstance(packet, ColorPacket):
                print("Color Picked", packet.color)
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