#include <Wire.h>
#include <RTClib.h>

#define SET 2
#define UP 3

#define A 4
#define B 5
#define C 6
#define D 7
#define E 8
#define F 9
#define G 10
#define sec 11

#define CA1 A0
#define CA2 A1
#define CA3 A2
#define CA4 A3

int d = 2, state=0, first_h=0, second_h=0, first_m=0, second_m=0, sec_old=0, h, m, s;
bool set = false;
RTC_DS1307 rtc;

const int segs[7] = { A, B, C, D, E, F, G};

const byte numbers[11] = {0b1000000, 0b1111001, 0b0100100, 0b0110000, 0b0011001, 0b0010010,
0b0000010, 0b1111000, 0b0000000, 0b0010000};

void state_change(){
  state += 1;
  if(state == 3){
    state = 0;
    set = true;
  }
}

void up(){
  if(state == 1){
      h = (h+1)%24;
  }else if(state == 2){
      m = (m+1)%60;
  }
}

void setup()
{
  Serial.begin(57600);
  #ifdef AVR
    Wire.begin();
  #else
    Wire1.begin();
  #endif
    rtc.begin();

  for(int i=4;i<=13;i++)
  {
    pinMode(i, OUTPUT);
  }
  for(int i=4;i<=13;i++)
  {
    digitalWrite(i, LOW);
  }
  pinMode(A0, OUTPUT);
  pinMode(A1, OUTPUT);
  pinMode(A2, OUTPUT);
  pinMode(A3, OUTPUT);  
  pinMode(2, INPUT_PULLUP);
  pinMode(3, INPUT_PULLUP);

  attachInterrupt( 2, state_change, FALLING);
  attachInterrupt( 3, up, FALLING);
}

void loop()
{
  if (state == 0){
    if(set){
      rtc.adjust(DateTime(2020, 10, 16, h, m, 0));
      delay(10*d);
      set = false;
    }
    
    DateTime now = rtc.now();
    
    h = now.hour();
    m = now.minute();
    s = now.second();
    
    if(s!=sec_old){
      digitalWrite(sec,!digitalRead(sec));
      sec_old = s;
    }
  }
  
  first_h = h / 10;
  second_h = h % 10;
  first_m = m / 10;
  second_m = m % 10;

  if(state == 1){
    lightDigit1(numbers[first_h]);
    lightDigit2(numbers[second_h]);
    digitalWrite(CA3, LOW);
    digitalWrite(CA4, LOW);
    digitalWrite(sec,LOW);
  }else if(state == 2){
    digitalWrite(CA1, LOW);
    digitalWrite(CA2, LOW);
    lightDigit3(numbers[first_m]);
    lightDigit4(numbers[second_m]);
    digitalWrite(sec,LOW);
  }else{
    lightDigit1(numbers[first_h]);
    lightDigit2(numbers[second_h]);
    lightDigit3(numbers[first_m]);
    lightDigit4(numbers[second_m]);
  }
} 

void lightDigit1(byte number) {
  digitalWrite(CA1, HIGH);
  digitalWrite(CA2, LOW);
  digitalWrite(CA3, LOW);
  digitalWrite(CA4, LOW);
  lightSegments(number);
  delay(d);
  digitalWrite(CA1, LOW);
  delay(d);
}

void lightDigit2(byte number) {
  digitalWrite(CA1, LOW);
  digitalWrite(CA2, HIGH);
  digitalWrite(CA3, LOW);
  digitalWrite(CA4, LOW);
  lightSegments(number);
  delay(d);
  digitalWrite(CA2, LOW);
  delay(d);
}

void lightDigit3(byte number) {
  digitalWrite(CA1, LOW);
  digitalWrite(CA2, LOW);
  digitalWrite(CA3, HIGH);
  digitalWrite(CA4, LOW);
  lightSegments(number);
  delay(d);
  digitalWrite(CA3, LOW);
  delay(d);
}

void lightDigit4(byte number) {
  digitalWrite(CA1, LOW);
  digitalWrite(CA2, LOW);
  digitalWrite(CA3, LOW);
  digitalWrite(CA4, HIGH);
  lightSegments(number);
  delay(d);
  digitalWrite(CA4, LOW);
  delay(d);
}

void lightSegments(byte number) {
  for (int i = 0; i < 7; i++) {
    int bit = bitRead(number, i);
    digitalWrite(segs[i], bit);
  }
}
