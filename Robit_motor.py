from microbit import *
from math import floor,fabs
from utime import sleep_us
from machine import time_pulse_us
from neopixel import NeoPixel
from music import pitch,play
class Robit:
    f=50;P=64;Mo=0;PR=254;LED0_ON_L=6;ALL_LED_ON_L=250;init=False;LFLPin=pin13;LFRPin=pin14;np=NeoPixel(pin12,2)
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
    def MotorRun(s,C,A):
        if not s.init:s.__AA()
        if A>=100:A=100
        if A<=-100:A=-100
        if C>4 or C<=0:return
        D=(C-1)*2;A*=40
        if A>=0:s.__CC(D,0,A);s.__CC(D+1,0,0)
        else:s.__CC(D,0,0);s.__CC(D+1,0,-A)
    def MotorStop(s,I):s.MotorRun(I, 0)
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
    def SoundR2D2(s):I='C8:0';H='F7:0';G='B7:0';F='D7:0';E='C7:0';D='E7:0';C='G7:0';B='A7:0';A=[B,C,D,E,F,G,H,I,B,C,D,E,F,G,H,I];play(A)
    def SoundBip(s):
        for E in range(2):
            A=2000
            while A>1000:pitch(int(A),10);A*=0.95
            while A<3000:pitch(int(A),10);A*=1.05