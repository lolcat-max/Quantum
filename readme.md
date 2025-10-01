# Photonically Sensitive Charge-Emitting Liquid Quantum Demo

This project demonstrates dynamic quantum coherence and charge emission in a Room-Temperature Ionic Liquid (RTIL)-based photonic system inside an optical cavity. The system converts photon gas coherence fluctuations into measurable electrical signals via a photodiode and transimpedance amplifier, controlled and read out through an Arduino microcontroller.

***

## Features

- Uses RTIL as a photonically sensitive liquid generating charge carriers on optical excitation.  
- Employs an optical cavity with diffuser to sustain photon gas modes and enhance coherence.  
- Converts photonic coherence into electrical signals using a photodiode + transimpedance amplifier.  
- Arduino-based control of laser modulation and real-time calibration with continuous data acquisition.  
- Tunable coherence dynamics by adjusting laser power, temperature, and environmental factors.  
- Educational and research platform for quantum coherence and photonic liquid state phenomena.

***

## Components

| Component                        | Quantity | Estimated Cost | Notes                       |
|---------------------------------|----------|----------------|-----------------------------|
| Room-Temperature Ionic Liquid (RTIL) | 1 vial   | $10+           | Photoconductive medium       |
| Optical Cavity Components (mirrors, diffuser) | Set      | $10            | For optical mode control     |
| Low-power Laser Diode or LED    | 1        | $10            | Photon source                |
| Photodiode or Phototransistor   | 1        | $5             | Fast, for charge conversion  |
| Operational Amplifier           | 1        | $5             | Builds transimpedance amplifier |
| Arduino Nano or Compatible      | 1        | $3             | Microcontroller              |
| Breadboard & Wiring             | Various  | $5             | Electronics assembly parts   |

***

## Assembly Overview

1. Place two RTIL vats within the cavity.  
2. Mount the laser diode to direct light into each cavity; place photodiode for light collection.  
3. Build and wire transimpedance amplifier converting photocurrent to voltage.  
4. Connect amplifier output to Arduino analog input (A0) and laser control to PWM pin (D3).  
5. Upload provided Arduino code for calibration and continuous measurement.  
6. Modulate laser intensity and monitor calibrated charge output reflecting coherence.

***

## Arduino Code Highlights

- Performs baseline and low-power reference signal calibration.  
- Calculates and applies gain for normalized signal output.  
- Continuously reads sensor voltage, applies calibration, and sends data over serial.  
- Generates PWM signal to control laser modulation dynamically.

***

## Using Temperature for Coherence Control

- Use cooling/heating elements to adjust coherence time and ionic mobility in RTIL.  
- Monitor how charge signals vary with temperature to study decoherence and thermal effects.

***

## Applications

- Hands-on exploration of quantum coherence and photonic liquids.  
- Experimental platform for quantum measurement and decoherence studies.  
- Educational tool for photonics, quantum materials, and liquid state physics.

***

## License

MIT License — Share and adapt freely.

***

This README is designed to guide users through building and experimenting with your RTIL photonically sensitive, charge-emitting quantum demo, highlighting key components, assembly, coding, and experimental considerations
