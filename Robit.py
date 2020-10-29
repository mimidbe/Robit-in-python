from microbit import *

import utime
import machine
import music

line_follow_Left_Pin = pin3
line_follow_Right_Pin = pin4

# Servo
S1 = 0
S2 = 1
S3 = 2
S4 = 3
S5 = 4
S6 = 5
S7 = 6
S8 = 7

Servos = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08]

# Motors
M1 = 0
M2 = 1
M3 = 2
M4 = 3
Motors = [0x1, 0x2, 0x3, 0x4]

# Steppers
STEP1 = 0
STEP2 = 1
Steppers = [True, False]

# Port J
J1 = 0
J2 = 1        ,
J3 = 2
J4 = 3
Jpin = ((pin13, pin14), (pin15, pin16), (pin1, pin2), (pin3, pin4))

Jpin_motor = ((pin13, pin14), (pin15, pin16))

# Led

led_on = True
led_off = False

class Robit:
    PRESCALE_REG = 0xFE
    MODE_1_REG = 0x00
    SRV_REG_BASE = 0x08
    MOT_REG_BASE = 0x28
    REG_OFFSET = 4
    SERVO_MULTIPLIER = 226
    SERVO_ZERO_OFFSET = 0x66

    chipAddress = 0x40  # PCA9685 ADDRESS  of the board
    initialised = False
    stepInit = False
    stepStage = 0
    stepper1Steps = 200
    stepper2Steps = 200

    def __init(self):
            
        buf = bytearray(2)

        buf[0] = self.PRESCALE_REG
        buf[1] = 0x85  # 50Hz
        i2c.write(self.chipAddress, buf, False)
        
        for blockReg in range(0xFA, 0xFE, 1):
            buf[0] = blockReg
            buf[1] = 0x00
            i2c.write(self.chipAddress, buf, False)

        buf[0] = self.MODE_1_REG
        buf[1] = 0x01
        i2c.write(self.chipAddress, buf, False)
        self.initialised = True

    def servoWrite(self, serv, degrees):
        servo = Servos[serv]
        if self.initialised is False:
            self.__init(self)
        buf = bytearray(2)
        calcServo = self.SRV_REG_BASE + ((servo - 1) * self.REG_OFFSET)
        HighByte = False
        PWMVal = (degrees * 100 * self.SERVO_MULTIPLIER) / (10000 + self.SERVO_ZERO_OFFSET)
        
        if (PWMVal > 0xFF):
            HighByte = True
        buf[0] = calcServo
        buf[1] = int(PWMVal)
        i2c.write(self.chipAddress, buf, False)
        buf[0] = calcServo + 1
        if (HighByte):
            buf[1] = 0x01
        else:
            buf[1] = 0x00
        i2c.write(self.chipAddress, buf, False)

    def motorOn(self, mot, direction, speed):
        motor = Motors[mot]
        if self.initialised is False:
            self.__init(self)
        buf = bytearray(2)
        motorReg = self.MOT_REG_BASE + (2 * (motor - 1) * self.REG_OFFSET)
        HighByte = False
        OutputVal = speed * 40
        
        if direction == "forward":
            if OutputVal > 0xFF:
                HighByte = True
                HighOutputVal = int(OutputVal/256)
            buf[0] = motorReg
            buf[1] = int(OutputVal)
            i2c.write(self.chipAddress, buf, False)
            buf[0] = motorReg + 1
            if HighByte:
                buf[1] = HighOutputVal
            else:
                buf[1] = 0x00
            i2c.write(self.chipAddress, buf, False)
            
            for offset in range(4, 6, 1):
                buf[0] = motorReg + offset
                buf[1] = 0x00
                i2c.write(self.chipAddress, buf, False)
            
        elif direction == "reverse":
            if OutputVal > 0xFF:
                HighByte = True
                HighOutputVal = int(OutputVal/256)
            buf[0] = motorReg + 4
            buf[1] = int(OutputVal)
            i2c.write(self.chipAddress, buf, False)
            buf[0] = motorReg + 5
            if HighByte:
                buf[1] = HighOutputVal
            else:
                buf[1] = 0x00
            i2c.write(self.chipAddress, buf, False)
            
            for offset2 in range(0, 2, 1):
                buf[0] = motorReg + offset2
                buf[1] = 0x00
                i2c.write(self.chipAddress, buf, False)

    def motorOff(self, mot):
        motor = Motors[mot]
        buf = bytearray(2)
        motorReg = self.MOT_REG_BASE + (2 * (motor - 1) * self.REG_OFFSET)
        
        for offset3 in range(0, 2, 1):
            buf[0] = motorReg + offset3
            buf[1] = 0x00
            i2c.write(self.chipAddress, buf, False)
        
        for offset4 in range(4, 6, 1):
            buf[0] = motorReg + offset4
            buf[1] = 0x00
            i2c.write(self.chipAddress, buf, False)

    def allOff(self):
        buf = bytearray(2)
        servoOffCount = 0
        servoRegCount = 0
        
        for motors in range(1, 5, 1):
            self.motorOff(self, motors)

        while servoOffCount < 8:
            for offset5 in range(0, 2, 1):
                buf[0] = self.SRV_REG_BASE + servoRegCount + offset5
                buf[1] = 0x00
                i2c.write(self.chipAddress, buf, False)

            servoRegCount += 4
            servoOffCount += 1

    def stepperMotorTurnAngle(self, step, direction, angle):
        stepper = Steppers[step]
        angleToSteps = 0

        if self.initialised is False: 
            self.__init(self)

        if stepper:
            angleToSteps = ((angle - 1) * (self.stepper1Steps - 1)) / (360 - 1) + 1
        else:
            angleToSteps = ((angle - 1) * (self.stepper2Steps - 1)) / (360 - 1) + 1

        angleToSteps = int(angleToSteps)
        self._turnStepperMotor(self, step, direction, angleToSteps)

    def stepperMotorTurnSteps(self, step, direction, stepperSteps):
        if self.initialised is False: 
            self.__init(self)

        self._turnStepperMotor(self, step, direction, stepperSteps)

    def _turnStepperMotor(self, step, direction, steps):
        stepper = Steppers[step]
        stepCounter = 0

        if self.stepInit is False:
            self.stepStage = 1
            self.stepInit = True

        while stepCounter < steps:
            if self.stepStage == 1 or self.stepStage == 3:
                if stepper:
                    currentMotor = 1
                else:
                    currentMotor = 3
            else:
                if stepper:
                    currentMotor = 2
                else:
                    currentMotor = 4

            if self.stepStage == 1 or self.stepStage == 4:
                currentDirection = "forward"
            else:
                currentDirection = "reverse"

            self.motorOn(self, currentMotor, currentDirection, 100)
            sleep(20)

            if direction == "forward":
                if self.stepStage == 4: 
                    self.stepStage = 1
                else:
                    self.stepStage += 1
            elif direction == "reverse":
                if self.stepStage == 1: 
                    self.stepStage = 4
                else:
                    self.stepStage -= 1
            
            stepCounter += 1

    #
    # get Ultrasonic
    # @param jpin, eg: J3
    #
    # blockId=robit_ultrasonic 
    # block="Ultrasonic|pin %Jpin"
    # weight=10

    def Ultrasonic(self, jpin):
        pin = Jpin[jpin][1]
        # send pulse	
        pin.write_digital(0)
        utime.sleep_us(2)
        pin.write_digital(1)
        utime.sleep_us(10)
        pin.write_digital(0)
        distance = machine.time_pulse_us(self.broche2, 1) / 58
        return distance

    # makeblock_touch_sensor
    # @param jpin; eg: J1
    # blockId=Touch_sensor_is_touched 
    # Touch sensor is touched on|pin %pin"
    # advanced=true
    # weight=10

    def Touch_sensor_is_touched(self, jpin): 
        pin = Jpin[jpin][1]
        if pin.read_digital() == 1:
            return True
        else:
            return False

    # makeblock_led
    # @param jpin; eg: J1
    # blockId=makeblock_led 
    # connect LED to|pin %Jpin|turn %Led_on or Led_off
    # weight=10
    # advanced=true
    def set_makeblock_led(jpin, sta): 
        pin = Jpin[jpin][1]
        if sta:
            pin.write_digital(1)
        elif not sta:
            pin.write_digital(0)

    # blockId=makeblock_motor 
    # @param jpin; eg: J1
    # connect 130-motor to|pin %Jpin|speed %speed "
    # weight=10
    # speed.min=-100 speed.max=100
    # advanced=true
    def set_makeblock_motor(self, jpin, speed): 
        pin1 = Jpin[jpin][0]
        pin2 = Jpin[jpin][1]
        speed = speed * 10  # map 100 to 1000
        if speed < 1000:
            speed = -1000
        elif speed > 1000:
            speed = 1000
        elif speed >= 0:
            pin1.write_analog(0)
            # period of(PWM) in microSeconds
            pin2.set_analog_period_microseconds(1000)  
            pin2.write_analog(speed)
        elif speed < 0:
            speed = speed * -1
            pin2.write_analog(0)
            pin1.set_analog_period_microseconds(1000)
            pin1.write_analog(pin1, speed)
    #
    # init line follow
    # @param jpin; eg: J1
    #
    # blockId=robit_init_line_follow 
    # init line follow|pin %jpin"
    # weight=10
    
    def init_line_follow(self, jpin):
        global line_follow_Left_Pin
        global line_follow_Right_Pin
        line_follow_Left_Pin = Jpin[jpin][0]
        line_follow_Right_Pin = Jpin[jpin][1]

    #
    # line follow left
    #
    # blockId=robit_left_line_follow 
    # left line follow digitalpin"
    # weight=10
    def left_line_follow(self):
        return line_follow_Left_Pin.read_digital()

    #
    # right follow right
    #
    # blockId=robit_right_line_follow 
    # right line follow digitalpin"
    # weight=10
    def right_line_follow(self): 
        return line_follow_Right_Pin.read_digital()
        
    # music on Buzzer in P0	
    def sound_r2d2(self):
        tune = ["A7:0", "G7:0", "E7:0", "C7:0", 
                "D7:0", "B7:0", "F7:0", "C8:0", 
                "A7:0", "G7:0", "E7:0", "C7:0", 
                "D7:0", "B7:0", "F7:0", "C8:0"]
        music.play(tune)

    def sound_bip(self):
        for i in range(2):
            freq = 2000
            while freq > 1000:
                music.pitch(int(freq), 10)
                freq *= 0.95
            freq = 1000
            while freq < 3000:
                music.pitch(int(freq), 10)
                freq *= 1.05

    # mlight level of light sensor on Pin10   
    def light_level(self):
        level = pin10.read_analog()  # level 0 to 1023
        return level

while True:
    theBoard = Robit
    if button_a.is_pressed():
        theBoard.stepperMotorTurnAngle(STEP1, "forward", 180)
        theBoard.motorOn(M3, "forward", 10)
        theBoard.motorOn(M4, "reverse", 100)
        theBoard.servoWrite(S1, 180)
        theBoard.servoWrite(S2, 180)
        theBoard.servoWrite(S3, 180)
        theBoard.servoWrite(S4, 180)
        theBoard.servoWrite(S5, 0)
        theBoard.servoWrite(S6, 0)
        theBoard.servoWrite(S7, 0)
        theBoard.servoWrite(S8, 0)
    if button_b.is_pressed():
        theBoard.stepperMotorTurnSteps(STEP1, "reverse", 100)
        theBoard.motorOff(M3)
        theBoard.motorOff(M4)
        theBoard.servoWrite(S1, 90)
        theBoard.servoWrite(S2, 90)
        theBoard.servoWrite(S3, 90)
        theBoard.servoWrite(S4, 90)
        theBoard.servoWrite(S5, 90)
        theBoard.servoWrite(S6, 90)
        theBoard.servoWrite(S7, 90)
        theBoard.servoWrite(S8, 90)
    if button_a.is_pressed() and button_b.is_pressed():
        theBoard.allOff()