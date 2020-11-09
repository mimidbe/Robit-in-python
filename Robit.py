from microbit import *
import utime
import machine
import music

class Robit:
    PRESCALE_REG = 0xFE
    MODE_1_REG = 0x00
    SRV_REG_BASE = 0x08
    MOT_REG_BASE = 0x28
    REG_OFFSET = 4
    SERVO_MULTIPLIER = 226
    SERVO_ZERO_OFFSET = 0x66

    chipAddress = 0x40
    initialised = False
    stepInit = False
    stepStage = 0
    stepper1Steps = 200
    stepper2Steps = 200
    lineFollowLeftPin = pin13
    lineFollowRightPin = pin14
    
    J1 = 0
    J2 = 1     
    J3 = 2
    J4 = 3
    Jpin = ((pin13, pin14), (pin15, pin16), (pin1, pin2), (pin3, pin4))

    def __init__(self):

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

    def servoWrite(self, servo, degrees):
        if self.initialised is False:
            self.__init__(self)
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

    def motorOn(self, motor, direction, speed):
        if self.initialised is False:
            self.__init__(self)
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

    def motorOff(self, motor):
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
    
    def Ultrasonic(self, jpin):
        pin = self.Jpin[jpin][1]
        # send pulse	
        pin.write_digital(0)
        utime.sleep_us(2)
        pin.write_digital(1)
        utime.sleep_us(10)
        pin.write_digital(0)
        # Get the duration, in microseconds, of a pulse high from one of the pin
        distance = machine.time_pulse_us(pin, 1,23000) / 58
        return distance
        
    def init_line_follow(self, jpin):
        self.lineFollowLeftPin = self.Jpin[jpin][0]
        self.lineFollowRightPin = self.Jpin[jpin][1]
    
    def left_line_follow(self):
        return self.lineFollowLeftPin.read_digital()

    def right_line_follow(self): 
        return self.lineFollowRightPin.read_digital()
        
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

    def light_level(self):
        level = pin10.read_analog() 
        return level

