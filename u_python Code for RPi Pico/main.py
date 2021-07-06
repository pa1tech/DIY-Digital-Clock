from machine import I2C, Pin
from urtc import DS1307
import time

i2c_rtc = I2C(0,scl = Pin(17),sda = Pin(16))
result = I2C.scan(i2c_rtc)
rtc = DS1307(i2c_rtc)

led = Pin(25, Pin.OUT); led.on()

G = Pin(4, Pin.OUT) 
F = Pin(5, Pin.OUT) 
A = Pin(6, Pin.OUT)
B = Pin(7, Pin.OUT)
D = Pin(9, Pin.OUT)
C = Pin(14, Pin.OUT)
E = Pin(15, Pin.OUT)
SEC = Pin(13, Pin.OUT)

states = Pin(19,Pin.IN,Pin.PULL_DOWN)
inc = Pin(26,Pin.IN,Pin.PULL_DOWN)

CA1 = Pin(0, Pin.OUT)
CA2 = Pin(1, Pin.OUT)
CA3 = Pin(2, Pin.OUT)
CA4 = Pin(3, Pin.OUT)

segs = [A,B,C,D,E,F,G]
numbers = [0b1000000, 0b1111001, 0b0100100, 0b0110000, 0b0011001, 0b0010010,
0b0000010, 0b1111000, 0b0000000, 0b0010000]

sec_old = 0; d = 0.002
sett = False; state = 0; gg = True
hour = 0; minute = 0

def state_change(pin): 
  global state, sett
  state += 1
  if(state == 3):
    state = 0
    sett = True

def up(pin):
  global state, gg
  global hour, minute
  if(state == 1):
      hour = (hour+1)%24;
  elif(state == 2):
      minute = (minute+1)%60;

def lightDigit1(number):
  CA1.on()
  CA2.off()
  CA3.off()
  CA4.off()
  lightSegments(number);
  time.sleep(d);
  CA1.off()
  time.sleep(d);

def lightDigit2(number):
  CA1.off()
  CA2.on()
  CA3.off()
  CA4.off()
  lightSegments(number);
  time.sleep(d);
  CA2.off()
  time.sleep(d);

def lightDigit3(number):
  CA1.off()
  CA2.off()
  CA3.on()
  CA4.off()
  lightSegments(number);
  time.sleep(d);
  CA3.off()
  time.sleep(d);

def lightDigit4(number):
  CA1.off()
  CA2.off()
  CA3.off()
  CA4.on()
  lightSegments(number);
  time.sleep(d);
  CA4.off()
  time.sleep(d);

def lightSegments(number):
  for i in range(7):
    (segs[i]).value( ((number >> i) & 1) )

states.irq(trigger=Pin.IRQ_RISING, handler=state_change)
inc.irq(trigger=Pin.IRQ_RISING, handler=up)

while True:
    if (state == 0):
      if(sett):
        now = (2020,10,10,2,hour,minute,10,0)
        rtc.datetime(now)
        time.sleep(10*d)
        sett = False;
    
      (year,month,date,day,hour,minute,second,p1)=rtc.datetime()
      if sec_old is not second:
        SEC.toggle()
        sec_old = second

    first_h = int(hour / 10);
    second_h = int(hour % 10);
    first_m = int(minute / 10);
    second_m = int(minute % 10);

    if(state == 1):
      CA3.off()
      CA4.off()
      SEC.on()
      lightDigit1(numbers[first_h]);
      lightDigit2(numbers[second_h]);
    elif(state == 2):
      CA1.off()
      CA2.off()
      SEC.on()
      lightDigit3(numbers[first_m]);
      lightDigit4(numbers[second_m]);
    else:
      lightDigit1(numbers[first_h]);
      lightDigit2(numbers[second_h]);
      lightDigit3(numbers[first_m]);
      lightDigit4(numbers[second_m]);


