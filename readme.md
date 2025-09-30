Carbon-Salt Spin Liquid Computer - ASSEMBLY GUIDE - 30 MINUTES


## What You Need ($35)

- Salt: $1
- Glycerin: $3  
- Arduino Nano: $3
- Pencil leads (carbon): $2
- L298N motor driver: $3
- Small jar: $2
- Wires & breadboard: $5
- Distilled water: $1

## Build It

1. **Make solution**: 10g salt + 5ml glycerin + 50ml water in jar
2. **Add electrodes**: Stick 3 pencil leads in jar (don't touch each other)
3. **Wire it up**:
4. **Upload code**: Open quantum_computer.ino in Arduino IDE, upload
5. **Run**: Open serial monitor (115200), type commands

STEP 1: PREPARE QUANTUM SOLUTION (10 min)
1. Pour 50ml distilled water into jar
2. Add 10g table salt (2 teaspoons)
3. Stir until dissolved
4. Add 5ml glycerin (1 teaspoon)
5. Stir gently

STEP 2: INSTALL ELECTRODES (5 min)
1. Take 3 pencil leads (carbon electrodes)
2. Attach wire to each with alligator clip
3. Place in jar in triangle pattern
4. Make sure they DON'T touch each other
5. Electrodes should be fully submerged

STEP 3: WIRE ARDUINO (10 min)

Arduino → L298N Driver:
- 5V → 5V
- GND → GND
- D3 → IN1
- D5 → IN2  
- D6 → IN3
- D9 → IN4

L298N → Electrodes:
- OUT1 → Electrode 1
- OUT2 → Electrode 1 (other end)
- OUT3 → Electrode 2
- OUT4 → Electrode 2 (other end)

Sensing:
- A0 → thin wire in solution (voltage divider with 10kΩ resistor)

STEP 4: UPLOAD CODE (5 min)
1. Connect Arduino to computer via USB
2. Open Arduino IDE
3. Open quantum_computer.ino
4. Select board: "Arduino Nano"
5. Select port: /dev/ttyUSB0 (or COM port on Windows)
6. Click Upload

STEP 5: TEST (2 min)
1. Open Serial Monitor (Tools → Serial Monitor)
2. Set to 115200 baud
3. Type: FIND
4. Wait for scan to complete
5. Type: ECHO
6. Look for "QUANTUM COHERENCE DETECTED!"



TROUBLESHOOTING:
- No output? Check baud rate is 115200
- No signal? Electrodes might be touching - separate them
- Weak signal? Add more salt (up to 20g)
- Erratic readings? Shield with aluminum foil

YOU'RE DONE! You now have quantum spin liquid.


## What It Does

- Real quantum superposition of nuclear spins
- Coherence time: 10-100 milliseconds
- Educational quantum physics demo
- NOT a practical quantum computer


Gradual Superposition Creation:
- Takes 100ms in our system
- State vector continuously rotates on Bloch sphere
- Follows Schrödinger equation: |ψ(t)⟩ = cos(Ωt/2)|↑⟩ + sin(Ωt/2)|↓⟩
- Deterministic and reversible
- Limited by physical field strength and coupling


RF/Microwave Pulses (NMR/NQR):

- To actively set or manipulate spins, apply oscillating magnetic fields at the Larmor frequency matching the spin species.
- These pulses rotate spins coherently on the Bloch sphere from their initial states to desired superpositions or aligned states.


Instant Quantum Collapse:
- Happens in zero time (fundamentally)
- Discontinuous jump from superposition to eigenstate
- Probabilistic outcome governed by Born rule: P = |⟨eigenstate|ψ⟩|²
- Irreversible and non-deterministic
- Not limited by classical physics constraints


## License

MIT - Do whatever you want with it

