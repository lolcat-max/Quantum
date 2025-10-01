// Arduino Calibration Code for Photonically Sensitive Charge-Emitting Liquid System

const int sensorPin = A0;      // Analog input from photodiode amplifier
const int laserPin = 3;        // PWM output to control laser diode
const int baselineSamples = 100; // Number of samples for baseline measurement

float baseline = 0;            // Baseline voltage level (no laser)
float gain = 1.0;              // Initial gain factor, adjustable during calibration

void setup() {
  Serial.begin(115200);
  pinMode(sensorPin, INPUT);
  pinMode(laserPin, OUTPUT);

  Serial.println("Starting Calibration...");
  delay(2000);

  // Step 1: Measure baseline with laser off
  analogWrite(laserPin, 0);   // Laser off
  baseline = measureBaseline();
  Serial.print("Baseline voltage (no laser): ");
  Serial.println(baseline, 4);

  // Step 2: Turn laser on at low power for reference
  analogWrite(laserPin, 64);  // 25% duty cycle PWM
  delay(1000);                // Wait stabilization

  float reference = measureSignal();
  Serial.print("Reference voltage (laser on low power): ");
  Serial.println(reference, 4);

  // Step 3: Calculate approximate gain needed to normalize signal
  gain = 1.0 / (reference - baseline);
  Serial.print("Calculated gain factor: ");
  Serial.println(gain, 4);

  Serial.println("Calibration Complete. Ready for measurement.");
}

void loop() {
  // Read raw sensor analog voltage
  float rawVoltage = analogRead(sensorPin) * (5.0 / 1023.0);

  // Apply baseline subtraction and gain adjustment
  float calibratedVoltage = (rawVoltage - baseline) * gain;

  // Output calibrated reading
  Serial.print("Calibrated signal: ");
  Serial.println(calibratedVoltage, 4);

  delay(100); // Sample every 100 ms
}

float measureBaseline() {
  float sum = 0;
  for (int i = 0; i < baselineSamples; i++) {
    int reading = analogRead(sensorPin);
    float voltage = reading * (5.0 / 1023.0);
    sum += voltage;
    delay(20);
  }
  return sum / baselineSamples;
}

float measureSignal() {
  float sum = 0;
  const int samples = 50;
  for (int i = 0; i < samples; i++) {
    int reading = analogRead(sensorPin);
    float voltage = reading * (5.0 / 1023.0);
    sum += voltage;
    delay(20);
  }
  return sum / samples;
}
apply_pulse(resonance_freq, 100);  // π/2 pulse
    Serial.println("  π/2 pulse applied");
    
    delay(50);  // Free evolution
    Serial.println("  Waiting 50ms...");
    
    apply_pulse(resonance_freq, 200);  // π pulse
    Serial.println("  π pulse applied (refocusing)");
    
    delay(50);  // Rephasing
    Serial.println("  Waiting 50ms...");
    
    float echo = measure_signal();
    Serial.print("  Echo signal: ");
    Serial.println(echo);
    
    if(echo > 0.1) {
        Serial.println("✓ QUANTUM COHERENCE DETECTED!");
    } else {
        Serial.println("✗ No echo - adjust parameters");
    }
}

void measure_state() {
    Serial.println("Measuring quantum state...");
    apply_pulse(resonance_freq, 10);
    delay(5);
    float state = measure_signal();
    
    Serial.print("State: ");
    Serial.println(state > 0.5 ? "|↓⟩ (down)" : "|↑⟩ (up)");
}
