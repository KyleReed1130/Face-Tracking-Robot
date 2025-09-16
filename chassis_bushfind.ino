// ECEN4632 Intro to Digital Filtering
// Project 3
// Driver code for the face tracking chassis
// David Hamaker, Branden Vigil, Kyle Reed


//Variable Definitions
String data; // read in from python code
float Kp=1/2; // proportional controller

//Motor A - Left
const int PWM_PinA = 6;
const int Dir_PinA01 =4;
const int Dir_PinA02 =3;

//Motor B - Right
const int PWM_PinB = 5;
const int Dir_PinB01 =2;
const int Dir_PinB02 =7;


//Direction settings: to change which end is front, swap values
const int forward = 1;
const int backward = 0;

//Drive enumerations
enum direction {STILL, RIGHT, LEFT, FORWARD, BACKWARD};

//Drive function
void drive(direction dir){
  switch(dir){
    case STILL:
      //Left Wheel
      digitalWrite(PWM_PinA, 0);
      digitalWrite(Dir_PinA01, 0);
      digitalWrite(Dir_PinA02, 0);
      //Right Wheel
      digitalWrite(PWM_PinB, 0);
      digitalWrite(Dir_PinB01, 0);
      digitalWrite(Dir_PinB02, 0);
    break;

    case RIGHT:
      //Left Wheel
      digitalWrite(PWM_PinA, 150);
      digitalWrite(Dir_PinA01, backward);
      digitalWrite(Dir_PinA02, forward);
      //Right Wheel
      digitalWrite(PWM_PinB, 150);
      digitalWrite(Dir_PinB01, backward);
      digitalWrite(Dir_PinB02, forward);
    break;

    case LEFT:
      //Left Wheel
      digitalWrite(PWM_PinA, 150);
      digitalWrite(Dir_PinA01, forward);
      digitalWrite(Dir_PinA02, backward);
      //Right Wheel
      digitalWrite(PWM_PinB, 150);
      digitalWrite(Dir_PinB01, forward);
      digitalWrite(Dir_PinB02, backward);
    break;

    case FORWARD:
      //Left Wheel
      digitalWrite(PWM_PinA, 10);
      digitalWrite(Dir_PinA01, forward);
      digitalWrite(Dir_PinA02, backward);
      //Right Wheel
      digitalWrite(PWM_PinB, 10);
      digitalWrite(Dir_PinB01, backward);
      digitalWrite(Dir_PinB02, forward);
    break;

    case BACKWARD:
      //Left Wheel
      digitalWrite(PWM_PinA, 150);
      digitalWrite(Dir_PinA01, backward);
      digitalWrite(Dir_PinA02, forward);
      //Right Wheel
      digitalWrite(PWM_PinB, 150);
      digitalWrite(Dir_PinB01, forward);
      digitalWrite(Dir_PinB02, backward);
    break;
  }
}

void shakeNo(){
  for(int i=0;i<2;i++){
    drive(RIGHT);
    delay(100);
    drive(STILL);
    delay(100);
    drive(LEFT);
    delay(100);
    drive(STILL);
    delay(100);
  }
}

void dance(){
  drive(FORWARD);
  delay(100);
  drive(STILL);
  delay(100);
  drive(BACKWARD);
  delay(100);
  drive(STILL);
  delay(100);
}

void checkForBush(bool Bush){
  if(Bush){
    for(int i = 0;i<4;i++){
      dance();
    }
  }
  else{
    shakeNo();
    drive(LEFT);
    delay(1000);
    drive(STILL);
    delay(100);
  }
}

void setup() {
  pinMode(PWM_PinA,OUTPUT);
  pinMode(Dir_PinA01,OUTPUT);
  pinMode(Dir_PinA02,OUTPUT);
  pinMode(PWM_PinB,OUTPUT);
  pinMode(Dir_PinB01,OUTPUT);
  pinMode(Dir_PinB02,OUTPUT);

  // Start the serial communication with the same baud rate as the Python script (9600)
  Serial.begin(9600);
}


void loop() {
    if (Serial.available()) {
      // Read the incoming byte (this is the random number sent by the Python script)
      data = Serial.readStringUntil('\n');
      data.trim();

      int comma1 = data.indexOf(',');
      int comma2 = data.indexOf(',', comma1 + 1);
    
      // Extract the two booleans and the integer from the string
      String faceBool_str = data.substring(0, comma1);
      String bushBool_str = data.substring(comma1 + 1, comma2);
      String loc_str = data.substring(comma2 + 1);

      // Convert the strings to the appropriate types
      bool faceBool = faceBool_str.toInt();  // Convert to integer (0 or 1)
      bool bushBool = bushBool_str.toInt();  // Convert to integer (0 or 1)
      //bool bushBool = 1;// makes any face do the happy dance
      int loc_value = loc_str.toInt();  // Convert to int
      float loc_float = loc_str.toFloat();

      Serial.print("Facebool: ");
      Serial.println(faceBool);
      Serial.print("Bushbool: ");
      Serial.println(bushBool);
      Serial.println(loc_value);

      //if face
      if(faceBool==1){
        //face center
        if(abs(loc_value-300)<10){
          checkForBush(bushBool);
        }
        //if face is right
        else if(loc_value>=310){
          drive(RIGHT);
          delay((loc_float-300.0)*Kp);
          drive(STILL);
        }// else face is left
        else if(loc_float<=290){
          drive(LEFT);
          delay((300.0-loc_value)*Kp);
          drive(STILL);
        }
      }
      else if(faceBool==0){
        drive(LEFT);
        delay(200);
        drive(STILL);
        delay(200);
      }
    }
    
  //Test functions for driving
  //drive(STILL);// Uncomment and run code to stop the Chassis
  //drive(LEFT);
  //drive(RIGHT);
  //drive(BACKWARD);
  //drive(FORWARD);
  //dance();
  //shakeNo();

  //Loop speed delay
  delay(100);

}
