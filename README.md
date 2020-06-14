## About

This code is for an LED jacket with 3D printed embellishments, built by following a guide by Sophy Wong in her book [Wearable Tech projects](https://www.raspberrypi.org/blog/create-wearable-tech-projects-with-sophy-wong/).

The code is run on an [Adafruit Feather nRF52840 Express](https://www.adafruit.com/product/4062) with Bluetooth.

The color of the default pattern can be changed by connecting to the board with a phone running [Adafruit's Bluefruit LE Connect App](https://learn.adafruit.com/bluefruit-le-connect) for iOS or Android. Sending a color will change the hue of the running pattern. 

The generative pattern was written in collaboration with [@jacobjoaquin](https://github.com/jacobjoaquin). 

## Photo

![](https://user-images.githubusercontent.com/2030983/84581729-4a843000-ad99-11ea-8282-ba67f90bb705.jpg)

## Future Plans

Currently the LED pattern runs quite slowly, likely because the code is always listening for Bluetooth packets. 

I'd like to try using the new [CircuitPython LED Animation library](https://github.com/adafruit/Adafruit_CircuitPython_LED_Animation), or potentially a cooperative multitasking approach using generators as outlined by Adam Forsyth in his [June 2020 Chicago Python talk](https://www.youtube.com/watch?v=g6dGfJ8oCqg).

Additionally, it would be nice to include an OLED feather wing display to display text status updates and add further interactivity using the onboard buttons.