from microbit import *
from math import floor,fabs
from utime import sleep_us
from machine import time_pulse_us
from neopixel import NeoPixel
class Robit:
    f=50;N=20;d=N*1000/360/f;P=64;Mo=0;PR=254;LED0_ON_L=6;ALL_LED_ON_L=250;init=False;LFLPin=pin13;LFRPin=pin14;np=NeoPixel(pin12,2)
    def __init__(s):s.__AA()
    def __AA(s):
        i2c.write(s.P,bytearray([s.Mo,0]));s.__BB(s.f)
        for C in range(16):s.__CC(C,0,0)
        s.init=True
    def __BB(s,f=None):
        if f is None:i2c.write(s.P,bytearray([s.PR]));return int(25000000.0/4096/(i2c.read(s.P,1)-0.5))
        G=int(floor(25000000.0/4096.0/f-1+0.5));i2c.write(s.P,bytearray([s.Mo]));D=i2c.read(s.P,1)[0];i2c.write(s.P,bytearray([s.Mo,D&127|16]));i2c.write(s.P,bytearray([s.PR,G]));i2c.write(s.P,bytearray([s.Mo,D]));sleep(1);i2c.write(s.P,bytearray([s.Mo,D|161]))
    def __CC(s,C,on,off):
        if C<0 or C>15:return
        A=bytearray(5);A[0]=s.LED0_ON_L+4*C;A[1]=on&255;A[2]=on>>8&255;A[3]=off&255;A[4]=off>>8&255;i2c.write(s.P,bytearray(A))
    def __DD(s,on,off):A=bytearray(5);A[0]=s.ALL_LED_ON_L;A[1]=on&255;A[2]=on>>8&255;A[3]=off&255;A[4]=off>>8&255;i2c.write(s.P,bytearray(A))
    def __EE(s,I,A,B):
        if B=='W':AL=1;AH=1023;BL=2047;BH=3071;CL=1023;CH=2047;DL=3071;DH=4095
        elif B=='F':AL=1;AH=2047;BL=2047;BH=4095;CL=1023;CH=3071;DL=3071;DH=1023
        elif B=='H':AL=3582;AH=1023;BL=1534;BH=3071;CL=511;CH=2047;DL=2558;DH=4095
        if I==1:
            if A:s.__CC(0,AL,AH);s.__CC(1,BL,BH);s.__CC(2,CL,CH);s.__CC(3,DL,DH)
            else:s.__CC(0,DL,DH);s.__CC(1,CL,CH);s.__CC(2,BL,BH);s.__CC(3,AL,AH)
        else:
            if A:s.__CC(4,AL,AH);s.__CC(5,BL,BH);s.__CC(6,CL,CH);s.__CC(7,DL,DH)
            else:s.__CC(4,DL,DH);s.__CC(5,CL,CH);s.__CC(6,BL,BH);s.__CC(7,BL,AH)
    def StepperDegree(s,I,D,M='F'):s.__EE(I,D>0,M);D=fabs(D);sleep(s.d*D);s.MotorStopAll()
    def MotorStopAll(s):s.__DD(0,0)
    def Ultrasonic(s,b):A=s.Jpin.get(b)[1];s.write_digital(0);sleep_us(2);s.write_digital(1);sleep_us(10);s.write_digital(0);C=time_pulse_us(A,1,23000)/58;return C
    def init_line_follow(s,a):
        if a=='J1':s.LFLPin=pin13;s.LFRPin=pin14
        elif a=='J2':s.LFLPin=pin15;s.LFRPin=pin16
        elif a=='J3':s.LFLPin=pin1;s.LFRPin=pin2
        elif a=='J4':s.LFLPin=pin3;s.LFRPin=pin4		
    def left_line_follow(s):return s.LFLPin.read_digital()
    def right_line_follow(s):return s.LFRPin.read_digital()
    def LightLevel(s):display.off();return pin10.read_analog()
    def LedRGBLeft(s,r,g,b):s.np[1]=(r,g,b);s.np.show()
    def LedRGBRight(s,r,g,b):s.np[0]=(r,g,b);s.np.show()