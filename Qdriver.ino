/*
  Arduino SHA-256 Miner with Analog Input Smoothing
  Fixes PWM value inconsistency with averaging filter
  Modified to measure execution time of mineSHA256()
*/

#include <Crypto.h>
#include <SHA256.h>

int sensorValue = 0;
int outputValue = 0;

String inputString = "";
const int analogThreshold = 800; //sensitivity to black phosphorus (requires configuration) 
int work = 10;

// Mining variables
SHA256 sha256;
unsigned long nonce = 0;
const char* prefix = "test";
const int difficulty = 1;

void setup() {
  Serial.begin(9600);
  inputString.reserve(50);
  pinMode(A0, INPUT);
  pinMode(13, OUTPUT);
  Serial.println("Arduino SHA-256 Miner Ready");
}

void loop() {
  // Record the start time in microseconds
  unsigned long startTime = micros();

  mineSHA256();

  // Record the end time in microseconds
  unsigned long endTime = micros();

  // Calculate and print the elapsed time
  unsigned long elapsedTime = endTime - startTime;
  Serial.print("mineSHA256() execution time: ");
  Serial.print(elapsedTime);
  Serial.println(" microseconds");

}

void mineSHA256() {
  float sensorValue = analogRead(A0);
  for (int i = 0; i < work; i++) {
    if (sensorValue > analogThreshold) { //sensitivity to black phosphorus (requires configuration) 
      break; //early stopping
    }
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
      delay(2); //duration of barium titanate activation
      digitalWrite(13, LOW);
      return;
    }
  }
  nonce += work;
}
