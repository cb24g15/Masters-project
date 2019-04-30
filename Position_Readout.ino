const int SensorPin = A0;
int SensorVal;

void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
pinMode(SensorPin, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
SensorVal = analogRead(SensorPin);
Serial.println(SensorVal);
}
