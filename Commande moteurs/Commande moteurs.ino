// ODOP 2022

#include <AccelStepper.h>
#include <SoftwareSerial.h>

// variables moteurs

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

// variables bluetooth

#define rxPin 11 // Broche 11 en tant que RX, à raccorder sur TX du HC-05
#define txPin 10 // Broche 10 en tant que TX, à raccorder sur RX du HC-05

#include <EasyTransfer.h>

EasyTransfer _etIn, _etOut; 

// Structures for sending and receiving data in a fixed format
struct RECEIVE_DATA_STRUCTURE {
  int8_t command;
};

struct SEND_DATA_STRUCTURE {
  int8_t command;
  char value[64];
};

RECEIVE_DATA_STRUCTURE _rxData;
SEND_DATA_STRUCTURE _txData;

//Serial buffer
String readString = "";


void setup() {
  Serial.begin(BAUD_RATE);

  stepper_c.setCurrentPosition();
  stepper_p.setCurrentPosition();

  pinMode(rxPin, INPUT);
  pinMode(txPin, OUTPUT);
  mySerial.begin(9600);

  // Open USB connection (for debugging)
  Serial.println("USB/Serial connected");
  
  // Set reference to BT connection
  _etIn.begin(details(_rxData), &Serial);
  _etOut.begin(details(_txData), &Serial);
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
      long a =readString.substring(8).toInt();              // "move_p xx" step number starts at 8
      setRunningSpeed_p();
      rotateTo_p(a);
      Serial.println("move_p ok");
    }

    // Motion commande for moteur courroie
    if (readString.startsWith("move_c ")) {
      long a =readString.substring(8).toInt();   
      setRunningSpeed_c();
      rotateTo_p(a);
      Serial.println("move_p ok");
    }


    // Relative motion command in steps for moteur pivot
    if (readString.startsWith("rotate_p ")) {
      long a =readString.substring(10).toInt();             // "rotate_p xx" step number starts at 10
      setRunningSpeed_p();                                 
      rotate_p(a);
      Serial.println("rotate_p ok");
    }

    // Relative motion command in steps for moteur courroie
    if (readString.startsWith("rotate_c ")) {
      long a =readString.substring(10).toInt();
      setRunningSpeed_c();
      rotate_c(a);
      Serial.println("rotate_c ok");
    }

    if (readString.startswith("take_picture")){
      if (_etIn.receiveData())
      {
        if (_rxdata.command < CAMERAPRO_COMMAND_OK)
        {
          if (_currentMode != _rxdata.command)
          _currentMode = _rxdata.command;
        }
          if (_currentMode == MODE_CAMERAPRO)
          {
            _txData.command = CAMERAPRO_COMMAND_OK;
            strcpy(_txData.value, "Cmd Ok");
            _etOut.sendData();
            Serial.flush();
            delay(30);
          }
      }
  
      else:
      {
        // Run mode dependent function
        switch(_currentMode){
          case MODE_CAMERAPRO:
            handleCameraProFocusMode();
          break;
          default:
          // do nothing
          break;
        }
      }
    }

    // Report status
    if (readString.startsWith("status")) {
      Serial.print("Current position moteur poulie (steps): ");
      Serial.println(stepper_p.currentPosition());
      Serial.print("Current position moteur poulie (degrees): ");
      float curPosSteps=(float)stepper_p.currentPosition();
      float curPosDeg=curPosSteps/ANGLE_RANGE;
      Serial.println(curPosDeg);

      Serial.print("Current position moteur courroie (steps): ");
      Serial.println(stepper_c.currentPosition());
      Serial.print("Current position moteur courroie (degrees): ");
      float curPosSteps=(float)stepper_c.currentPosition();
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

// Actual rotation function, in steps, absolute for moteur courroie
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

void handleCameraProFocusMode()
{
  _txData.command = CAMERAPRO_CAMERA_CONTROL;  // The command.
  strcpy(_txData.value, "capture");            // The value for triggering image capture
  _etOut.sendData();
  Serial.flush();
  delay(1000);
}
