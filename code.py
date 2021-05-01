"""
The MIT License

Copyright (c) 2021 Nina Zakharenko and contributors

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import random
import time

import board
import neopixel
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_bluefruit_connect.button_packet import ButtonPacket
from adafruit_bluefruit_connect.color_packet import ColorPacket
from adafruit_bluefruit_connect.packet import Packet
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.sparklepulse import SparklePulse
from adafruit_led_animation.color import (AMBER, JADE, MAGENTA, ORANGE, PURPLE,
                                          WHITE, RED, GREEN)
from adafruit_led_animation.sequence import AnimationSequence

ble = BLERadio()
uart_service = UARTService()
advertisement = ProvideServicesAdvertisement(uart_service)

num_pixels = 5

pixels = neopixel.NeoPixel(board.D12, num_pixels, brightness=0.5, auto_write=False)
onboard_pixel = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.01)

print("Starting...")


blink = Blink(pixels, speed=0.5, color=JADE)
colorcycle = ColorCycle(pixels, speed=0.4, colors=[MAGENTA, ORANGE])
comet = Comet(pixels, speed=0.15, color=PURPLE, tail_length=5, bounce=True)
chase = Chase(pixels, speed=0.15, size=3, spacing=6, color=WHITE)
pulse = Pulse(pixels, speed=0.15, period=2, color=PURPLE)
sparkle = Sparkle(pixels, speed=0.1, color=PURPLE, num_sparkles=10)
solid = Solid(pixels, color=JADE)
rainbow = Rainbow(pixels, speed=0.1, period=2)
sparkle_pulse = SparklePulse(
    pixels, speed=0.1, period=20, color=JADE, min_intensity=0.2, max_intensity=0.6
)
rainbow_comet = RainbowComet(pixels, speed=0.12, tail_length=10, bounce=True)
rainbow_chase = RainbowChase(pixels, speed=0.1, size=3, spacing=2, step=8)
rainbow_sparkle = RainbowSparkle(pixels, speed=0.1, num_sparkles=15)


animations = AnimationSequence(
    comet,
    chase,
    pulse,
    sparkle_pulse,
    rainbow_comet,
    auto_clear=True,
)

anim_list = [
    comet,
    chase,
    pulse,
    sparkle_pulse,
    rainbow_comet,
]


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


def print_cycle_complete(animation_object):
    random_color = color_list[random.randint(0, len(color_list) - 1)]
    animation_object.color = random_color


pulse.add_cycle_complete_receiver(print_cycle_complete)

selected_color = None

brightness_buttons = (ButtonPacket.BUTTON_1, ButtonPacket.BUTTON_2, ButtonPacket.BUTTON_3, ButtonPacket.BUTTON_4)
speed_buttons = (ButtonPacket.DOWN, ButtonPacket.UP)
pattern_buttons = (ButtonPacket.LEFT, ButtonPacket.RIGHT)


while True:
    ble.start_advertising(advertisement)  # Send advertisement before connection starts
    

    # Wait for a Bluetooth connection, play an animation with random colors.
    while not ble.connected:
        onboard_pixel.fill(RED)
        animations.animate()
        
        if animations.current_animation != pulse:
            random_color = color_list[random.randint(0, len(color_list) - 1)]
            animations.color = random_color

    while ble.connected:
        onboard_pixel.fill(GREEN)
        animations.animate()
        random_color = color_list[random.randint(0, len(color_list) - 1)]
        if animations.current_animation != pulse:
            animations.color = selected_color or random_color
        
        if uart_service.in_waiting:  # Get a Bluetooth Packet if one is sent
            packet = Packet.from_stream(uart_service)

            if isinstance(packet, ColorPacket):
                print("Color Picked", packet.color)
                pixels.fill((0, 0, 0))
                color_list = [packet.color] * 4
                selected_color = packet.color
                onboard_pixel.fill(packet.color)

            if isinstance(packet, ButtonPacket):
                if packet.pressed:
                    # if packet.button == ButtonPacket.BUTTON_1:
                    #     # The 1 button was pressed.
                    #     print("Resetting colors. (1 button pressed)")
                    #     # reset colors
                    #     color_list = [
                    #         (0, 0, 255),
                    #         (0, 255, 255),
                    #         (255, 255, 0),
                    #         (255, 0, 255),
                    #     ]
                    #     selected_color = None
                    if packet.button == ButtonPacket.RIGHT:
                        animations.next()
                        print(
                            "Selecting next animation: ",
                            animations.current_animation.__class__.__name__,
                        )
                        print("Speed is:", animations.current_animation.speed)
                    elif packet.button == ButtonPacket.DOWN:
                        print("Speeding up.")
                        new_speed = animations.current_animation.speed + 0.025
                        for animation in anim_list:
                            animation.speed = new_speed
                        print("New speed is", new_speed)
                    elif packet.button == ButtonPacket.UP:
                        print("Slowing down.")
                        current_speed = animations.current_animation.speed
                        new_speed = max(0.05, current_speed - 0.025)
                        for animation in anim_list:
                            animation.speed = new_speed
                        print("New speed is", new_speed)
                    elif packet.button in brightness_buttons:
                        print("Adjusting Brightness")
                        if packet.button == ButtonPacket.BUTTON_1:
                            pixels.brightness = 0.1
                        elif packet.button == ButtonPacket.BUTTON_2:
                            pixels.brightness = 0.3
                        elif packet.button == ButtonPacket.BUTTON_3:
                            pixels.brightness = 0.5
                        elif packet.button == ButtonPacket.BUTTON_4:
                            pixels.brightness = 0.8
