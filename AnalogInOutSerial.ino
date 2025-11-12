/*
  Analog input, analog output, serial output

  Reads an analog input pin, maps the result to a range from 0 to 255 and uses
  the result to set the pulse width modulation (PWM) of an output pin.
  Also prints the results to the Serial Monitor.
*/

const int analogInPin = A0;    // Analog input pin with potentiometer
const int analogOutPin = 9;    // PWM output pin for LED

int sensorValue = 0;           // Analog reading
int outputValue = 0;           // PWM output value (0-255)
String inputString = "";       // For serial input
bool stringComplete = false;   // Flag for completed input string

void setup() {
  Serial.begin(9600);          // Initialize serial port
  inputString.reserve(50);     // Optional reserve buffer size
  pinMode(analogOutPin, OUTPUT);
}

void loop() {
  // Read analog input and map to PWM range
  sensorValue = analogRead(analogInPin);
  outputValue = map(sensorValue, 0, 1023, 0, 255);

  // Set PWM output accordingly
  analogWrite(analogOutPin, outputValue);

  // Read serial input if available
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar;
    if (inChar == '\n') {
      stringComplete = true;
    }
  }

  // If entire string received, process it
  if (stringComplete) {
    // Example action: if the input string is "ON", turn LED fully on
    inputString.trim();  // Remove whitespace and newlines
    if (inputString.equalsIgnoreCase("ON")) {
      analogWrite(analogOutPin, 255);  // Full brightness
      Serial.println("LED turned ON");
    } else if (inputString.equalsIgnoreCase("OFF")) {
      analogWrite(analogOutPin, 0);    // Turn off LED
      Serial.println("LED turned OFF");
    } else {
      Serial.print("Received: ");
      Serial.println(inputString);
    }
    // Reset input string and flag
    inputString = "";
    stringComplete = false;
  }
  
  // Print the current analog reading and PWM value every 100ms
  static unsigned long lastPrint = 0;
  if (millis() - lastPrint > 100) {
    Serial.print("Analog: ");
    Serial.print(sensorValue);
    Serial.print(" PWM: ");
    Serial.println(outputValue);
    lastPrint = millis();
  }
}
