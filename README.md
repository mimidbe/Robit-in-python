# Robit in python
A Robit package in python, for the [ElecFreaks](https://www.elecfreaks.com/robit-diy-mini-smart-cars-robot-development-platform-chassis-for-micro-bit-compatible-with-mbot.html) kit Robit.

## Code Example for using Robit with motor
```Python
from microbit import *
from Robit_motor import Robit
from random import randint

theBoard = Robit()
while True:
    red = randint(0, 60)
    green = randint(0, 60)
    blue = randint(0, 60)
    if button_a.is_pressed():
        print(theBoard.LightLevel())
        theBoard.MotorRun(1, 50)
        theBoard.MotorRun(2, -50)
        theBoard.LedRGBLeft(red, green, blue)
        theBoard.SoundR2D2()
    elif button_b.is_pressed():
        theBoard.MotorRun(1, -50)
        theBoard.MotorRun(2, 50)
        theBoard.LedRGBRight(red, green, blue)
    else:
        theBoard.MotorStop(1)
        theBoard.MotorStop(2)
        theBoard.LedRGBRight(0, 0, 0)
        theBoard.LedRGBLeft(0, 0, 0) 
```

## Code Example for using Robit with servo
```Python
from microbit import *
from Robit_servo import Robit

theBoard = Robit()
while True:
    if button_a.is_pressed():
        theBoard.Servo(1, 50)
        display.show(Image.YES)
        theBoard.LedRGBLeft(10,50,30)
    elif button_b.is_pressed():
        theBoard.Servo(1, 180)
        display.show(Image.NO)
        theBoard.LedRGBRight(100,50,60)
        theBoard.SoundR2D2()
    else:
        theBoard.LedRGBLeft(0,0,0)
        theBoard.LedRGBRight(0,0,0)
        theBoard.Servo(1, 0)
'''

## Code Example for using Robit with stepper motor
```Python
from microbit import *
import Robit_stepper

theBoard = Robit_stepper.Robit()
while True:
    if button_a.is_pressed():
        theBoard.StepperDegree(1, 500, "W")
    elif button_b.is_pressed():
        theBoard.StepperDegree(1, -500, "W")
    else:
        theBoard.MotorStopAll()	
'''

## License
MIT

## Supported targets
for BBC micro:bit embeded on Robit board
