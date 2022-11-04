// ODOP 2022

#include <AccelStepper.h>
#include <SoftwareSerial.h>

#define dirPin_c 2 // moteur de la courroie
#define stepPin_c 3 // moteur de la courroie
#define dirPin_p 4 // moteur de la pivot
#define stepPin_p 5 // moteur de la pivot

#define BAUD_RATE 9600

#define MAX_SPEED_P 100  // à adapter
#define ACCELERATION_P 50 // à adapter
#define SPEED_P = 100

#define MAX_SPEED_c 100  // à adapter
#define ACCELERATION_c 50 // à adapter
#define SPEED_C = 100

#define ANGLE_RANGE = 17.7777777778f //nombre de pas par degré (microstep 1/32e de pas)


AccelStepper stepper_c = AccelStepper(motorInterfaceType, stepPin_c, dirPin_c);
AccelStepper stepper_p = AccelStepper(motorInterfaceType, stepPin_p, dirPin_p);

//Serial buffer
String readString = "";


void setup() {
  Serial.begin(BAUD_RATE);

  stepper_c.setCurrentPosition();
  stepper_p.setCurrentPosition();
}

void loop() {
  // Read messages form serial
  while (Serial.available()) {
    delay(3);
    char c = Serial.read();  //gets one byte from serial buffer
    if (c == '\n'){
      break;
    }
    readString += c; //makes the string readString
  }

  // Interpret messages, do action, send answer

  if (readString.length() >0) {

    // Motion command in steps for moteur pivot
    if (readString.startsWith("move_p ")) {
      long a =readString.substring(5).toInt();
      setRunningSpeed_p();
      rotateTo_p(a);
      Serial.println("move_p ok");
    }

    // Motion commande for moteur courroie
    if (readString.startsWith("move_c ")) {
      long a =readString.substring(5).toInt();
      setRunningSpeed_c();
      rotateTo_p(a);
      Serial.println("move_p ok");
    }


    // Relative motion command in steps for moteur pivot
    if (readString.startsWith("rotate_p ")) {
      long a =readString.substring(6).toInt();
      setRunningSpeed_p();
      rotate_p(a);
      Serial.println("rotate_p ok");
    }

    // Relative motion command in steps for moteur courroie
    if (readString.startsWith("rotate_c ")) {
      long a =readString.substring(6).toInt();
      setRunningSpeed_c();
      rotate_c(a);
      Serial.println("rotate_c ok");
    }

    // Report status
    if (readString.startsWith("status")) {
      Serial.print("Current position (steps): ");
      Serial.println(stepperX.currentPosition());
      Serial.print("Current position (degrees): ");
      float curPosSteps=(float)stepperX.currentPosition();
      float curPosDeg=curPosSteps/ANGLE_RANGE;
      Serial.println(curPosDeg);
      Serial.println("Status ok");
    }

    readString="";
  }
}

// Actual rotation function, in steps, absolute for moteur pivot
void rotateTo_p(long _angle)
{
  stepper_p.moveTo(_angle);
  while (stepper_p.run()) {
    //No op
  }
  setRunningSpeed_p();
}

// Actual rotation function, in steps, absolute for moteur pivot
void rotateTo_c(long _angle)
{
  stepper_c.moveTo(_angle);
  while (stepper_c.run()) {
    //No op
  }
  setRunningSpeed_c();
}

// Actual rotation function, in steps, relative for moteur pivot
void rotate_p(long _angle)
{
  stepper_p.move(_angle);
  while (stepper_p.run()) {
    //No op
  }
  setRunningSpeed_p();
}

// Actual rotation function, in steps, relative for moteur courroie
void rotate_c(long _angle)
{
  stepper_c.move(_angle);
  while (stepper_c.run()) {
    //No op
  }
  setRunningSpeed_c();
}


void setRunningSpeed_p(void) {
  stepper_p.setMaxSpeed(RUN_MAX_SPEED_P);
  stepper_p.setAcceleration(RUN_MAX_ACCELERATION_P);
  stepper_p.setSpeed(SPEED_P); 
}

void setRunningSpeed_c(void) {
  stepper_c.setMaxSpeed(MAX_SPEED_C);
  stepper_c.setAcceleration(ACCELERATION_C);
  stepper_c.setSpeed(SPEED_C); 
}
