## About

This code is for an LED jacket with 3D printed embellishments, built by following a guide by Sophy Wong in her book [Wearable Tech projects](https://www.raspberrypi.org/blog/create-wearable-tech-projects-with-sophy-wong/).

The code targets an [Adafruit Feather nRF52840 Express](https://www.adafruit.com/product/4062) with Bluetooth running CircuitPython 5.3.0.

The color of the default pattern can be changed by connecting to the board with a phone running [Adafruit's Bluefruit LE Connect App](https://learn.adafruit.com/bluefruit-le-connect) for iOS or Android. Sending a color will change the hue of the running pattern. 

The generative pattern was written in collaboration with [@jacobjoaquin](https://github.com/jacobjoaquin). 

## Preview

![](https://user-images.githubusercontent.com/2030983/84583316-22ea9300-adac-11ea-9b62-adcae3b21277.gif)


## Future Plans

It would be nice to include an OLED feather wing display to display text status updates and add further interactivity using the onboard buttons.

Other Ideas:

- use up/down to cycle between brightness
- use left/right to cycle between patterns
- think about how to "play" multiple patterns
- find code with various patterns in backup
- try using the [adafruit_led_animation library](https://github.com/adafruit/Adafruit_CircuitPython_LED_Animation) to switch between patterns