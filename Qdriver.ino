/*
  Arduino SHA-256 Miner with Analog Input Smoothing
  Fixes PWM value inconsistency with averaging filter
  Modified to measure execution time of mineSHA256()
*/

#include <Crypto.h>
#include <SHA256.h>

int sensorValue = 0;
int outputValue = 0;

const int analogThreshold = 800; //sensitivity to black phosphorus (requires configuration) 
int work = 20000;

unsigned long nonce = 0;


void setup() {
  Serial.begin(9600);
  pinMode(A0, INPUT);
  pinMode(13, OUTPUT);
  Serial.println("Arduino SHA-256 Miner Ready");
}

void loop() {
  // Record the start time in microseconds
  unsigned long startTime = micros();

  processing();

  // Record the end time in microseconds
  unsigned long endTime = micros();

  // Calculate and print the elapsed time
  unsigned long elapsedTime = endTime - startTime;
  Serial.print("processing() execution time: ");
  Serial.print(elapsedTime);
  Serial.println(" microseconds");

}

void processing() {
  float sensorValue = analogRead(A0);
  for (int i = 0; i < work; i++) {
    if (sensorValue > analogThreshold) { //sensitivity to black phosphorus (requires configuration) 
      break; //early stopping
    }
    bool found = false;
    if (found) {
      digitalWrite(13, HIGH);
      Serial.println("\n*** Processing Done!***");
      Serial.print("Nonce: ");
      Serial.println(nonce + i);

      Serial.println("*******************\n");
      nonce += work;
      delay(2); //duration of barium titanate activation
      digitalWrite(13, LOW);
      return;
    }
  }
  nonce += work;
}

