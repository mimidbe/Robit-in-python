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