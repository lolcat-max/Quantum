"""
Quantum Entanglement & Wavefunction Collapse Simulator
Based on the entangled photon detection system with frequency-resolved measurement

This simulation demonstrates:
- Pulsed laser photon generation
- Entangled beamsplitter grating array (photon multiplier)
- Dual-frequency photodetection (2.5 GHz and 17 GHz)
- Wavefunction collapse measurement
- Quantum interference patterns
- Qubit state control
"""

import tkinter as tk
from tkinter import ttk
import numpy as np
import random
import math

class QuantumEntanglementSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Quantum Entanglement & Wavefunction Collapse Simulator")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1a1a1a')
        
        # Simulation state
        self.is_running = False
        self.photon_pairs = []
        self.max_photons = 20
        self.collapse_frequency = 0.0
        self.superposition_exists = True
        self.shot_count = 0
        self.detection_events_2_5ghz = []
        self.detection_events_17ghz = []
        self.interference_data = []
        
        # Qubit states (|0⟩ and |1⟩ amplitudes)
        self.qubit1_state = [1.0, 0.0]  # |0⟩
        self.qubit2_state = [1.0, 0.0]  # |0⟩
        self.qubit3_state = [1.0, 0.0]  # |0⟩
        
        self.setup_ui()
        self.animation_loop()
    
    def setup_ui(self):
        # Title
        title = tk.Label(self.root, text="Quantum Entanglement Measurement System", 
                        font=('Arial', 20, 'bold'), bg='#1a1a1a', fg='#00ff00')
        title.pack(pady=10)
        
        # Main canvas for visualization
        self.canvas = tk.Canvas(self.root, width=1350, height=600, bg='#0a0a0a', highlightthickness=0)
        self.canvas.pack(pady=10)
        
        # Control panel
        control_frame = tk.Frame(self.root, bg='#1a1a1a')
        control_frame.pack(pady=5)
        
        # Buttons
        self.start_btn = tk.Button(control_frame, text="Start Laser Pulse", 
                                   command=self.start_simulation, bg='#00ff00', fg='black',
                                   font=('Arial', 12, 'bold'), width=15)
        self.start_btn.grid(row=0, column=0, padx=5)
        
        self.stop_btn = tk.Button(control_frame, text="Stop", 
                                 command=self.stop_simulation, bg='#ff0000', fg='white',
                                 font=('Arial', 12, 'bold'), width=15)
        self.stop_btn.grid(row=0, column=1, padx=5)
        
        self.reset_btn = tk.Button(control_frame, text="Reset", 
                                  command=self.reset_simulation, bg='#ffaa00', fg='black',
                                  font=('Arial', 12, 'bold'), width=15)
        self.reset_btn.grid(row=0, column=2, padx=5)
        
        # Pulse mode
        self.pulse_mode = tk.StringVar(value="Single")
        tk.Label(control_frame, text="Mode:", bg='#1a1a1a', fg='white', 
                font=('Arial', 10)).grid(row=0, column=3, padx=5)
        single_rb = tk.Radiobutton(control_frame, text="Single Shot", variable=self.pulse_mode, 
                                   value="Single", bg='#1a1a1a', fg='white', 
                                   selectcolor='#333333', font=('Arial', 10))
        single_rb.grid(row=0, column=4, padx=5)
        continuous_rb = tk.Radiobutton(control_frame, text="Continuous", variable=self.pulse_mode, 
                                       value="Continuous", bg='#1a1a1a', fg='white',
                                       selectcolor='#333333', font=('Arial', 10))
        continuous_rb.grid(row=0, column=5, padx=5)
        
        # Info panel
        info_frame = tk.Frame(self.root, bg='#1a1a1a')
        info_frame.pack(pady=5)
        
        # Status labels
        self.shot_label = tk.Label(info_frame, text="Shots: 0", 
                                   font=('Arial', 12), bg='#1a1a1a', fg='#00ff00')
        self.shot_label.grid(row=0, column=0, padx=15)
        
        self.freq_label = tk.Label(info_frame, text="Collapse Frequency: 0.00 GHz", 
                                   font=('Arial', 12), bg='#1a1a1a', fg='#00ffff')
        self.freq_label.grid(row=0, column=1, padx=15)
        
        self.superpos_label = tk.Label(info_frame, text="Superposition: ACTIVE", 
                                      font=('Arial', 12), bg='#1a1a1a', fg='#ff00ff')
        self.superpos_label.grid(row=0, column=2, padx=15)
        
        self.detection_label = tk.Label(info_frame, text="2.5GHz: 0 | 17GHz: 0", 
                                       font=('Arial', 12), bg='#1a1a1a', fg='#ffff00')
        self.detection_label.grid(row=0, column=3, padx=15)
        
        # Qubit state display
        qubit_frame = tk.Frame(self.root, bg='#1a1a1a')
        qubit_frame.pack(pady=5)
        
        self.qubit1_label = tk.Label(qubit_frame, text="Q1: |0⟩", 
                                     font=('Arial', 11), bg='#1a1a1a', fg='#00ff88')
        self.qubit1_label.grid(row=0, column=0, padx=10)
        
        self.qubit2_label = tk.Label(qubit_frame, text="Q2: |0⟩", 
                                     font=('Arial', 11), bg='#1a1a1a', fg='#00ff88')
        self.qubit2_label.grid(row=0, column=1, padx=10)
        
        self.qubit3_label = tk.Label(qubit_frame, text="Q3: |0⟩", 
                                     font=('Arial', 11), bg='#1a1a1a', fg='#00ff88')
        self.qubit3_label.grid(row=0, column=2, padx=10)
        
        # Draw static components
        self.draw_components()
    
    def draw_components(self):
        # Component positions
        self.laser_pos = (100, 300)
        self.beamsplitter_pos = (350, 300)
        self.detector1_pos = (600, 200)  # 2.5 GHz
        self.detector2_pos = (600, 400)  # 17 GHz
        self.controller_pos = (600, 80)
        self.receiver_pos = (1150, 300)
        
        # Draw Pulsed Laser Source
        self.canvas.create_rectangle(50, 250, 150, 350, fill='#ff0000', outline='#ffff00', width=2)
        self.canvas.create_text(100, 280, text="Pulsed Laser", fill='white', font=('Arial', 10, 'bold'))
        self.canvas.create_text(100, 300, text="Source", fill='white', font=('Arial', 10, 'bold'))
        self.canvas.create_text(100, 330, text="(# of Shots)", fill='#ffff00', font=('Arial', 8))
        
        # Draw Entangled Beamsplitter Grating Array
        self.canvas.create_rectangle(300, 250, 400, 350, fill='#0066ff', outline='#00ffff', width=2)
        self.canvas.create_text(350, 270, text="Entangled", fill='white', font=('Arial', 9, 'bold'))
        self.canvas.create_text(350, 290, text="Beamsplitter", fill='white', font=('Arial', 9, 'bold'))
        self.canvas.create_text(350, 310, text="Grating Array", fill='white', font=('Arial', 9))
        self.canvas.create_text(350, 330, text="(Multiplier)", fill='#00ffff', font=('Arial', 8))
        
        # Draw 2.5 GHz Detector
        self.canvas.create_rectangle(540, 150, 660, 250, fill='#006600', outline='#00ff00', width=3)
        self.canvas.create_text(600, 175, text="2.5 GHz Electronic", fill='#00ff00', font=('Arial', 9, 'bold'))
        self.canvas.create_text(600, 195, text="Transparent", fill='white', font=('Arial', 8))
        self.canvas.create_text(600, 210, text="Photodetector", fill='white', font=('Arial', 8))
        self.canvas.create_text(600, 225, text="Grated Plate", fill='white', font=('Arial', 8))
        self.canvas.create_text(600, 240, text="(Qubit #1)", fill='#ffff00', font=('Arial', 8))
        
        # Draw 17 GHz Detector
        self.canvas.create_rectangle(540, 350, 660, 450, fill='#660066', outline='#ff00ff', width=3)
        self.canvas.create_text(600, 375, text="17 GHz Electronic", fill='#ff00ff', font=('Arial', 9, 'bold'))
        self.canvas.create_text(600, 395, text="Transparent", fill='white', font=('Arial', 8))
        self.canvas.create_text(600, 410, text="Photodetector", fill='white', font=('Arial', 8))
        self.canvas.create_text(600, 425, text="Grated Plate", fill='white', font=('Arial', 8))
        self.canvas.create_text(600, 440, text="(Qubit #1)", fill='#ffff00', font=('Arial', 8))
        
        # Draw Controller
        self.canvas.create_rectangle(510, 30, 690, 140, fill='#333333', outline='#ffffff', width=2)
        self.canvas.create_text(600, 55, text="Controller", fill='white', font=('Arial', 12, 'bold'))
        self.canvas.create_text(600, 80, text="(Qubit #1, #2 #3", fill='#ffff00', font=('Arial', 10))
        self.canvas.create_text(600, 100, text="etc)", fill='#ffff00', font=('Arial', 10))
        self.canvas.create_text(600, 120, text="State Management", fill='#00ff88', font=('Arial', 8))
        
        # Draw Receiver
        self.canvas.create_rectangle(1090, 240, 1210, 360, fill='#cc6600', outline='#ffaa00', width=3)
        self.canvas.create_text(1150, 265, text="Micro", fill='white', font=('Arial', 10, 'bold'))
        self.canvas.create_text(1150, 285, text="Photodiode", fill='white', font=('Arial', 10, 'bold'))
        self.canvas.create_text(1150, 305, text="(Wavefunction", fill='white', font=('Arial', 8))
        self.canvas.create_text(1150, 320, text="Collapse", fill='white', font=('Arial', 8))
        self.canvas.create_text(1150, 335, text="Resistant)", fill='white', font=('Arial', 8))
        self.canvas.create_text(1150, 350, text="(Receiver)", fill='#ffaa00', font=('Arial', 8))
        
        # Draw static connections
        # Laser to Beamsplitter
        self.canvas.create_line(150, 300, 300, 300, fill='#ffff00', width=3, arrow=tk.LAST, 
                               arrowshape=(12, 15, 5))
        
        # Beamsplitter to Detectors
        self.canvas.create_line(400, 280, 540, 200, fill='#00ffff', width=3, arrow=tk.LAST,
                               arrowshape=(12, 15, 5))
        self.canvas.create_line(400, 320, 540, 400, fill='#00ffff', width=3, arrow=tk.LAST,
                               arrowshape=(12, 15, 5))
        
        # Beamsplitter to lower path (for interference)
        self.canvas.create_line(350, 350, 350, 480, fill='#888888', width=2, dash=(5,5))
        self.canvas.create_line(350, 480, 850, 480, fill='#888888', width=2, dash=(5,5))
        
        # Controller connections to Detectors
        self.canvas.create_line(600, 140, 600, 150, fill='#888888', width=2, arrow=tk.BOTH)
        self.canvas.create_line(600, 250, 600, 350, fill='#888888', width=2, arrow=tk.BOTH)
        
        # Detectors to Receiver
        self.canvas.create_line(660, 200, 1090, 280, fill='#00ff00', width=3, arrow=tk.LAST,
                               arrowshape=(12, 15, 5))
        self.canvas.create_line(660, 400, 1090, 320, fill='#ff00ff', width=3, arrow=tk.LAST,
                               arrowshape=(12, 15, 5))
        
        # Draw interference screen area
        self.screen_x = 900
        self.canvas.create_rectangle(840, 150, 960, 480, fill='#000033', outline='#0066ff', width=3)
        self.canvas.create_text(900, 175, text="Interference", fill='#0066ff', font=('Arial', 10, 'bold'))
        self.canvas.create_text(900, 195, text="Screen", fill='#0066ff', font=('Arial', 10, 'bold'))
        self.canvas.create_text(900, 460, text="Pattern Analysis", fill='#00aaff', font=('Arial', 8))
    
    def start_simulation(self):
        self.is_running = True
        self.shot_count += 1
        self.generate_entangled_pair()
    
    def stop_simulation(self):
        self.is_running = False
    
    def reset_simulation(self):
        self.is_running = False
        self.photon_pairs = []
        self.shot_count = 0
        self.collapse_frequency = 0.0
        self.superposition_exists = True
        self.detection_events_2_5ghz = []
        self.detection_events_17ghz = []
        self.interference_data = []
        self.qubit1_state = [1.0, 0.0]
        self.qubit2_state = [1.0, 0.0]
        self.qubit3_state = [1.0, 0.0]
        self.canvas.delete('photon')
        self.canvas.delete('interference')
        self.canvas.delete('laser_pulse')
        self.update_labels()
    
    def generate_entangled_pair(self):
        if len(self.photon_pairs) < self.max_photons:
            # Create entangled photon pair with quantum correlations
            phase = random.uniform(0, 2 * math.pi)
            pair = {
                'photon1': {
                    'x': self.beamsplitter_pos[0], 
                    'y': self.beamsplitter_pos[1], 
                    'target': self.detector1_pos, 
                    'phase': phase, 
                    'detected': False,
                    'color': '#00ffff',
                    'freq': 2.5
                },
                'photon2': {
                    'x': self.beamsplitter_pos[0], 
                    'y': self.beamsplitter_pos[1], 
                    'target': self.detector2_pos, 
                    'phase': phase + math.pi,  # Entangled phase correlation
                    'detected': False,
                    'color': '#ff00ff',
                    'freq': 17.0
                },
                'entangled': True,
                'creation_time': self.shot_count
            }
            self.photon_pairs.append(pair)
            self.draw_laser_pulse()
    
    def draw_laser_pulse(self):
        # Animate laser pulse
        self.canvas.delete('laser_pulse')
        for i in range(5):
            self.canvas.create_oval(90-i*3, 290-i*3, 110+i*3, 310+i*3,
                                   outline='#ff0000', width=2, tags='laser_pulse')
    
    def update_photons(self):
        to_remove = []
        
        for pair in self.photon_pairs:
            for photon_key in ['photon1', 'photon2']:
                photon = pair[photon_key]
                if not photon['detected']:
                    # Move photon toward target detector
                    dx = photon['target'][0] - photon['x']
                    dy = photon['target'][1] - photon['y']
                    dist = math.sqrt(dx**2 + dy**2)
                    
                    if dist > 5:
                        # Smooth movement with slight quantum jitter
                        photon['x'] += dx * 0.05 + random.uniform(-0.5, 0.5)
                        photon['y'] += dy * 0.05 + random.uniform(-0.5, 0.5)
                    else:
                        # Photon reached detector - measurement event!
                        photon['detected'] = True
                        detection_time = self.shot_count + random.uniform(0, 0.1)
                        
                        if photon['target'] == self.detector1_pos:
                            self.detection_events_2_5ghz.append({
                                'phase': photon['phase'],
                                'time': detection_time,
                                'freq': 2.5
                            })
                            self.create_detection_flash(self.detector1_pos, '#00ff00')
                        else:
                            self.detection_events_17ghz.append({
                                'phase': photon['phase'],
                                'time': detection_time,
                                'freq': 17.0
                            })
                            self.create_detection_flash(self.detector2_pos, '#ff00ff')
                        
                        # Trigger measurement and wavefunction collapse
                        if pair['entangled']:
                            self.measure_and_collapse(pair, photon)
            
            # Check if both photons detected
            if pair['photon1']['detected'] and pair['photon2']['detected']:
                to_remove.append(pair)
                # Record interference data
                phase_diff = abs(pair['photon1']['phase'] - pair['photon2']['phase'])
                self.interference_data.append(phase_diff)
        
        # Remove fully detected pairs
        for pair in to_remove:
            self.photon_pairs.remove(pair)
        
        # Calculate collapse frequency
        self.calculate_collapse_frequency()
    
    def create_detection_flash(self, pos, color):
        # Visual feedback for detection event
        x, y = pos
        flash = self.canvas.create_oval(x-20, y-20, x+20, y+20,
                                        outline=color, width=3, tags='photon')
        self.root.after(200, lambda: self.canvas.delete(flash))
    
    def measure_and_collapse(self, pair, measured_photon):
        # Simulate quantum measurement and wavefunction collapse
        pair['entangled'] = False
        
        # The measurement of one photon instantaneously affects the other (entanglement)
        other_key = 'photon2' if measured_photon == pair['photon1'] else 'photon1'
        other_photon = pair[other_key]
        
        # Correlated measurement outcome due to entanglement
        if not other_photon['detected']:
            # The other photon's phase is now determined
            phase_correlation = math.pi  # Anti-correlated for entangled pair
            other_photon['phase'] = measured_photon['phase'] + phase_correlation
        
        # Check if superposition exists based on detection patterns
        if len(self.detection_events_2_5ghz) > 3 and len(self.detection_events_17ghz) > 3:
            # Analyze phase coherence
            recent_phases_1 = [d['phase'] for d in self.detection_events_2_5ghz[-5:]]
            recent_phases_2 = [d['phase'] for d in self.detection_events_17ghz[-5:]]
            
            phase_std_1 = np.std(recent_phases_1) if len(recent_phases_1) > 1 else 0
            phase_std_2 = np.std(recent_phases_2) if len(recent_phases_2) > 1 else 0
            
            # If phases show coherence (low std), superposition exists
            if phase_std_1 < 1.5 and phase_std_2 < 1.5:
                self.superposition_exists = True
            else:
                # Decoherence observed
                self.superposition_exists = False
        
        # Update qubit states based on measurement
        self.update_qubit_states()
    
    def calculate_collapse_frequency(self):
        total_detections = len(self.detection_events_2_5ghz) + len(self.detection_events_17ghz)
        
        if total_detections > 0 and self.shot_count > 0:
            # Calculate weighted average frequency based on detection rates
            rate_2_5 = len(self.detection_events_2_5ghz) / self.shot_count
            rate_17 = len(self.detection_events_17ghz) / self.shot_count
            total_rate = rate_2_5 + rate_17
            
            if total_rate > 0:
                # Weighted frequency calculation
                self.collapse_frequency = (2.5 * rate_2_5 + 17.0 * rate_17) / total_rate
            
            # Add quantum interference effects
            if len(self.interference_data) > 5:
                interference_factor = np.mean(self.interference_data[-5:]) / (2 * math.pi)
                self.collapse_frequency *= (1 + 0.1 * interference_factor)
    
    def update_qubit_states(self):
        # Simulate quantum state evolution of qubits based on measurements
        
        # Qubit 1: Controlled by 2.5 GHz detector
        if len(self.detection_events_2_5ghz) > 0:
            last_phase = self.detection_events_2_5ghz[-1]['phase']
            angle = (last_phase % (2 * math.pi)) / 2
            self.qubit1_state = [math.cos(angle), math.sin(angle)]
        
        # Qubit 2: Controlled by 17 GHz detector
        if len(self.detection_events_17ghz) > 0:
            last_phase = self.detection_events_17ghz[-1]['phase']
            angle = (last_phase % (2 * math.pi)) / 2
            self.qubit2_state = [math.cos(angle), math.sin(angle)]
        
        # Qubit 3: Combination of both detectors
        if len(self.detection_events_2_5ghz) + len(self.detection_events_17ghz) > 0:
            combined_phase = 0
            if self.detection_events_2_5ghz:
                combined_phase += self.detection_events_2_5ghz[-1]['phase']
            if self.detection_events_17ghz:
                combined_phase += self.detection_events_17ghz[-1]['phase']
            angle = (combined_phase % (2 * math.pi)) / 2
            self.qubit3_state = [math.cos(angle), math.sin(angle)]
    
    def format_qubit_state(self, state):
        # Format qubit state as quantum notation
        alpha, beta = state
        alpha_prob = abs(alpha)**2
        beta_prob = abs(beta)**2
        
        if beta_prob < 0.01:
            return "|0⟩"
        elif alpha_prob < 0.01:
            return "|1⟩"
        else:
            return f"|ψ⟩ ({alpha_prob:.2f}|0⟩+{beta_prob:.2f}|1⟩)"
    
    def draw_photons(self):
        # Clear old photon visualizations
        self.canvas.delete('photon')
        
        for pair in self.photon_pairs:
            for photon_key in ['photon1', 'photon2']:
                photon = pair[photon_key]
                if not photon['detected']:
                    x, y = photon['x'], photon['y']
                    color = photon['color']
                    
                    # Draw photon with pulsing glow effect
                    pulse = abs(math.sin(self.shot_count * 0.2))
                    glow_size = 8 + pulse * 4
                    
                    # Outer glow
                    self.canvas.create_oval(x-glow_size, y-glow_size, 
                                          x+glow_size, y+glow_size, 
                                          fill='', outline=color, width=2, tags='photon')
                    # Middle glow
                    self.canvas.create_oval(x-5, y-5, x+5, y+5, 
                                          fill='', outline=color, width=2, tags='photon')
                    # Core
                    self.canvas.create_oval(x-3, y-3, x+3, y+3, 
                                          fill=color, outline='white', width=1, tags='photon')
                    
                    # Draw entanglement connection
                    if pair['entangled'] and photon_key == 'photon1':
                        other = pair['photon2']
                        if not other['detected']:
                            # Quantum entanglement visualization
                            for i in range(3):
                                offset = i * 3
                                self.canvas.create_line(
                                    photon['x'] + offset, photon['y'], 
                                    other['x'] - offset, other['y'],
                                    fill='#ffff00', width=1, dash=(3,3), 
                                    tags='photon')
                            
                            # Midpoint marker
                            mid_x = (photon['x'] + other['x']) / 2
                            mid_y = (photon['y'] + other['y']) / 2
                            self.canvas.create_text(mid_x, mid_y - 10, 
                                                   text="⚛", fill='#ffff00', 
                                                   font=('Arial', 12), tags='photon')
    
    def draw_interference_pattern(self):
        # Clear old interference pattern
        self.canvas.delete('interference')
        
        # Draw interference fringes based on detection data
        if len(self.interference_data) > 0:
            screen_height = 330  # Height of interference screen area
            num_lines = 50
            
            for i in range(num_lines):
                y = 200 + i * (screen_height / num_lines)
                
                # Calculate interference intensity
                intensity = 0
                
                # Contribution from 2.5 GHz detector
                for event in self.detection_events_2_5ghz[-10:]:
                    phase_contribution = math.cos(event['phase'] + i * 0.15)
                    intensity += phase_contribution
                
                # Contribution from 17 GHz detector
                for event in self.detection_events_17ghz[-10:]:
                    phase_contribution = math.cos(event['phase'] + i * 0.15 + math.pi/4)
                    intensity += phase_contribution
                
                # Normalize and convert to brightness
                total_events = len(self.detection_events_2_5ghz[-10:]) + len(self.detection_events_17ghz[-10:])
                if total_events > 0:
                    normalized_intensity = abs(intensity) / total_events
                    brightness = int(min(255, normalized_intensity * 255))
                else:
                    brightness = 0
                
                # Create color gradient (blue to white)
                color = f'#{brightness//4:02x}{brightness//2:02x}{min(255, brightness):02x}'
                
                # Draw fringe line
                line_width = 2 if brightness > 100 else 1
                self.canvas.create_line(850, y, 950, y, 
                                       fill=color, width=line_width, 
                                       tags='interference')
                
                # Add intensity markers at peaks
                if brightness > 200:
                    self.canvas.create_oval(948, y-2, 952, y+2,
                                           fill='#ffffff', outline='', 
                                           tags='interference')
    
    def update_labels(self):
        # Update all status labels
        self.shot_label.config(text=f"Shots: {self.shot_count}")
        self.freq_label.config(text=f"Collapse Frequency: {self.collapse_frequency:.2f} GHz")
        
        if self.superposition_exists:
            self.superpos_label.config(text="Superposition: ACTIVE ✓", fg='#ff00ff')
        else:
            self.superpos_label.config(text="Superposition: COLLAPSED ✗", fg='#ff0000')
        
        self.detection_label.config(
            text=f"2.5GHz: {len(self.detection_events_2_5ghz)} | "
                 f"17GHz: {len(self.detection_events_17ghz)}"
        )
        
        # Update qubit state labels
        self.qubit1_label.config(text=f"Q1: {self.format_qubit_state(self.qubit1_state)}")
        self.qubit2_label.config(text=f"Q2: {self.format_qubit_state(self.qubit2_state)}")
        self.qubit3_label.config(text=f"Q3: {self.format_qubit_state(self.qubit3_state)}")
    
    def animation_loop(self):
        # Main animation loop
        if self.is_running:
            self.update_photons()
            
            # Generate new pairs in continuous mode
            if self.pulse_mode.get() == "Continuous":
                if random.random() < 0.2 and len(self.photon_pairs) < self.max_photons:
                    self.shot_count += 1
                    self.generate_entangled_pair()
            elif len(self.photon_pairs) == 0:
                # Single shot mode - stop after all photons detected
                self.is_running = False
        
        self.draw_photons()
        self.draw_interference_pattern()
        self.update_labels()
        
        # Schedule next frame (20 FPS)
        self.root.after(50, self.animation_loop)


# Run the simulator
if __name__ == "__main__":
    root = tk.Tk()
    simulator = QuantumEntanglementSimulator(root)
    root.mainloop()
