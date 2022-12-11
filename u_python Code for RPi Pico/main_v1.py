from machine import I2C, Pin
from urtc import DS1307
import time

i2c_rtc = I2C(1,scl = Pin(27),sda = Pin(26))
result = I2C.scan(i2c_rtc)
rtc = DS1307(i2c_rtc)

led = Pin(25, Pin.OUT); led.off()

A = Pin(6, Pin.OUT)
B = Pin(5, Pin.OUT)
C = Pin(1, Pin.OUT)
D = Pin(2, Pin.OUT)
E = Pin(13, Pin.OUT)
F = Pin(7, Pin.OUT)
G = Pin(3, Pin.OUT)

SEC = Pin(0, Pin.OUT)

D0 = Pin(18, Pin.OPEN_DRAIN)
D1 = Pin(8, Pin.OPEN_DRAIN)
D2 = Pin(12, Pin.OPEN_DRAIN)
D3 = Pin(11, Pin.OPEN_DRAIN)

digits = [D0,D1,D2,D3]
segs = [A,B,C,D,E,F,G]
numbers = [0b1000000, 0b1111001, 0b0100100, 0b0110000, 0b0011001, 0b0010010,0b0000010, 0b1111000, 0b0000000, 0b0010000]

sec_old = 0; d = 0.005
hour = 0; minute = 0

def lightDigit(n,number):
  lightSegments(number)
  digits[n].on()
  time.sleep(d)
  digits[n].off()

def lightSegments(number):
  for i in range(7):
    (segs[i]).value( ((number >> i) & 1) )

'''now = (2020,10,10,2,7,23 ,10,0)
rtc.datetime(now)
time.sleep(10*d)'''
        
while True:  
    (year,month,date,day,hour,minute,second,p1)=rtc.datetime()
    if sec_old is not second:
        SEC.toggle()
        sec_old = second
      
    if(hour>12): hour = hour-12

    first_h = int(hour / 10);
    second_h = int(hour % 10);
    first_m = int(minute / 10);
    second_m = int(minute % 10);
    
    if(first_h == 0): digits[0].on()
    else: digits[0].off()

    lightDigit(1,numbers[second_h]);
    lightDigit(2,numbers[first_m]);
    lightDigit(3,numbers[second_m]);

