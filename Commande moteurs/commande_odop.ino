// ODOP 2022

#include <AccelStepper.h>
#include <SoftwareSerial.h>

// variables moteurs

#define dirPin_c 2 // moteur de la courroie
#define stepPin_c 3 // moteur de la courroie
#define dirPin_p 4 // moteur de la pivot
#define stepPin_p 5 // moteur de la pivot
#define motorInterfaceType 1

#define BAUD_RATE 9600

#define MAX_SPEED_P 100  // à adapter
#define ACCELERATION_P 50 // à adapter
#define SPEED_P 100

#define MAX_SPEED_C 500  // à adapter
#define ACCELERATION_C 100 // à adapter
#define SPEED_C 500

#define ANGLE_RANGE  17.7777777778f //nombre de pas par degré (microstep 1/32e de pas)

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

// CameraPro commands
#define MODE_UNKOWN              0               // Unkown state (default)
#define MODE_CAMERAPRO           1               // This command is sent by CameraPro when it is ready to receive commands.

#define CAMERAPRO_COMMAND_OK	20
#define CAMERAPRO_COMMAND_FAILED	21
#define CAMERAPRO_CAMERA_CONTROL	23
#define CAMERAPRO_CAMERA_MODE	24
#define CAMERAPRO_GET_CAPTURED_IMAGE	25       // Only supported for Wifi
#define CAMERAPRO_EFFECT_MODE	26
#define CAMERAPRO_EXPOSURE_COMPENSATION	27
#define CAMERAPRO_FLASH_MODE	29
#define CAMERAPRO_FOCUS_MODE	30
#define CAMERAPRO_FOCUS_POSITION_X	31
#define CAMERAPRO_FOCUS_POSITION_Y	32
#define CAMERAPRO_IMAGECONTROLS_BRIGHTNESS	33
#define CAMERAPRO_IMAGECONTROLS_CONTRAST	34
#define CAMERAPRO_IMAGECONTROLS_SATURATION	35
#define CAMERAPRO_IMAGECONTROLS_SHARPNESS	36
#define CAMERAPRO_ISO_VALUE	37
#define CAMERAPRO_SCENE_MODE	38
#define CAMERAPRO_RESOLUTION	39
#define CAMERAPRO_SWITCH_CAMERA	40
#define CAMERAPRO_WHITEBALANCE_MODE	41
#define CAMERAPRO_ZOOM	42
#define CAMERAPRO_ANTIBANDING_MODE	43
#define CAMERAPRO_METERING_MODE	44
#define CAMERAPRO_EXPOSURE_LOCK	45

int8_t _currentMode = MODE_UNKOWN;


void setup() {
  Serial.begin(BAUD_RATE);

  stepper_c.setCurrentPosition(0);
  stepper_p.setCurrentPosition(0);

  pinMode(rxPin, INPUT);
  pinMode(txPin, OUTPUT);

  // Open USB connection (for debugging)
  Serial.println("USB/Serial connected");
  
  // Set reference to BT connection
  _etIn.begin(details(_rxData), &Serial);
  _etOut.begin(details(_txData), &Serial);

  Serial.println("Controller ready");
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

    // Relative motion command in steps for moteur pivot
    if (readString.startsWith("rotate_p ")) {
      long a =readString.substring(9).toInt();             // "rotate_p xx" step number starts at 9
      setRunningSpeed_p();                                 
      rotate_p(a);
      Serial.println("rotate_p : success"); 
    }

    // Relative motion command in steps for moteur courroie
    if (readString.startsWith("rotate_c ")) {
      long a =readString.substring(9).toInt();
      setRunningSpeed_c();
      rotate_c(a);
      Serial.println("rotate_c : success");
    }

    if (readString.startsWith("take_picture")){
      if (_etIn.receiveData())
      {
        if (_rxData.command < CAMERAPRO_COMMAND_OK)
        {
          if (_currentMode != _rxData.command)
          _currentMode = _rxData.command;
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
  
    else
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
      Serial.println('take_picture : success');
    }

    // Report status
    if (readString.startsWith("status")) {
      Serial.print("Current position moteur poulie (steps): ");
      Serial.println(stepper_p.currentPosition());
      Serial.print("Current position moteur poulie (degrees): ");
      float curPosStepsp=(float)stepper_p.currentPosition();
      float curPosDegp=curPosStepsp/ANGLE_RANGE;
      Serial.println(curPosDegp);

      Serial.print("Current position moteur courroie (steps): ");
      Serial.println(stepper_c.currentPosition());
      Serial.print("Current position moteur courroie (degrees): ");
      float curPosStepsc=(float)stepper_c.currentPosition();
      float curPosDegc =curPosStepsc/ANGLE_RANGE;
      Serial.println(curPosDegc);

      Serial.println("Status ok");
    }

    readString="";
  }
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
  stepper_p.setMaxSpeed(MAX_SPEED_P);
  stepper_p.setAcceleration(ACCELERATION_P);
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
