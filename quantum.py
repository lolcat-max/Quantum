"""
Quantum Entanglement & Wavefunction Collapse Simulator
Complete Enhanced Version with Qiskit-style State Vectors and Probability Visualization

Author: AI Assistant
Date: October 2025
Description: Full quantum simulation with entangled photon detection, 
             state vector visualization, quantum gate operations, and measurement statistics
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import numpy as np
import random
import math
from datetime import datetime

class QuantumEntanglementSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Quantum Entanglement & Wavefunction Collapse Simulator - Complete Edition")
        self.root.geometry("1800x1000")
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
        
        # Qubit states (complex amplitudes for |0⟩ and |1⟩)
        self.qubit1_state = np.array([1.0+0j, 0.0+0j])  # |0⟩
        self.qubit2_state = np.array([1.0+0j, 0.0+0j])  # |0⟩
        self.qubit3_state = np.array([1.0+0j, 0.0+0j])  # |0⟩
        
        # Measurement statistics
        self.measurement_counts = {
            'qubit1': {'0': 0, '1': 0},
            'qubit2': {'0': 0, '1': 0},
            'qubit3': {'0': 0, '1': 0}
        }
        
        # Quantum gate configuration
        self.gate_config = {
            'qubit1': 'I',
            'qubit2': 'I',
            'qubit3': 'I',
            'coupling': False
        }
        
        self.setup_ui()
        self.update_state_displays()
        self.animation_loop()
    
    def setup_ui(self):
        """Setup the complete user interface"""
        # Main container
        main_container = tk.Frame(self.root, bg='#1a1a1a')
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel - visualization
        left_panel = tk.Frame(main_container, bg='#1a1a1a')
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Right panel - data and controls
        right_panel = tk.Frame(main_container, bg='#1a1a1a', width=500)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5)
        right_panel.pack_propagate(False)
        
        # Setup panels
        self.setup_visualization(left_panel)
        self.setup_data_panel(right_panel)
    
    def setup_visualization(self, parent):
        """Setup the visualization canvas and controls"""
        # Title
        title = tk.Label(parent, text="Quantum Entanglement Measurement System", 
                        font=('Arial', 18, 'bold'), bg='#1a1a1a', fg='#00ff00')
        title.pack(pady=5)
        
        # Main canvas
        self.canvas = tk.Canvas(parent, width=1150, height=600, bg='#0a0a0a', highlightthickness=0)
        self.canvas.pack(pady=5)
        
        # Control panel
        control_frame = tk.Frame(parent, bg='#1a1a1a')
        control_frame.pack(pady=5)
        
        self.start_btn = tk.Button(control_frame, text="Start Laser Pulse", 
                                   command=self.start_simulation, bg='#00ff00', fg='black',
                                   font=('Arial', 11, 'bold'), width=15)
        self.start_btn.grid(row=0, column=0, padx=5)
        
        self.stop_btn = tk.Button(control_frame, text="Stop", 
                                 command=self.stop_simulation, bg='#ff0000', fg='white',
                                 font=('Arial', 11, 'bold'), width=15)
        self.stop_btn.grid(row=0, column=1, padx=5)
        
        self.reset_btn = tk.Button(control_frame, text="Reset", 
                                  command=self.reset_simulation, bg='#ffaa00', fg='black',
                                  font=('Arial', 11, 'bold'), width=15)
        self.reset_btn.grid(row=0, column=2, padx=5)
        
        # Pulse mode
        self.pulse_mode = tk.StringVar(value="Single")
        tk.Label(control_frame, text="Mode:", bg='#1a1a1a', fg='white', 
                font=('Arial', 10)).grid(row=0, column=3, padx=5)
        tk.Radiobutton(control_frame, text="Single Shot", variable=self.pulse_mode, 
                      value="Single", bg='#1a1a1a', fg='white', 
                      selectcolor='#333333', font=('Arial', 9)).grid(row=0, column=4, padx=5)
        tk.Radiobutton(control_frame, text="Continuous", variable=self.pulse_mode, 
                      value="Continuous", bg='#1a1a1a', fg='white',
                      selectcolor='#333333', font=('Arial', 9)).grid(row=0, column=5, padx=5)
        
        # Info panel
        info_frame = tk.Frame(parent, bg='#1a1a1a')
        info_frame.pack(pady=5)
        
        self.shot_label = tk.Label(info_frame, text="Shots: 0", 
                                   font=('Arial', 11), bg='#1a1a1a', fg='#00ff00')
        self.shot_label.grid(row=0, column=0, padx=12)
        
        self.freq_label = tk.Label(info_frame, text="Collapse Frequency: 0.00 GHz", 
                                   font=('Arial', 11), bg='#1a1a1a', fg='#00ffff')
        self.freq_label.grid(row=0, column=1, padx=12)
        
        self.superpos_label = tk.Label(info_frame, text="Superposition: ACTIVE", 
                                      font=('Arial', 11), bg='#1a1a1a', fg='#ff00ff')
        self.superpos_label.grid(row=0, column=2, padx=12)
        
        self.detection_label = tk.Label(info_frame, text="2.5GHz: 0 | 17GHz: 0", 
                                       font=('Arial', 11), bg='#1a1a1a', fg='#ffff00')
        self.detection_label.grid(row=0, column=3, padx=12)
        
        # Draw static components
        self.draw_components()
    
    def setup_data_panel(self, parent):
        """Setup the data panel with tabs"""
        # Create notebook for tabs
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Tab 1: State Vectors
        state_tab = tk.Frame(notebook, bg='#1a1a1a')
        notebook.add(state_tab, text="State Vectors")
        
        # Tab 2: Gate Config
        gate_tab = tk.Frame(notebook, bg='#1a1a1a')
        notebook.add(gate_tab, text="Gate Config")
        
        # Tab 3: Output Log
        output_tab = tk.Frame(notebook, bg='#1a1a1a')
        notebook.add(output_tab, text="Output Log")
        
        self.setup_state_vectors_tab(state_tab)
        self.setup_gate_config_tab(gate_tab)
        self.setup_output_tab(output_tab)
    
    def setup_state_vectors_tab(self, parent):
        """Setup the state vectors visualization tab"""
        # Scrollable canvas for state vectors
        canvas_frame = tk.Frame(parent, bg='#1a1a1a')
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.state_canvas = tk.Canvas(canvas_frame, bg='#0a0a0a', 
                                      yscrollcommand=scrollbar.set, highlightthickness=0)
        self.state_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.state_canvas.yview)
        
        # Frame inside canvas
        self.state_frame = tk.Frame(self.state_canvas, bg='#0a0a0a')
        self.state_canvas.create_window((0, 0), window=self.state_frame, anchor='nw')
        
        # Title
        title = tk.Label(self.state_frame, text="Quantum State Vectors", 
                        font=('Arial', 13, 'bold'), bg='#0a0a0a', fg='#00ffff')
        title.pack(pady=10)
        
        # Qubit 1 State
        self.q1_state_frame = self.create_qubit_state_display(self.state_frame, "Qubit 1", '#00ff88')
        
        # Qubit 2 State
        self.q2_state_frame = self.create_qubit_state_display(self.state_frame, "Qubit 2", '#ff8800')
        
        # Qubit 3 State
        self.q3_state_frame = self.create_qubit_state_display(self.state_frame, "Qubit 3", '#ff0088')
        
        # Multi-qubit state vector
        separator = tk.Frame(self.state_frame, height=2, bg='#00ffff')
        separator.pack(fill=tk.X, pady=10, padx=20)
        
        tk.Label(self.state_frame, text="3-Qubit System State Vector", 
                font=('Arial', 12, 'bold'), bg='#0a0a0a', fg='#ffff00').pack(pady=5)
        
        self.system_state_text = tk.Text(self.state_frame, height=10, width=45,
                                         bg='#1a1a1a', fg='#00ff00',
                                         font=('Courier', 9))
        self.system_state_text.pack(pady=5, padx=10)
        
        # Measurement statistics
        separator2 = tk.Frame(self.state_frame, height=2, bg='#00ffff')
        separator2.pack(fill=tk.X, pady=10, padx=20)
        
        tk.Label(self.state_frame, text="Measurement Statistics", 
                font=('Arial', 12, 'bold'), bg='#0a0a0a', fg='#ffff00').pack(pady=5)
        
        self.stats_frame = tk.Frame(self.state_frame, bg='#0a0a0a')
        self.stats_frame.pack(pady=5)
        
        self.state_frame.update_idletasks()
        self.state_canvas.config(scrollregion=self.state_canvas.bbox("all"))
    
    def create_qubit_state_display(self, parent, label, color):
        """Create a display panel for a single qubit state"""
        frame = tk.LabelFrame(parent, text=label, bg='#1a1a1a', fg=color,
                             font=('Arial', 11, 'bold'), padx=10, pady=10)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        # State vector equation
        state_label = tk.Label(frame, text="|ψ⟩ = α|0⟩ + β|1⟩", 
                              bg='#1a1a1a', fg='white', font=('Courier', 10))
        state_label.pack(anchor='w')
        
        # Amplitude displays
        amp_frame = tk.Frame(frame, bg='#1a1a1a')
        amp_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(amp_frame, text="α = ", bg='#1a1a1a', fg='#00ffff',
                font=('Courier', 9)).grid(row=0, column=0, sticky='e')
        alpha_label = tk.Label(amp_frame, text="1.000 + 0.000j", bg='#1a1a1a', 
                              fg='#00ff00', font=('Courier', 9), width=20)
        alpha_label.grid(row=0, column=1, sticky='w', padx=5)
        
        tk.Label(amp_frame, text="β = ", bg='#1a1a1a', fg='#00ffff',
                font=('Courier', 9)).grid(row=1, column=0, sticky='e')
        beta_label = tk.Label(amp_frame, text="0.000 + 0.000j", bg='#1a1a1a', 
                             fg='#00ff00', font=('Courier', 9), width=20)
        beta_label.grid(row=1, column=1, sticky='w', padx=5)
        
        # Probability displays
        prob_frame = tk.Frame(frame, bg='#1a1a1a')
        prob_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(prob_frame, text="P(|0⟩) = |α|² = ", bg='#1a1a1a', fg='#ffff00',
                font=('Courier', 9)).grid(row=0, column=0, sticky='e')
        prob0_label = tk.Label(prob_frame, text="1.0000 (100.00%)", bg='#1a1a1a', 
                              fg='#00ff00', font=('Courier', 9, 'bold'))
        prob0_label.grid(row=0, column=1, sticky='w', padx=5)
        
        tk.Label(prob_frame, text="P(|1⟩) = |β|² = ", bg='#1a1a1a', fg='#ffff00',
                font=('Courier', 9)).grid(row=1, column=0, sticky='e')
        prob1_label = tk.Label(prob_frame, text="0.0000 (0.00%)", bg='#1a1a1a', 
                              fg='#00ff00', font=('Courier', 9, 'bold'))
        prob1_label.grid(row=1, column=1, sticky='w', padx=5)
        
        # Probability bars
        bar_frame = tk.Frame(frame, bg='#1a1a1a')
        bar_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(bar_frame, text="|0⟩:", bg='#1a1a1a', fg='white',
                font=('Arial', 8)).grid(row=0, column=0, sticky='e', padx=2)
        bar0_canvas = tk.Canvas(bar_frame, width=200, height=20, bg='#2a2a2a', highlightthickness=1)
        bar0_canvas.grid(row=0, column=1, padx=5)
        
        tk.Label(bar_frame, text="|1⟩:", bg='#1a1a1a', fg='white',
                font=('Arial', 8)).grid(row=1, column=0, sticky='e', padx=2)
        bar1_canvas = tk.Canvas(bar_frame, width=200, height=20, bg='#2a2a2a', highlightthickness=1)
        bar1_canvas.grid(row=1, column=1, padx=5)
        
        # Bloch sphere representation (phase)
        phase_label = tk.Label(frame, text="Phase: θ = 0.000, φ = 0.000", 
                              bg='#1a1a1a', fg='#ff00ff', font=('Courier', 9))
        phase_label.pack(pady=5)
        
        return {
            'frame': frame,
            'alpha_label': alpha_label,
            'beta_label': beta_label,
            'prob0_label': prob0_label,
            'prob1_label': prob1_label,
            'bar0_canvas': bar0_canvas,
            'bar1_canvas': bar1_canvas,
            'phase_label': phase_label
        }
    
    def setup_gate_config_tab(self, parent):
        """Setup the quantum gate configuration tab"""
        # Quantum Gate Configuration Section
        gate_frame = tk.LabelFrame(parent, text="Quantum Gate Operations", 
                                   bg='#1a1a1a', fg='#00ffff', font=('Arial', 11, 'bold'),
                                   padx=10, pady=10)
        gate_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Qubit 1 Gates
        tk.Label(gate_frame, text="Qubit 1:", bg='#1a1a1a', fg='#00ff88', 
                font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='w', pady=5)
        self.q1_gate = ttk.Combobox(gate_frame, values=['I', 'X', 'Y', 'Z', 'H', 'S', 'T', 'RX', 'RY', 'RZ'], 
                                    width=10, state='readonly')
        self.q1_gate.set('I')
        self.q1_gate.grid(row=0, column=1, padx=5)
        
        tk.Button(gate_frame, text="Apply", command=lambda: self.apply_gate('qubit1', self.q1_gate.get()),
                 bg='#00aa00', fg='white', font=('Arial', 9)).grid(row=0, column=2, padx=5)
        
        # Qubit 2 Gates
        tk.Label(gate_frame, text="Qubit 2:", bg='#1a1a1a', fg='#ff8800', 
                font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky='w', pady=5)
        self.q2_gate = ttk.Combobox(gate_frame, values=['I', 'X', 'Y', 'Z', 'H', 'S', 'T', 'RX', 'RY', 'RZ'], 
                                    width=10, state='readonly')
        self.q2_gate.set('I')
        self.q2_gate.grid(row=1, column=1, padx=5)
        
        tk.Button(gate_frame, text="Apply", command=lambda: self.apply_gate('qubit2', self.q2_gate.get()),
                 bg='#00aa00', fg='white', font=('Arial', 9)).grid(row=1, column=2, padx=5)
        
        # Qubit 3 Gates
        tk.Label(gate_frame, text="Qubit 3:", bg='#1a1a1a', fg='#ff0088', 
                font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky='w', pady=5)
        self.q3_gate = ttk.Combobox(gate_frame, values=['I', 'X', 'Y', 'Z', 'H', 'S', 'T', 'RX', 'RY', 'RZ'], 
                                    width=10, state='readonly')
        self.q3_gate.set('I')
        self.q3_gate.grid(row=2, column=1, padx=5)
        
        tk.Button(gate_frame, text="Apply", command=lambda: self.apply_gate('qubit3', self.q3_gate.get()),
                 bg='#00aa00', fg='white', font=('Arial', 9)).grid(row=2, column=2, padx=5)
        
        # Rotation angle for parametric gates
        separator = tk.Frame(gate_frame, height=2, bg='#333333')
        separator.grid(row=3, column=0, columnspan=3, sticky='ew', pady=10)
        
        tk.Label(gate_frame, text="Rotation Angle (θ):", bg='#1a1a1a', fg='white',
                font=('Arial', 9)).grid(row=4, column=0, sticky='w', pady=5)
        self.rotation_angle = tk.DoubleVar(value=np.pi/2)
        angle_scale = tk.Scale(gate_frame, from_=0, to=2*np.pi, resolution=0.1, orient=tk.HORIZONTAL,
                              variable=self.rotation_angle, bg='#1a1a1a', fg='white',
                              length=200)
        angle_scale.grid(row=4, column=1, columnspan=2, padx=5)
        
        self.angle_label = tk.Label(gate_frame, text="π/2 rad", bg='#1a1a1a', fg='#ffff00',
                                   font=('Courier', 9))
        self.angle_label.grid(row=5, column=1, columnspan=2, sticky='w', padx=5)
        
        # CNOT/Entanglement
        separator2 = tk.Frame(gate_frame, height=2, bg='#333333')
        separator2.grid(row=6, column=0, columnspan=3, sticky='ew', pady=10)
        
        self.entangle_var = tk.BooleanVar(value=False)
        tk.Checkbutton(gate_frame, text="Enable Qubit Coupling (CNOT)", variable=self.entangle_var,
                      bg='#1a1a1a', fg='#ffff00', selectcolor='#333333',
                      font=('Arial', 10), command=self.toggle_coupling).grid(row=7, column=0, 
                                                                             columnspan=3, sticky='w', pady=5)
        
        tk.Button(gate_frame, text="Apply CNOT(1→2)", 
                 command=lambda: self.apply_cnot(0, 1),
                 bg='#aa00aa', fg='white', font=('Arial', 9)).grid(row=8, column=0, columnspan=3, pady=2)
        
        tk.Button(gate_frame, text="Apply CNOT(2→3)", 
                 command=lambda: self.apply_cnot(1, 2),
                 bg='#aa00aa', fg='white', font=('Arial', 9)).grid(row=9, column=0, columnspan=3, pady=2)
        
        # Simulation Parameters
        separator3 = tk.Frame(gate_frame, height=2, bg='#333333')
        separator3.grid(row=10, column=0, columnspan=3, sticky='ew', pady=10)
        
        tk.Label(gate_frame, text="Max Photons:", bg='#1a1a1a', fg='white',
                font=('Arial', 9)).grid(row=11, column=0, sticky='w', pady=2)
        self.max_photons_var = tk.IntVar(value=20)
        tk.Spinbox(gate_frame, from_=5, to=50, textvariable=self.max_photons_var,
                  width=10, font=('Arial', 9)).grid(row=11, column=1, padx=5)
        
        tk.Label(gate_frame, text="Sensitivity:", bg='#1a1a1a', fg='white',
                font=('Arial', 9)).grid(row=12, column=0, sticky='w', pady=2)
        self.sensitivity_var = tk.DoubleVar(value=1.0)
        tk.Scale(gate_frame, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL,
                variable=self.sensitivity_var, bg='#1a1a1a', fg='white',
                length=150).grid(row=12, column=1, columnspan=2, padx=5)
        
        # Update angle display
        self.rotation_angle.trace('w', self.update_angle_display)
    
    def setup_output_tab(self, parent):
        """Setup the output log tab"""
        # Output text area
        output_frame = tk.Frame(parent, bg='#1a1a1a')
        output_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, width=50, height=30,
                                                     bg='#0a0a0a', fg='#00ff00',
                                                     font=('Courier', 9), wrap=tk.WORD)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Output controls
        btn_frame = tk.Frame(output_frame, bg='#1a1a1a')
        btn_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(btn_frame, text="Clear Output", command=self.clear_output,
                 bg='#aa0000', fg='white', font=('Arial', 9)).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Export Data", command=self.export_data,
                 bg='#0000aa', fg='white', font=('Arial', 9)).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Measure All", command=self.measure_all_qubits,
                 bg='#aa6600', fg='white', font=('Arial', 9)).pack(side=tk.LEFT, padx=2)
        
        # Initialize output
        self.log_output("=== Quantum Entanglement Simulator (Qiskit-style) ===")
        self.log_output(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.log_output("System initialized with 3 qubits in |000⟩ state\n")
    
    def draw_components(self):
        """Draw all quantum system components on canvas"""
        # Component positions
        self.laser_pos = (80, 300)
        self.beamsplitter_pos = (300, 300)
        self.detector1_pos = (520, 200)  # 2.5 GHz
        self.detector2_pos = (520, 400)  # 17 GHz
        self.controller_pos = (520, 80)
        self.receiver_pos = (1000, 300)
        
        # Draw Pulsed Laser Source
        self.canvas.create_rectangle(40, 260, 120, 340, fill='#ff0000', outline='#ffff00', width=2)
        self.canvas.create_text(80, 285, text="Pulsed", fill='white', font=('Arial', 9, 'bold'))
        self.canvas.create_text(80, 300, text="Laser", fill='white', font=('Arial', 9, 'bold'))
        self.canvas.create_text(80, 315, text="Source", fill='white', font=('Arial', 9, 'bold'))
        
        # Draw Entangled Beamsplitter
        self.canvas.create_rectangle(260, 260, 340, 340, fill='#0066ff', outline='#00ffff', width=2)
        self.canvas.create_text(300, 280, text="Entangled", fill='white', font=('Arial', 8, 'bold'))
        self.canvas.create_text(300, 295, text="Beamsplitter", fill='white', font=('Arial', 8, 'bold'))
        self.canvas.create_text(300, 310, text="Grating Array", fill='white', font=('Arial', 7))
        self.canvas.create_text(300, 325, text="(Multiplier)", fill='#00ffff', font=('Arial', 7))
        
        # Draw 2.5 GHz Detector
        self.canvas.create_rectangle(470, 160, 570, 240, fill='#006600', outline='#00ff00', width=2)
        self.canvas.create_text(520, 180, text="2.5 GHz", fill='#00ff00', font=('Arial', 9, 'bold'))
        self.canvas.create_text(520, 195, text="Photodetector", fill='white', font=('Arial', 7))
        self.canvas.create_text(520, 210, text="(Qubit #1)", fill='#ffff00', font=('Arial', 7))
        
        # Draw 17 GHz Detector
        self.canvas.create_rectangle(470, 360, 570, 440, fill='#660066', outline='#ff00ff', width=2)
        self.canvas.create_text(520, 380, text="17 GHz", fill='#ff00ff', font=('Arial', 9, 'bold'))
        self.canvas.create_text(520, 395, text="Photodetector", fill='white', font=('Arial', 7))
        self.canvas.create_text(520, 410, text="(Qubit #1)", fill='#ffff00', font=('Arial', 7))
        
        # Draw Controller
        self.canvas.create_rectangle(450, 40, 590, 120, fill='#333333', outline='#ffffff', width=2)
        self.canvas.create_text(520, 60, text="Controller", fill='white', font=('Arial', 10, 'bold'))
        self.canvas.create_text(520, 80, text="(Qubits #1,#2,#3)", fill='#ffff00', font=('Arial', 8))
        self.canvas.create_text(520, 100, text="Gate Control", fill='#00ff88', font=('Arial', 7))
        
        # Draw Receiver
        self.canvas.create_rectangle(960, 260, 1040, 340, fill='#cc6600', outline='#ffaa00', width=2)
        self.canvas.create_text(1000, 275, text="Micro", fill='white', font=('Arial', 8, 'bold'))
        self.canvas.create_text(1000, 290, text="Photodiode", fill='white', font=('Arial', 8, 'bold'))
        self.canvas.create_text(1000, 305, text="(Collapse", fill='white', font=('Arial', 7))
        self.canvas.create_text(1000, 320, text="Resistant)", fill='white', font=('Arial', 7))
        
        # Draw connections
        self.canvas.create_line(120, 300, 260, 300, fill='#ffff00', width=3, arrow=tk.LAST, arrowshape=(10, 12, 4))
        self.canvas.create_line(340, 280, 470, 200, fill='#00ffff', width=2, arrow=tk.LAST, arrowshape=(10, 12, 4))
        self.canvas.create_line(340, 320, 470, 400, fill='#00ffff', width=2, arrow=tk.LAST, arrowshape=(10, 12, 4))
        self.canvas.create_line(520, 120, 520, 160, fill='#888888', width=2, arrow=tk.BOTH)
        self.canvas.create_line(520, 240, 520, 360, fill='#888888', width=2, arrow=tk.BOTH)
        self.canvas.create_line(570, 200, 960, 280, fill='#00ff00', width=2, arrow=tk.LAST, arrowshape=(10, 12, 4))
        self.canvas.create_line(570, 400, 960, 320, fill='#ff00ff', width=2, arrow=tk.LAST, arrowshape=(10, 12, 4))
        
        # Draw interference screen
        self.canvas.create_rectangle(730, 180, 820, 420, fill='#000033', outline='#0066ff', width=2)
        self.canvas.create_text(775, 200, text="Interference", fill='#0066ff', font=('Arial', 8, 'bold'))
        self.canvas.create_text(775, 215, text="Screen", fill='#0066ff', font=('Arial', 8, 'bold'))
    
    def update_angle_display(self, *args):
        """Update rotation angle display"""
        angle = self.rotation_angle.get()
        if abs(angle - np.pi) < 0.1:
            self.angle_label.config(text="π rad")
        elif abs(angle - np.pi/2) < 0.1:
            self.angle_label.config(text="π/2 rad")
        elif abs(angle - np.pi/4) < 0.1:
            self.angle_label.config(text="π/4 rad")
        elif abs(angle - 2*np.pi) < 0.1:
            self.angle_label.config(text="2π rad")
        else:
            self.angle_label.config(text=f"{angle:.3f} rad")
    
    def apply_gate(self, qubit, gate):
        """Apply quantum gate to specified qubit with complex amplitudes"""
        self.gate_config[qubit] = gate
        
        # Gate matrices with complex numbers
        theta = self.rotation_angle.get()
        gates = {
            'I': np.array([[1, 0], [0, 1]], dtype=complex),
            'X': np.array([[0, 1], [1, 0]], dtype=complex),
            'Y': np.array([[0, -1j], [1j, 0]], dtype=complex),
            'Z': np.array([[1, 0], [0, -1]], dtype=complex),
            'H': np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2),
            'S': np.array([[1, 0], [0, 1j]], dtype=complex),
            'T': np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=complex),
            'RX': np.array([[np.cos(theta/2), -1j*np.sin(theta/2)],
                           [-1j*np.sin(theta/2), np.cos(theta/2)]], dtype=complex),
            'RY': np.array([[np.cos(theta/2), -np.sin(theta/2)],
                           [np.sin(theta/2), np.cos(theta/2)]], dtype=complex),
            'RZ': np.array([[np.exp(-1j*theta/2), 0],
                           [0, np.exp(1j*theta/2)]], dtype=complex)
        }
        
        if gate in gates:
            gate_matrix = gates[gate]
            
            if qubit == 'qubit1':
                self.qubit1_state = gate_matrix @ self.qubit1_state
            elif qubit == 'qubit2':
                self.qubit2_state = gate_matrix @ self.qubit2_state
            elif qubit == 'qubit3':
                self.qubit3_state = gate_matrix @ self.qubit3_state
            
            self.log_output(f"Applied {gate} gate to {qubit}")
            if gate in ['RX', 'RY', 'RZ']:
                self.log_output(f"  Rotation angle: {theta:.4f} rad")
            
            self.update_state_displays()
    
    def apply_cnot(self, control, target):
        """Apply CNOT gate between two qubits"""
        qubits = [self.qubit1_state, self.qubit2_state, self.qubit3_state]
        
        # Measure control qubit
        control_prob_1 = abs(qubits[control][1])**2
        
        # If control is in |1⟩ state, flip target
        if control_prob_1 > 0.5 or (control_prob_1 > 0.1 and random.random() < control_prob_1):
            # Apply X gate to target
            X = np.array([[0, 1], [1, 0]], dtype=complex)
            qubits[target] = X @ qubits[target]
            self.log_output(f"CNOT: Control Q{control+1} triggered flip on Q{target+1}")
        else:
            self.log_output(f"CNOT: Control Q{control+1} in |0⟩, no action on Q{target+1}")
        
        self.qubit1_state = qubits[0]
        self.qubit2_state = qubits[1]
        self.qubit3_state = qubits[2]
        
        self.update_state_displays()
    
    def measure_all_qubits(self):
        """Perform measurement on all qubits"""
        results = []
        
        for i, (qubit_state, qubit_name) in enumerate([(self.qubit1_state, 'Q1'),
                                                         (self.qubit2_state, 'Q2'),
                                                         (self.qubit3_state, 'Q3')]):
            prob_0 = abs(qubit_state[0])**2
            prob_1 = abs(qubit_state[1])**2
            
            # Perform measurement
            outcome = '0' if random.random() < prob_0 else '1'
            results.append(outcome)
            
            # Collapse state
            if outcome == '0':
                if i == 0:
                    self.qubit1_state = np.array([1.0+0j, 0.0+0j])
                elif i == 1:
                    self.qubit2_state = np.array([1.0+0j, 0.0+0j])
                else:
                    self.qubit3_state = np.array([1.0+0j, 0.0+0j])
                self.measurement_counts[f'qubit{i+1}']['0'] += 1
            else:
                if i == 0:
                    self.qubit1_state = np.array([0.0+0j, 1.0+0j])
                elif i == 1:
                    self.qubit2_state = np.array([0.0+0j, 1.0+0j])
                else:
                    self.qubit3_state = np.array([0.0+0j, 1.0+0j])
                self.measurement_counts[f'qubit{i+1}']['1'] += 1
        
        result_str = ''.join(results)
        self.log_output(f"Measurement result: |{result_str}⟩")
        self.log_output(f"  Q1→|{results[0]}⟩, Q2→|{results[1]}⟩, Q3→|{results[2]}⟩")
        
        self.update_state_displays()
    
    def update_state_displays(self):
        """Update all state vector displays"""
        # Update Qubit 1
        self.update_single_qubit_display(self.q1_state_frame, self.qubit1_state, '#00ff88')
        
        # Update Qubit 2
        self.update_single_qubit_display(self.q2_state_frame, self.qubit2_state, '#ff8800')
        
        # Update Qubit 3
        self.update_single_qubit_display(self.q3_state_frame, self.qubit3_state, '#ff0088')
        
        # Update 3-qubit system state
        self.update_system_state()
        
        # Update measurement statistics
        self.update_measurement_stats()
    
    def update_single_qubit_display(self, display_dict, state, color):
        """Update single qubit state display"""
        alpha, beta = state[0], state[1]
        
        # Update amplitude labels
        display_dict['alpha_label'].config(
            text=f"{alpha.real:.3f} + {alpha.imag:.3f}j"
        )
        display_dict['beta_label'].config(
            text=f"{beta.real:.3f} + {beta.imag:.3f}j"
        )
        
        # Calculate probabilities
        prob_0 = abs(alpha)**2
        prob_1 = abs(beta)**2
        
        # Update probability labels
        display_dict['prob0_label'].config(
            text=f"{prob_0:.4f} ({prob_0*100:.2f}%)"
        )
        display_dict['prob1_label'].config(
            text=f"{prob_1:.4f} ({prob_1*100:.2f}%)"
        )
        
        # Update probability bars
        bar0 = display_dict['bar0_canvas']
        bar1 = display_dict['bar1_canvas']
        
        bar0.delete('all')
        bar1.delete('all')
        
        bar_width_0 = int(prob_0 * 190)
        bar_width_1 = int(prob_1 * 190)
        
        bar0.create_rectangle(5, 5, 5+bar_width_0, 15, fill='#00ff00', outline='')
        bar1.create_rectangle(5, 5, 5+bar_width_1, 15, fill='#ff0000', outline='')
        
        # Calculate phase angles
        theta = np.arctan2(abs(beta), abs(alpha)) * 2
        phi = np.angle(beta) - np.angle(alpha)
        
        display_dict['phase_label'].config(
            text=f"Phase: θ={theta:.3f}, φ={phi:.3f}"
        )
    
    def update_system_state(self):
        """Update the full 3-qubit system state vector"""
        # Compute tensor product of all three qubits
        state_vector = np.kron(np.kron(self.qubit1_state, self.qubit2_state), self.qubit3_state)
        
        self.system_state_text.delete(1.0, tk.END)
        self.system_state_text.insert(tk.END, "Statevector |ψ⟩ (8 basis states):\n\n")
        
        basis_states = ['|000⟩', '|001⟩', '|010⟩', '|011⟩', 
                       '|100⟩', '|101⟩', '|110⟩', '|111⟩']
        
        for i, (amplitude, basis) in enumerate(zip(state_vector, basis_states)):
            prob = abs(amplitude)**2
            if prob > 0.001:
                self.system_state_text.insert(tk.END, 
                    f"{basis}: ({amplitude.real:.3f}{amplitude.imag:+.3f}j)\n")
                self.system_state_text.insert(tk.END, 
                    f"      P = {prob:.4f} ({prob*100:.2f}%)\n\n")
    
    def update_measurement_stats(self):
        """Update measurement statistics display"""
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        for i, qubit in enumerate(['qubit1', 'qubit2', 'qubit3']):
            counts = self.measurement_counts[qubit]
            total = counts['0'] + counts['1']
            
            if total > 0:
                frame = tk.Frame(self.stats_frame, bg='#1a1a1a', relief=tk.RIDGE, borderwidth=2)
                frame.pack(fill=tk.X, pady=5, padx=10)
                
                colors = ['#00ff88', '#ff8800', '#ff0088']
                tk.Label(frame, text=f"Qubit {i+1} Measurements ({total} total):", 
                        bg='#1a1a1a', fg=colors[i], font=('Arial', 9, 'bold')).pack(anchor='w', padx=5)
                
                tk.Label(frame, text=f"  |0⟩: {counts['0']} ({counts['0']/total*100:.1f}%)", 
                        bg='#1a1a1a', fg='#00ff00', font=('Courier', 8)).pack(anchor='w', padx=10)
                tk.Label(frame, text=f"  |1⟩: {counts['1']} ({counts['1']/total*100:.1f}%)", 
                        bg='#1a1a1a', fg='#ff0000', font=('Courier', 8)).pack(anchor='w', padx=10)
    
    def toggle_coupling(self):
        """Enable/disable qubit coupling"""
        self.gate_config['coupling'] = self.entangle_var.get()
        status = "ENABLED" if self.gate_config['coupling'] else "DISABLED"
        self.log_output(f"Qubit coupling {status}")
    
    def log_output(self, message):
        """Log message to output panel"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.output_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.output_text.see(tk.END)
    
    def clear_output(self):
        """Clear output text area"""
        self.output_text.delete(1.0, tk.END)
        self.log_output("Output cleared.")
    
    def export_data(self):
        """Export measurement data to file"""
        filename = f"quantum_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w') as f:
            f.write("=== Quantum Measurement Data Export ===\n")
            f.write(f"Timestamp: {datetime.now()}\n\n")
            f.write(f"Total Shots: {self.shot_count}\n")
            f.write(f"Collapse Frequency: {self.collapse_frequency:.4f} GHz\n\n")
            f.write(f"Qubit 1 State: {self.qubit1_state}\n")
            f.write(f"Qubit 2 State: {self.qubit2_state}\n")
            f.write(f"Qubit 3 State: {self.qubit3_state}\n\n")
            f.write(f"Measurement Statistics:\n")
            for qubit in ['qubit1', 'qubit2', 'qubit3']:
                f.write(f"  {qubit}: {self.measurement_counts[qubit]}\n")
            f.write(f"\n2.5 GHz Detections: {len(self.detection_events_2_5ghz)}\n")
            f.write(f"17 GHz Detections: {len(self.detection_events_17ghz)}\n")
        
        self.log_output(f"Data exported to {filename}")
    
    def start_simulation(self):
        """Start the quantum simulation"""
        self.is_running = True
        self.shot_count += 1
        self.max_photons = self.max_photons_var.get()
        self.generate_entangled_pair()
        self.log_output(f"Shot #{self.shot_count} initiated")
    
    def stop_simulation(self):
        """Stop the simulation"""
        self.is_running = False
        self.log_output("Simulation paused")
    
    def reset_simulation(self):
        """Reset all simulation parameters"""
        self.is_running = False
        self.photon_pairs = []
        self.shot_count = 0
        self.collapse_frequency = 0.0
        self.superposition_exists = True
        self.detection_events_2_5ghz = []
        self.detection_events_17ghz = []
        self.interference_data = []
        self.qubit1_state = np.array([1.0+0j, 0.0+0j])
        self.qubit2_state = np.array([1.0+0j, 0.0+0j])
        self.qubit3_state = np.array([1.0+0j, 0.0+0j])
        self.measurement_counts = {
            'qubit1': {'0': 0, '1': 0},
            'qubit2': {'0': 0, '1': 0},
            'qubit3': {'0': 0, '1': 0}
        }
        self.canvas.delete('photon')
        self.canvas.delete('interference')
        self.canvas.delete('laser_pulse')
        self.update_state_displays()
        self.update_labels()
        self.log_output("System reset - all qubits initialized to |000⟩")
    
    def generate_entangled_pair(self):
        """Generate an entangled photon pair"""
        if len(self.photon_pairs) < self.max_photons:
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
                    'phase': phase + math.pi,
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
        """Animate laser pulse"""
        self.canvas.delete('laser_pulse')
        for i in range(4):
            self.canvas.create_oval(72-i*2, 292-i*2, 88+i*2, 308+i*2,
                                   outline='#ff0000', width=2, tags='laser_pulse')
    
    def update_photons(self):
        """Update photon positions and handle detections"""
        to_remove = []
        
        for pair in self.photon_pairs:
            for photon_key in ['photon1', 'photon2']:
                photon = pair[photon_key]
                if not photon['detected']:
                    dx = photon['target'][0] - photon['x']
                    dy = photon['target'][1] - photon['y']
                    dist = math.sqrt(dx**2 + dy**2)
                    
                    if dist > 5:
                        photon['x'] += dx * 0.05 + random.uniform(-0.5, 0.5)
                        photon['y'] += dy * 0.05 + random.uniform(-0.5, 0.5)
                    else:
                        photon['detected'] = True
                        detection_time = self.shot_count + random.uniform(0, 0.1)
                        
                        if photon['target'] == self.detector1_pos:
                            self.detection_events_2_5ghz.append({
                                'phase': photon['phase'],
                                'time': detection_time,
                                'freq': 2.5
                            })
                            self.create_detection_flash(self.detector1_pos, '#00ff00')
                            self.log_output(f"2.5 GHz detection: φ={photon['phase']:.3f}")
                        else:
                            self.detection_events_17ghz.append({
                                'phase': photon['phase'],
                                'time': detection_time,
                                'freq': 17.0
                            })
                            self.create_detection_flash(self.detector2_pos, '#ff00ff')
                            self.log_output(f"17 GHz detection: φ={photon['phase']:.3f}")
                        
                        if pair['entangled']:
                            self.measure_and_collapse(pair, photon)
            
            if pair['photon1']['detected'] and pair['photon2']['detected']:
                to_remove.append(pair)
                phase_diff = abs(pair['photon1']['phase'] - pair['photon2']['phase'])
                self.interference_data.append(phase_diff)
                self.log_output(f"Pair complete: Δφ={phase_diff:.3f}")
        
        for pair in to_remove:
            self.photon_pairs.remove(pair)
        
        self.calculate_collapse_frequency()
    
    def create_detection_flash(self, pos, color):
        """Create visual flash effect at detector"""
        x, y = pos
        flash = self.canvas.create_oval(x-15, y-15, x+15, y+15,
                                        outline=color, width=3, tags='photon')
        self.root.after(200, lambda: self.canvas.delete(flash))
    
    def measure_and_collapse(self, pair, measured_photon):
        """Handle quantum measurement and wavefunction collapse"""
        pair['entangled'] = False
        
        other_key = 'photon2' if measured_photon == pair['photon1'] else 'photon1'
        other_photon = pair[other_key]
        
        if not other_photon['detected']:
            phase_correlation = math.pi
            other_photon['phase'] = measured_photon['phase'] + phase_correlation
        
        if len(self.detection_events_2_5ghz) > 3 and len(self.detection_events_17ghz) > 3:
            recent_phases_1 = [d['phase'] for d in self.detection_events_2_5ghz[-5:]]
            recent_phases_2 = [d['phase'] for d in self.detection_events_17ghz[-5:]]
            
            phase_std_1 = np.std(recent_phases_1) if len(recent_phases_1) > 1 else 0
            phase_std_2 = np.std(recent_phases_2) if len(recent_phases_2) > 1 else 0
            
            if phase_std_1 < 1.5 and phase_std_2 < 1.5:
                self.superposition_exists = True
            else:
                self.superposition_exists = False
                self.log_output("Wavefunction collapse detected!")
        
        self.update_qubit_states()
    
    def calculate_collapse_frequency(self):
        """Calculate wavefunction collapse frequency"""
        total_detections = len(self.detection_events_2_5ghz) + len(self.detection_events_17ghz)
        
        if total_detections > 0 and self.shot_count > 0:
            rate_2_5 = len(self.detection_events_2_5ghz) / self.shot_count
            rate_17 = len(self.detection_events_17ghz) / self.shot_count
            total_rate = rate_2_5 + rate_17
            
            if total_rate > 0:
                self.collapse_frequency = (2.5 * rate_2_5 + 17.0 * rate_17) / total_rate
                self.collapse_frequency *= self.sensitivity_var.get()
            
            if len(self.interference_data) > 5:
                interference_factor = np.mean(self.interference_data[-5:]) / (2 * math.pi)
                self.collapse_frequency *= (1 + 0.1 * interference_factor)
    
    def update_qubit_states(self):
        """Update qubit states based on measurements"""
        if len(self.detection_events_2_5ghz) > 0:
            last_phase = self.detection_events_2_5ghz[-1]['phase']
            angle = (last_phase % (2 * math.pi)) / 2
            self.qubit1_state = np.array([np.cos(angle), np.sin(angle)], dtype=complex)
        
        if len(self.detection_events_17ghz) > 0:
            last_phase = self.detection_events_17ghz[-1]['phase']
            angle = (last_phase % (2 * math.pi)) / 2
            phase = np.exp(1j * last_phase)
            self.qubit2_state = np.array([np.cos(angle), np.sin(angle) * phase], dtype=complex)
        
        if len(self.detection_events_2_5ghz) + len(self.detection_events_17ghz) > 0:
            combined_phase = 0
            if self.detection_events_2_5ghz:
                combined_phase += self.detection_events_2_5ghz[-1]['phase']
            if self.detection_events_17ghz:
                combined_phase += self.detection_events_17ghz[-1]['phase']
            angle = (combined_phase % (2 * math.pi)) / 2
            self.qubit3_state = np.array([np.cos(angle), np.sin(angle)], dtype=complex)
        
        if self.gate_config['coupling']:
            if abs(self.qubit1_state[1]) > 0.5:
                self.qubit2_state = np.array([self.qubit2_state[1], self.qubit2_state[0]])
        
        self.update_state_displays()
    
    def draw_photons(self):
        """Draw photons on canvas"""
        self.canvas.delete('photon')
        
        for pair in self.photon_pairs:
            for photon_key in ['photon1', 'photon2']:
                photon = pair[photon_key]
                if not photon['detected']:
                    x, y = photon['x'], photon['y']
                    color = photon['color']
                    
                    pulse = abs(math.sin(self.shot_count * 0.2))
                    glow_size = 6 + pulse * 3
                    
                    self.canvas.create_oval(x-glow_size, y-glow_size, 
                                          x+glow_size, y+glow_size, 
                                          fill='', outline=color, width=2, tags='photon')
                    self.canvas.create_oval(x-3, y-3, x+3, y+3, 
                                          fill=color, outline='white', width=1, tags='photon')
                    
                    if pair['entangled'] and photon_key == 'photon1':
                        other = pair['photon2']
                        if not other['detected']:
                            self.canvas.create_line(photon['x'], photon['y'], 
                                                  other['x'], other['y'],
                                                  fill='#ffff00', width=1, dash=(3,3), 
                                                  tags='photon')
                            
                            mid_x = (photon['x'] + other['x']) / 2
                            mid_y = (photon['y'] + other['y']) / 2
                            self.canvas.create_text(mid_x, mid_y - 8, 
                                                   text="⚛", fill='#ffff00', 
                                                   font=('Arial', 10), tags='photon')
    
    def draw_interference_pattern(self):
        """Draw interference pattern on screen"""
        self.canvas.delete('interference')
        
        if len(self.interference_data) > 0:
            screen_height = 240
            num_lines = 40
            
            for i in range(num_lines):
                y = 235 + i * (screen_height / num_lines)
                
                intensity = 0
                
                for event in self.detection_events_2_5ghz[-10:]:
                    phase_contribution = math.cos(event['phase'] + i * 0.15)
                    intensity += phase_contribution
                
                for event in self.detection_events_17ghz[-10:]:
                    phase_contribution = math.cos(event['phase'] + i * 0.15 + math.pi/4)
                    intensity += phase_contribution
                
                total_events = len(self.detection_events_2_5ghz[-10:]) + len(self.detection_events_17ghz[-10:])
                if total_events > 0:
                    normalized_intensity = abs(intensity) / total_events
                    brightness = int(min(255, normalized_intensity * 255))
                else:
                    brightness = 0
                
                color = f'#{brightness//4:02x}{brightness//2:02x}{min(255, brightness):02x}'
                
                line_width = 2 if brightness > 100 else 1
                self.canvas.create_line(740, y, 810, y, 
                                       fill=color, width=line_width, 
                                       tags='interference')
                
                if brightness > 200:
                    self.canvas.create_oval(808, y-1, 812, y+1,
                                           fill='#ffffff', outline='', 
                                           tags='interference')
    
    def update_labels(self):
        """Update all status labels"""
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
    
    def animation_loop(self):
        """Main animation loop"""
        if self.is_running:
            self.update_photons()
            
            if self.pulse_mode.get() == "Continuous":
                if random.random() < 0.2 and len(self.photon_pairs) < self.max_photons:
                    self.shot_count += 1
                    self.generate_entangled_pair()
            elif len(self.photon_pairs) == 0:
                self.is_running = False
        
        self.draw_photons()
        self.draw_interference_pattern()
        self.update_labels()
        
        self.root.after(50, self.animation_loop)


def main():
    """Main entry point"""
    root = tk.Tk()
    simulator = QuantumEntanglementSimulator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
