/*
  Arduino SHA-256 Miner with Analog Input and PWM Output
  Uses Crypto library by Rhys Weatherley
*/

#include <Crypto.h>
#include <SHA256.h>

const int analogInPin = A0;
const int analogOutPin = 9;

int sensorValue = 0;
int outputValue = 0;

String inputString = "";
bool stringComplete = false;

const int pwmThreshold = 25;
unsigned long lastPrintTime = 0;
const unsigned long printInterval = 100;

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
  
  Serial.println("Arduino SHA-256 Miner Ready");
}

void loop() {
  sensorValue = analogRead(analogInPin);
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

  if (outputValue > pwmThreshold) {
    miningEnabled = true;
  } else {
    miningEnabled = false;
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
    String input = String(prefix) + String(nonce);
    
    // Compute SHA-256 hash using Rhys library
    sha256.reset();
    sha256.update(input.c_str(), input.length());
    
    uint8_t hash[32];
    sha256.finalize(hash, 32);  // Correct syntax for Rhys library
    
    // Convert hash to hex string
    String hashStr = "";
    for (int j = 0; j < 32; j++) {
      if (hash[j] < 16) hashStr += "0";
      hashStr += String(hash[j], HEX);
    }
    
    // Check difficulty (leading zeros)
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
      Serial.println(nonce);
      Serial.print("Hash: ");
      Serial.println(hashStr);
      Serial.println("*******************\n");
      
      // Flash LED
      for (int k = 0; k < 3; k++) {
        analogWrite(analogOutPin, 255);
        delay(1);
        analogWrite(analogOutPin, 0);
        delay(1);
      }
      
      nonce = 0;
      return;
    }
    
    nonce++;
  }
}
