const int MotorPin = 5;     //Name Pins
//const int SensorPin = A0;
const int DirPin1 = 4;
const int DirPin2 = 3;
const int SwitchPin = 7;
int V = 0;
float Pos_1 = 0;
float Pos_2 = 0;
float Pos_3 = 0;
float Pos_4 = 0;
float Integral = 0;
int V_mapped;
unsigned long micros_start;
unsigned long micros_last = 0;
//unsigned long dT = 20000-4;
float ZeroPos = 0;
int map_point = 30;
float k_p = 130;    //Set up Control Variables
float k_d = 0.0E6;
float k_i = 0E-6;
float K = 1;

#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps20.h"
#if I2DEV_IMPLEMANTATION == I2CDEV_ARDUINO_WIRE
  #include "wire_h"
#endif

MPU6050 mpu;

//#define OUTPUT_READABLE_YAWPITCHROLL

#define INTERRUPT_PIN 2
#define LED_PIN 13
bool blinkstate = false;

bool dmpReady = false;  // set true if DMP init was successful
uint8_t mpuIntStatus;   // holds actual interrupt status byte from MPU
uint8_t devStatus;      // return status after each device operation (0 = success, !0 = error)
uint16_t packetSize;    // expected DMP packet size (default is 42 bytes)
uint16_t fifoCount;     // count of all bytes currently in FIFO
uint8_t fifoBuffer[64]; // FIFO storage buffer

// orientation/motion vars
Quaternion q;           // [w, x, y, z]         quaternion container
VectorFloat gravity;
float ypr[3];     

volatile bool mpuInterrupt = false;     // indicates whether MPU interrupt pin has gone high
void dmpDataReady() {
    mpuInterrupt = true;
}

void setup() {
  pinMode(13, OUTPUT);    //Assign Pins (13 is on board LED)
  pinMode(MotorPin, OUTPUT);
  //pinMode(SensorPin, INPUT);
  pinMode(DirPin1, OUTPUT);
  pinMode(DirPin2, OUTPUT);
  pinMode(SwitchPin, INPUT);

  // join I2C bus (I2Cdev library doesn't do this automatically)
  #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
      Wire.begin();
      Wire.setClock(400000); // 400kHz I2C clock. Comment this line if having compilation difficulties
  #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
      Fastwire::setup(400, true);
  #endif

  // initialize serial communication
  // (115200 chosen because it is required for Teapot Demo output, but it's
  // really up to you depending on your project)
  Serial.begin(115200);
  while (!Serial); // wait for Leonardo enumeration, others continue immediately

    // NOTE: 8MHz or slower host processors, like the Teensy @ 3.3V or Arduino
    // Pro Mini running at 3.3V, cannot handle this baud rate reliably due to
    // the baud timing being too misaligned with processor ticks. You must use
    // 38400 or slower in these cases, or use some kind of external separate
    // crystal solution for the UART timer.

  // initialize device
  Serial.println(F("Initializing I2C devices..."));
  mpu.initialize();
  pinMode(INTERRUPT_PIN, INPUT);

  // verify connection
  Serial.println(F("Testing device connections..."));
  Serial.println(mpu.testConnection() ? F("MPU6050 connection successful") : F("MPU6050 connection failed"));

  // wait for ready
  Serial.println(F("\nSend any character to begin DMP programming and demo: "));
  while (Serial.available() && Serial.read()); // empty buffer
  while (!Serial.available());                 // wait for data
  while (Serial.available() && Serial.read()); // empty buffer again

  // load and configure the DMP
  Serial.println(F("Initializing DMP..."));
  devStatus = mpu.dmpInitialize();

  // supply your own gyro offsets here, scaled for min sensitivity
  mpu.setXGyroOffset(220);
  mpu.setYGyroOffset(76);
  mpu.setZGyroOffset(-85);
  mpu.setZAccelOffset(1788); // 1688 factory default for my test chip

  // make sure it worked (returns 0 if so)
  if (devStatus == 0) {
      // turn on the DMP, now that it's ready
      Serial.println(F("Enabling DMP..."));
      mpu.setDMPEnabled(true);

      // enable Arduino interrupt detection
      Serial.print(F("Enabling interrupt detection (Arduino external interrupt "));
      Serial.print(digitalPinToInterrupt(INTERRUPT_PIN));
      Serial.println(F(")..."));
      attachInterrupt(digitalPinToInterrupt(INTERRUPT_PIN), dmpDataReady, RISING);
      mpuIntStatus = mpu.getIntStatus();

      // set our DMP Ready flag so the main loop() function knows it's okay to use it
      Serial.println(F("DMP ready! Waiting for first interrupt..."));
      dmpReady = true;
     // get expected DMP packet size for later comparison
      packetSize = mpu.dmpGetFIFOPacketSize();
  } else {
      // ERROR!
      // 1 = initial memory load failed
      // 2 = DMP configuration updates failed
      // (if it's going to break, usually the code will be 1)
      Serial.print(F("DMP Initialization failed (code "));
      Serial.print(devStatus);
      Serial.println(F(")"));
  }
  
  //while(digitalRead(SwitchPin) == 0){if (analogRead(A0) == ZeroPos){digitalWrite(13, HIGH);} else {digitalWrite(13, LOW);} Serial.println(analogRead(A0)-ZeroPos);}
  micros_last = micros(); //- dT;
  micros_start = micros();
}

void loop() {
 //if (micros()-micros_last >= dT) {
 
     // if programming failed, don't try to do anything
    if (!dmpReady) return;

    // wait for MPU interrupt or extra packet(s) available
    while (!mpuInterrupt && fifoCount < packetSize) {
        if (mpuInterrupt && fifoCount < packetSize) {
          // try to get out of the infinite loop 
          fifoCount = mpu.getFIFOCount();
        }  
        // other program behavior stuff here
        // .
        // .
        // .
        // if you are really paranoid you can frequently test in between other
        // stuff to see if mpuInterrupt is true, and if so, "break;" from the
        // while() loop to immediately process the MPU data
        // .
        // .
        // .
    }

    // reset interrupt flag and get INT_STATUS byte
    mpuInterrupt = false;
    mpuIntStatus = mpu.getIntStatus();

    // get current FIFO count
    fifoCount = mpu.getFIFOCount();

    // check for overflow (this should never happen unless our code is too inefficient)
    if ((mpuIntStatus & _BV(MPU6050_INTERRUPT_FIFO_OFLOW_BIT)) || fifoCount >= 1024) {
        // reset so we can continue cleanly
        mpu.resetFIFO();
        fifoCount = mpu.getFIFOCount();
        Serial.println(F("FIFO overflow!"));

    // otherwise, check for DMP data ready interrupt (this should happen frequently)
    } else if (mpuIntStatus & _BV(MPU6050_INTERRUPT_DMP_INT_BIT)) {
        // wait for correct available data length, should be a VERY short wait
        while (fifoCount < packetSize) fifoCount = mpu.getFIFOCount();

        // read a packet from FIFO
        mpu.getFIFOBytes(fifoBuffer, packetSize);
        
        // track FIFO count here in case there is > 1 packet available
        // (this lets us immediately read more without waiting for an interrupt)
        fifoCount -= packetSize;
    }   

 mpu.dmpGetQuaternion(&q, fifoBuffer);
 mpu.dmpGetGravity(&gravity, &q);
 mpu.dmpGetYawPitchRoll(ypr, &q, &gravity);
 
 unsigned long dT = micros() - micros_last;
 micros_last = micros();
 float Pos = (ypr[1] * 180/M_PI) - ZeroPos;
 
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
 //}
}
