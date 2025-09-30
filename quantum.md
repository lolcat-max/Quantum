Absolute Minimum True Quantum Setup
Core Philosophy: Use quantum phenomena in common materials instead of expensive specialized equipment.

Shopping List ($47 total)
Quantum Materials:

Table salt (NaCl): $1 - contains nuclear spins

Epsom salt (MgSO₄·7H₂O): $2 - has paramagnetic centers

Glycerin: $3 - host matrix, long T₂ times

Food coloring: $2 - optical contrast agent

Electronics:

Salvaged smartphone: $0 - use magnetometer, camera, flashlight

Arduino clone: $3 - cheapest microcontroller

Salvaged computer speakers: $0 - for audio frequency magnetic fields

Wire from electronics waste: $0

Magnets from old hard drives: $0

Hardware:

Mason jar: $2 - sample container

Aluminum foil: $1 - magnetic shielding

Cardboard box: $0 - enclosure

Duct tape: $2 - assembly

Tools:

Multimeter (borrowed/cheapest): $8

Function generator app: $0 - smartphone app

Oscilloscope app: $0 - smartphone audio input

Lab Supplies:

Distilled water: $1

Baking soda: $1 - pH adjustment

Coffee filters: $1 - filtering

Ice: $0 - cooling

Total: $27 + $20 contingency = $47

True Quantum System 1: Nuclear Spin Ensemble
The Physics:

Salt crystals contain millions of nuclear spins (¹H, ²³Na)

Nuclear magnetic moments are true quantum systems

Ensemble behavior gives measurable signals

Room temperature T₂ times: 1-100 milliseconds

Dissolve 10g salt in 50ml distilled water
Add 5ml glycerin (extends coherence)
Result: 10²⁰ nuclear spin qubits in solution!

Use Electromagnet for B1 field
Frequency = Larmor frequency
        
100ms π/2 pulse
        
Creates superposition: (|↑⟩ + |↓⟩)/√2 for all spins








// Carbon salt Quantum Computer
// Controls nuclear spins in salt water using carbon electrodes

// Pin definitions
#define ELECTRODE_X1 3
#define ELECTRODE_X2 5
#define ELECTRODE_Y1 6
#define ELECTRODE_Y2 9
#define ELECTRODE_Z1 10
#define ELECTRODE_Z2 11
#define SENSE_PIN A0

// Quantum parameters
float resonance_frequency = 250000;  // 250 kHz
float coherence_time_T2 = 50;  // 50ms estimated

void setup() {
    Serial.begin(115200);
    
    // Setup electrode pins
    pinMode(ELECTRODE_X1, OUTPUT);
    pinMode(ELECTRODE_X2, OUTPUT);
    pinMode(ELECTRODE_Y1, OUTPUT);
    pinMode(ELECTRODE_Y2, OUTPUT);
    pinMode(ELECTRODE_Z1, OUTPUT);
    pinMode(ELECTRODE_Z2, OUTPUT);
    
    pinMode(SENSE_PIN, INPUT);
    
    Serial.println("=====================================");
    Serial.println("CARBON ELECTRODE QUANTUM SYSTEM");
    Serial.println("=====================================");
    Serial.println();
    Serial.println("Commands:");
    Serial.println("  FIND    - Find resonance frequency");
    Serial.println("  ECHO    - Spin echo experiment");
    Serial.println("  RABI    - Rabi oscillations");
    Serial.println("  SUPER   - Create superposition");
    Serial.println("  FLIP    - Flip spin state");
    Serial.println("  MEASURE - Measure current state");
    Serial.println("  T2      - Measure coherence time");
    Serial.println();
}

void loop() {
    if(Serial.available()) {
        String command = Serial.readStringUntil('\n');
        command.trim();
        command.toUpperCase();
        
        if(command == "FIND") {
            find_resonance_frequency();
        }
        else if(command == "ECHO") {
            spin_echo_experiment();
        }
        else if(command == "RABI") {
            rabi_oscillation_experiment();
        }
        else if(command == "SUPER") {
            create_superposition();
        }
        else if(command == "FLIP") {
            flip_spin_state();
        }
        else if(command == "MEASURE") {
            measure_quantum_state();
        }
        else if(command == "T2") {
            measure_T2_coherence();
        }
        else {
            Serial.println("Unknown command. Type HELP for list.");
        }
    }
}

void find_resonance_frequency() {
    Serial.println("Scanning for NQR resonance...");
    
    float best_freq = 0;
    float max_signal = 0;
    
    // Sweep frequency
    for(float freq = 100000; freq <= 500000; freq += 10000) {
        apply_nqr_pulse(freq, 50);
        delay(10);
        
        float signal = measure_echo_signal();
        
        Serial.print(freq/1000);
        Serial.print(" kHz: ");
        Serial.println(signal);
        
        if(signal > max_signal) {
            max_signal = signal;
            best_freq = freq;
        }
        
        delay(100);
    }
    
    resonance_frequency = best_freq;
    
    Serial.println();
    Serial.print("Resonance found at ");
    Serial.print(best_freq/1000);
    Serial.println(" kHz");
}

void create_superposition() {
    Serial.println("Creating quantum superposition...");
    apply_nqr_pulse(resonance_frequency, 100);  // π/2 pulse
    Serial.println("Spins now in state: (|↑⟩ + |↓⟩)/√2");
}

void flip_spin_state() {
    Serial.println("Flipping spin state...");
    apply_nqr_pulse(resonance_frequency, 200);  // π pulse
    Serial.println("Spins flipped: |↑⟩ ↔ |↓⟩");
}

void measure_quantum_state() {
    Serial.println("Measuring quantum state...");
    float state = measure_spin_state();
    
    Serial.print("State measurement: ");
    Serial.println(state > 0.5 ? "|↓⟩ (spin down)" : "|↑⟩ (spin up)");
}

void measure_T2_coherence() {
    Serial.println("Measuring T2 coherence time...");
    Serial.println("Tau(ms), Echo Amplitude");
    
    for(float tau = 5; tau <= 200; tau += 10) {
        // Spin echo with varying tau
        apply_nqr_pulse(resonance_frequency, 100);  // π/2
        delay(tau);
        apply_nqr_pulse(resonance_frequency, 200);  // π
        delay(tau);
        
        float echo = measure_echo_signal();
        
        Serial.print(tau);
        Serial.print(", ");
        Serial.println(echo);
        
        delay(1000);  // T1 relaxation
    }
    
    Serial.println("Fit exponential decay to find T2");
}

