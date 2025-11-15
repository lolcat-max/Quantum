/*
  Arduino SHA-256 Miner with Analog Input Smoothing
  Fixes PWM value inconsistency with averaging filter
*/

#include <Crypto.h>
#include <SHA256.h>

int sensorValue = 0;
int outputValue = 0;

String inputString = "";
bool stringComplete = false;
const int analogThreshold = 200; //sensitivity to black phosphorus (requires configuration) 
unsigned long lastPrintTime = 0;
const unsigned long printInterval = 100;
int work = 10;
// Mining variables
SHA256 sha256;
unsigned long nonce = 0;
const char* prefix = "test";
const int difficulty = 3;
bool miningEnabled = false;

void setup() {
  Serial.begin(9600);
  inputString.reserve(50);
  pinMode(A0, INPUT);

  pinMode(13, OUTPUT);
    

  Serial.println("Arduino SHA-256 Miner Ready");
}

void loop() {
  mineSHA256();
}

void mineSHA256() {
  float sensorValue = analogRead(A0);
  if (sensorValue > analogThreshold) {//sensitivity to black phosphorus (requires configuration) 
    for (int i = 0; i < work; i++) {
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
        digitalWrite(13, HIGH);

        Serial.println("\n*** BLOCK FOUND ***");
        Serial.print("Nonce: ");
        Serial.println(nonce + i);
        Serial.print("Hash: ");
        Serial.println(hashStr);
        Serial.println("*******************\n");
        nonce += work;
        return;
      }
      
      delay(2);//duration of barium titanate activation
      digitalWrite(13, LOW);
    }
  }
  nonce += work;
}
