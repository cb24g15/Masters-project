const int MotorPin = 5;     //Name Pins
const int SensorPin = A0;
const int DirPin1 = 4;
const int DirPin2 = 3;
const int SwitchPin = 7;
int V = 0;
int Pos_1 = 0;
int Pos_2 = 0;
int Pos_3 = 0;
int Pos_4 = 0;
float Integral = 0;
int V_mapped;
unsigned long micros_start;
unsigned long micros_last = 0;
unsigned long dT = 1000-4;
int ZeroPos = 600;
int map_point = 30;
float k_p = 87;    //Set up Control Variables
float k_d = 0.0E6;
float k_i = 0E-6;
float K = 1;

void setup() {
  Serial.begin(1000000);
  pinMode(13, OUTPUT);    //Assign Pins (13 is on board LED)
  pinMode(MotorPin, OUTPUT);
  pinMode(SensorPin, INPUT);
  pinMode(DirPin1, OUTPUT);
  pinMode(DirPin2, OUTPUT);
  pinMode(SwitchPin, INPUT);
  while(digitalRead(SwitchPin) == 0){if (analogRead(A0) == ZeroPos){digitalWrite(13, HIGH);} else {digitalWrite(13, LOW);} Serial.println(analogRead(A0)-ZeroPos);}
  micros_last = micros() - dT;
  micros_start = micros();
}

void loop() {
 if (micros()-micros_last >= dT) {
 micros_last = micros();
 int Pos = analogRead(A0) - ZeroPos;   

 Integral = Integral + (k_i * Pos * (dT+4));
 float Deriv = ((25*Pos) - (48*Pos_1) + (36*Pos_2) - (16*Pos_3) + (3*Pos_4));
 V = K * ((k_p * Pos) + (k_d * Deriv/(12*(dT-4))) + Integral); 

 Pos_4 = Pos_3; 
 Pos_3 = Pos_2; 
 Pos_2 = Pos_1; 
 Pos_1 = Pos;
 
 if (V > 0) {digitalWrite(DirPin1, HIGH); digitalWrite(DirPin2, LOW);} else {digitalWrite(DirPin1, LOW); digitalWrite(DirPin2, HIGH);}  //Set Motor Direction
 if (V > 255) {V = 255;}
 if (V < -255) {V = -255;}
 if (abs(V) > 0) {V_mapped = map(abs(V), 0, 255, map_point, 255);} else {V_mapped = 0;}
 analogWrite(MotorPin, V_mapped);
  
 Serial.print(micros_last - micros_start);
 Serial.print("\t");
 Serial.print(Pos, DEC);
 Serial.print("\t");
 Serial.println(V);
 }
}
