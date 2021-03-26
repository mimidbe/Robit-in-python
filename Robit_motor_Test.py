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
