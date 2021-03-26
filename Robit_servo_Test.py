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
