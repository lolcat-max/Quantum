/*
  Arduino SHA-256 Miner with Analog Input Smoothing
  Fixes PWM value inconsistency with averaging filter
*/

#include <Crypto.h>
#include <SHA256.h>

const int analogInPin = A0;
const int analogOutPin = 9;

int sensorValue = 0;
int outputValue = 0;

String inputString = "";
bool stringComplete = false;
const int analogThreshold = 280;
const int pwmThreshold = 70;
unsigned long lastPrintTime = 0;
const unsigned long printInterval = 100;

// Smoothing variables for analog input
const int numReadings = 2;
int readings[numReadings];
int readIndex = 0;
int total = 0;
int average = 0;

// Mining variables
SHA256 sha256;
unsigned long nonce = 0;
const char* prefix = "test";
const int difficulty = 3;
bool miningEnabled = false;

void setup() {
  Serial.begin(9600);
  inputString.reserve(50);
  pinMode(analogOutPin, OUTPUT);
  
  // Initialize smoothing array
  for (int i = 0; i < numReadings; i++) {
    readings[i] = 0;
  }
  
  Serial.println("Arduino SHA-256 Miner Ready");
}

void loop() {
  // Smooth analog input using running average
  total = total - readings[readIndex];
  readings[readIndex] = analogRead(analogInPin);
  total = total + readings[readIndex];
  readIndex = (readIndex + 1) % numReadings;
  average = total / numReadings;
  
  sensorValue = average;  // Use smoothed value
  outputValue = map(sensorValue, 0, 1023, 0, 255);
  analogWrite(analogOutPin, outputValue);

  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar;
    if (inChar == '\n') {
      stringComplete = true;
    }
  }

  if (stringComplete) {
    inputString.trim();
    if (inputString.equalsIgnoreCase("ON")) {
      analogWrite(analogOutPin, 255);
      Serial.println("LED turned ON");
    } else if (inputString.equalsIgnoreCase("OFF")) {
      analogWrite(analogOutPin, 0);
      Serial.println("LED turned OFF");
    } else if (inputString.equalsIgnoreCase("START")) {
      miningEnabled = true;
      Serial.println("Mining started");
    } else if (inputString.equalsIgnoreCase("STOP")) {
      miningEnabled = false;
      Serial.println("Mining stopped");
    }
    inputString = "";
    stringComplete = false;
  }

  // Your original threshold logic with stable PWM values
  if (sensorValue > analogThreshold) {
    miningEnabled = true;
  } else {
    miningEnabled = false;
    nonce += 100;
  }

  if (miningEnabled) {
    mineSHA256();
  }

  unsigned long currentMillis = millis();
  if (currentMillis - lastPrintTime >= printInterval) {
    Serial.print("Analog: ");
    Serial.print(sensorValue);
    Serial.print(" PWM: ");
    Serial.println(outputValue);
    lastPrintTime = currentMillis;
  }
}

void mineSHA256() {
  for (int i = 0; i < 100; i++) {
    String input = String(prefix) + String(nonce + i);
    
    sha256.reset();
    sha256.update(input.c_str(), input.length());
    
    uint8_t hash[32];
    sha256.finalize(hash, 32);
    
    String hashStr = "";
    for (int j = 0; j < 32; j++) {
      if (hash[j] < 16) hashStr += "0";
      hashStr += String(hash[j], HEX);
    }
    
    bool found = true;
    for (int j = 0; j < difficulty; j++) {
      if (hashStr.charAt(j) != '0') {
        found = false;
        break;
      }
    }
    
    if (found) {
      Serial.println("\n*** BLOCK FOUND ***");
      Serial.print("Nonce: ");
      Serial.println(nonce + i);
      Serial.print("Hash: ");
      Serial.println(hashStr);
      Serial.println("*******************\n");
      
      for (int k = 0; k < 3; k++) {
        analogWrite(analogOutPin, 255);
        delay(100);
        analogWrite(analogOutPin, 0);
        delay(100);
      }
      
      nonce += 100;
      return;
    }
    
    delay(2);
  }
  nonce += 100;
}
