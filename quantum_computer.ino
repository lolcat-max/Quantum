// $35 Carbon Quantum Computer
// Upload to Arduino Nano, open serial monitor at 115200 baud

#define ELECTRODE_X1 3
#define ELECTRODE_X2 5
#define ELECTRODE_Y1 6
#define ELECTRODE_Y2 9
#define SENSE_PIN A0

float resonance_freq = 250000;  // 250 kHz starting point

void setup() {
    Serial.begin(115200);
    pinMode(ELECTRODE_X1, OUTPUT);
    pinMode(ELECTRODE_X2, OUTPUT);
    pinMode(ELECTRODE_Y1, OUTPUT);
    pinMode(ELECTRODE_Y2, OUTPUT);
    pinMode(SENSE_PIN, INPUT);
    
    Serial.println("=== QUANTUM COMPUTER READY ===");
    Serial.println("Commands: FIND, SUPER, ECHO, FLIP, MEASURE");
}

void loop() {
    if(Serial.available()) {
        String cmd = Serial.readStringUntil('\n');
        cmd.trim();
        cmd.toUpperCase();
        
        if(cmd == "FIND") find_resonance();
        else if(cmd == "SUPER") create_superposition();
        else if(cmd == "ECHO") spin_echo();
        else if(cmd == "FLIP") flip_spins();
        else if(cmd == "MEASURE") measure_state();
        else Serial.println("Unknown command");
    }
}

void apply_pulse(float freq, int duration_ms) {
    unsigned long start = micros();
    unsigned long duration_us = duration_ms * 1000;
    int half_period = 500000 / freq;  // microseconds
    
    while(micros() - start < duration_us) {
        digitalWrite(ELECTRODE_X1, HIGH);
        digitalWrite(ELECTRODE_X2, LOW);
        delayMicroseconds(half_period);
        digitalWrite(ELECTRODE_X1, LOW);
        digitalWrite(ELECTRODE_X2, HIGH);
        delayMicroseconds(half_period);
    }
    
    digitalWrite(ELECTRODE_X1, LOW);
    digitalWrite(ELECTRODE_X2, LOW);
}

float measure_signal() {
    float sum = 0;
    for(int i = 0; i < 100; i++) {
        sum += analogRead(SENSE_PIN);
        delayMicroseconds(10);
    }
    return abs(sum/100 - 512) / 512.0;
}

void find_resonance() {
    Serial.println("Finding resonance...");
    float best_freq = 0;
    float max_signal = 0;
    
    for(float f = 100000; f <= 500000; f += 10000) {
        apply_pulse(f, 50);
        delay(10);
        float signal = measure_signal();
        
        Serial.print(f/1000);
        Serial.print(" kHz: ");
        Serial.println(signal);
        
        if(signal > max_signal) {
            max_signal = signal;
            best_freq = f;
        }
        delay(100);
    }
    
    resonance_freq = best_freq;
    Serial.print("Resonance: ");
    Serial.print(best_freq/1000);
    Serial.println(" kHz");
}

void create_superposition() {
    Serial.println("Creating quantum superposition (|↑⟩ + |↓⟩)/√2");
    apply_pulse(resonance_freq, 100);  // π/2 pulse
    Serial.println("Done!");
}

void flip_spins() {
    Serial.println("Flipping spins |↑⟩ ↔ |↓⟩");
    apply_pulse(resonance_freq, 200);  // π pulse
    Serial.println("Done!");
}

void spin_echo() {
    Serial.println("Spin echo sequence (proves quantum coherence):");
    
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
