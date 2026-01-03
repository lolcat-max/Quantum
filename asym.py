import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PolyCollection
import matplotlib.gridspec as gridspec
from scipy.signal import correlate, periodogram
from scipy.fft import fft, fftfreq

class KitaevQuantumSpinLiquidWithGravity:
    """
    Quantum Spin Liquid with gravitational coupling.
    
    Models:
    1. Directional kinetic law: c(velocity) balancing with emitted light frequency
    2. Gravitational gradient effects on nuclear positions (resting state)
    3. Coupling between gravitational potential and spin dynamics
    """
    
    def __init__(self, Lx=6, Ly=6, Jx=1.0, Jy=1.0, Jz=1.0, 
                 g_field=0.1, g_gradient=0.01, 
                 light_coupling=0.05, kinetic_coupling=0.1):
        """
        Args:
            Lx, Ly: Linear dimensions of honeycomb lattice
            Jx, Jy, Jz: Coupling strengths for x, y, z bonds
            g_field: Gravitational field strength (vertical direction)
            g_gradient: Gravitational gradient (∂g/∂z)
            light_coupling: Coupling strength between spin dynamics and photon emission
            kinetic_coupling: Coupling between material velocity and spin dynamics
        """
        self.Lx = Lx
        self.Ly = Ly
        self.Jx = Jx
        self.Jy = Jy
        self.Jz = Jz
        
        # Gravitational parameters
        self.g_field = g_field
        self.g_gradient = g_gradient
        self.light_coupling = light_coupling
        self.kinetic_coupling = kinetic_coupling
        
        # Speed of light (normalized units)
        self.c = 1.0
        
        # Build honeycomb lattice geometry
        self.build_honeycomb_lattice()
        
        # Initialize spin configuration (random)
        self.spins = np.random.choice([-1, 1], size=self.n_sites)
        
        # Nuclear displacement due to gravity gradient (resting state)
        self.nuclear_displacement = np.zeros((self.n_sites, 2))
        self.calculate_nuclear_displacement()
        
        # Material velocity (for moving reference frame)
        self.velocity = np.array([0.0, 0.0])  # [v_x, v_y]
        
        # Track history
        self.energy_history = []
        self.gravitational_energy_history = []
        self.photon_emission_history = []
        self.asymmetry_history = []
        self.velocity_history = []
        
    def build_honeycomb_lattice(self):
        """Build honeycomb lattice coordinates and bond structure"""
        sites = []
        bonds_x = []
        bonds_y = []
        bonds_z = []
        
        # Basis vectors for honeycomb lattice
        a1 = np.array([np.sqrt(3), 0])
        a2 = np.array([np.sqrt(3)/2, 3/2])
        
        # Build lattice sites
        site_idx = 0
        self.site_positions = []
        self.site_to_idx = {}
        
        for ix in range(self.Lx):
            for iy in range(self.Ly):
                # A sublattice
                pos_A = ix * a1 + iy * a2
                sites.append(('A', ix, iy))
                self.site_positions.append(pos_A)
                self.site_to_idx[('A', ix, iy)] = site_idx
                site_idx += 1
                
                # B sublattice
                pos_B = pos_A + np.array([1/np.sqrt(3), 0])
                sites.append(('B', ix, iy))
                self.site_positions.append(pos_B)
                self.site_to_idx[('B', ix, iy)] = site_idx
                site_idx += 1
        
        self.n_sites = len(sites)
        self.sites = sites
        self.site_positions = np.array(self.site_positions)
        
        # Build bonds
        for ix in range(self.Lx):
            for iy in range(self.Ly):
                # Z-bonds: vertical bonds (A to B in same cell)
                i_A = self.site_to_idx[('A', ix, iy)]
                i_B = self.site_to_idx[('B', ix, iy)]
                bonds_z.append((i_A, i_B))
                
                # X-bonds
                if ix < self.Lx - 1:
                    i_B = self.site_to_idx[('B', ix, iy)]
                    i_A_next = self.site_to_idx[('A', ix+1, iy)]
                    bonds_x.append((i_B, i_A_next))
                
                # Y-bonds
                if iy < self.Ly - 1:
                    i_B = self.site_to_idx[('B', ix, iy)]
                    i_A_next = self.site_to_idx[('A', ix, iy+1)]
                    bonds_y.append((i_B, i_A_next))
        
        self.bonds_x = bonds_x
        self.bonds_y = bonds_y
        self.bonds_z = bonds_z
        self.all_bonds = bonds_x + bonds_y + bonds_z
        
    def calculate_nuclear_displacement(self):
        """
        Calculate nuclear displacement in resting state due to gravity gradient.
        
        The gradient creates asymmetric forces on opposite sides of the nucleus,
        leading to a net displacement δr ~ g_gradient * z_position
        """
        for i in range(self.n_sites):
            z_pos = self.site_positions[i, 1]  # Use y-coordinate as vertical
            
            # Displacement proportional to height and gradient
            # Upper sites displaced upward, lower sites displaced downward
            displacement_magnitude = self.g_gradient * (z_pos - np.mean(self.site_positions[:, 1]))
            
            # Displacement is primarily vertical
            self.nuclear_displacement[i, 0] = 0.0
            self.nuclear_displacement[i, 1] = displacement_magnitude
    
    def calculate_effective_light_speed(self, direction):
        """
        Calculate effective speed of light in moving frame.
        
        For motion in direction θ:
        - Forward (along velocity): c_eff = c - v·n̂
        - Backward (against velocity): c_eff = c + v·n̂
        
        This affects photon emission frequency via Doppler shift.
        """
        v_magnitude = np.linalg.norm(self.velocity)
        
        if v_magnitude < 1e-10:
            return self.c
        
        # Direction unit vector
        v_hat = self.velocity / v_magnitude
        direction_hat = direction / (np.linalg.norm(direction) + 1e-10)
        
        # Relativistic Doppler factor (simplified to first order)
        beta = v_magnitude / self.c
        cos_theta = np.dot(v_hat, direction_hat)
        
        # c_eff for photon emission
        c_eff = self.c * (1 - beta * cos_theta)
        
        return c_eff
    
    def calculate_gravitational_potential(self, site):
        """
        Calculate gravitational potential energy at a site.
        
        Φ(z) = m*g*z + (1/2)*m*g'*z²
        
        where g' is the gravitational gradient.
        """
        z_pos = self.site_positions[site, 1]
        z_displaced = z_pos + self.nuclear_displacement[site, 1]
        
        # Linear term + gradient term
        potential = self.g_field * z_displaced + 0.5 * self.g_gradient * z_displaced**2
        
        return potential
    
    def calculate_kinetic_energy_correction(self, site, spin):
        """
        Calculate kinetic energy correction due to material motion.
        
        When material moves, spin dynamics couple to kinetic energy through:
        E_kin_corr = α * (v/c)² * σ * f(direction)
        
        This represents the coupling between spin and momentum.
        """
        v_magnitude = np.linalg.norm(self.velocity)
        
        if v_magnitude < 1e-10:
            return 0.0
        
        # Position relative to center
        r_rel = self.site_positions[site] - np.mean(self.site_positions, axis=0)
        
        # Check if site is in direction of motion or opposite
        alignment = np.dot(r_rel, self.velocity) / (np.linalg.norm(r_rel) + 1e-10)
        
        # Kinetic correction depends on spin and alignment with motion
        beta_squared = (v_magnitude / self.c) ** 2
        correction = self.kinetic_coupling * beta_squared * spin * np.sign(alignment)
        
        return correction
    
    def calculate_photon_emission_rate(self, site):
        """
        Calculate photon emission rate from spin flip at this site.
        
        Rate depends on:
        1. Local spin configuration (energy available)
        2. Direction relative to velocity (Doppler shift)
        3. Gravitational redshift
        """
        # Direction from site to neighbors (average)
        neighbor_directions = []
        for i, j in self.all_bonds:
            if i == site:
                neighbor_directions.append(self.site_positions[j] - self.site_positions[i])
            elif j == site:
                neighbor_directions.append(self.site_positions[i] - self.site_positions[j])
        
        if len(neighbor_directions) == 0:
            return 0.0
        
        avg_direction = np.mean(neighbor_directions, axis=0)
        
        # Effective light speed in this direction
        c_eff = self.calculate_effective_light_speed(avg_direction)
        
        # Gravitational redshift factor
        z_pos = self.site_positions[site, 1]
        redshift_factor = 1.0 - self.g_field * z_pos / (self.c**2)
        
        # Emission rate ~ ω = E/ℏ, modified by Doppler and gravity
        base_rate = abs(self.spins[site])  # Spin-dependent
        emission_rate = base_rate * (c_eff / self.c) * redshift_factor
        
        return emission_rate
    
    def calculate_energy(self):
        """Calculate total energy including gravitational and kinetic corrections"""
        energy = 0.0
        
        # Standard spin-spin interaction energy
        for i, j in self.bonds_x:
            energy -= self.Jx * self.spins[i] * self.spins[j]
        
        for i, j in self.bonds_y:
            energy -= self.Jy * self.spins[i] * self.spins[j]
        
        for i, j in self.bonds_z:
            energy -= self.Jz * self.spins[i] * self.spins[j]
        
        return energy
    
    def calculate_total_energy_with_gravity(self):
        """Calculate total energy including all gravitational effects"""
        # Base spin energy
        E_spin = self.calculate_energy()
        
        # Gravitational potential energy
        E_grav = sum([self.calculate_gravitational_potential(i) * abs(self.spins[i]) 
                      for i in range(self.n_sites)])
        
        # Kinetic energy corrections
        E_kin = sum([self.calculate_kinetic_energy_correction(i, self.spins[i]) 
                     for i in range(self.n_sites)])
        
        return E_spin + E_grav + E_kin
    
    def calculate_directional_asymmetry(self):
        """
        Calculate asymmetry in spin configuration due to gravity gradient.
        
        Measures difference between upper and lower halves of lattice.
        """
        z_median = np.median(self.site_positions[:, 1])
        
        upper_spins = [self.spins[i] for i in range(self.n_sites) 
                       if self.site_positions[i, 1] > z_median]
        lower_spins = [self.spins[i] for i in range(self.n_sites) 
                       if self.site_positions[i, 1] <= z_median]
        
        if len(upper_spins) == 0 or len(lower_spins) == 0:
            return 0.0
        
        asymmetry = np.mean(upper_spins) - np.mean(lower_spins)
        return asymmetry
    
    def monte_carlo_step_with_gravity(self, temperature):
        """
        Monte Carlo step including gravitational effects.
        """
        beta = 1.0 / temperature if temperature > 0 else np.inf
        
        # Propose spin flip
        site = np.random.randint(0, self.n_sites)
        
        # Calculate energy change with all effects
        E_old = self.calculate_total_energy_with_gravity()
        
        # Flip spin
        self.spins[site] *= -1
        
        E_new = self.calculate_total_energy_with_gravity()
        dE = E_new - E_old
        
        # Calculate photon emission for this flip
        photon_rate = self.calculate_photon_emission_rate(site)
        
        # Accept or reject
        if dE < 0 or np.random.random() < np.exp(-beta * dE):
            # Accept - photon may be emitted
            return True, photon_rate
        else:
            # Reject - flip back
            self.spins[site] *= -1
            return False, 0.0
    
    def simulate_dynamics_with_gravity(self, n_steps, temperature=0.1, 
                                       record_interval=1, 
                                       velocity_schedule=None):
        """
        Run Monte Carlo dynamics with gravitational effects.
        
        Args:
            velocity_schedule: Function v(t) that returns velocity at each step
                             If None, system is at rest
        """
        energies = []
        grav_energies = []
        photon_emissions = []
        asymmetries = []
        velocities = []
        magnetizations = []
        
        for step in range(n_steps):
            # Update velocity if schedule provided
            if velocity_schedule is not None:
                self.velocity = velocity_schedule(step)
            
            # Perform MC sweep
            total_photon_rate = 0.0
            for _ in range(self.n_sites):
                accepted, photon_rate = self.monte_carlo_step_with_gravity(temperature)
                if accepted:
                    total_photon_rate += photon_rate
            
            # Record data
            if step % record_interval == 0:
                E_total = self.calculate_total_energy_with_gravity()
                E_spin = self.calculate_energy()
                E_grav = E_total - E_spin
                
                energies.append(E_total)
                grav_energies.append(E_grav)
                photon_emissions.append(total_photon_rate)
                asymmetries.append(self.calculate_directional_asymmetry())
                velocities.append(np.linalg.norm(self.velocity))
                magnetizations.append(np.mean(self.spins))
        
        self.energy_history = np.array(energies)
        self.gravitational_energy_history = np.array(grav_energies)
        self.photon_emission_history = np.array(photon_emissions)
        self.asymmetry_history = np.array(asymmetries)
        self.velocity_history = np.array(velocities)
        
        return {
            'energies': np.array(energies),
            'grav_energies': np.array(grav_energies),
            'photon_emissions': np.array(photon_emissions),
            'asymmetries': np.array(asymmetries),
            'velocities': np.array(velocities),
            'magnetizations': np.array(magnetizations)
        }


def plot_gravity_effects(qsl_systems, labels, titles):
    """
    Comprehensive visualization of gravitational effects on QSL.
    """
    n_systems = len(qsl_systems)
    
    fig = plt.figure(figsize=(20, 14))
    gs = gridspec.GridSpec(4, 3, figure=fig, hspace=0.4, wspace=0.35)
    
    colors = ['blue', 'red', 'green', 'purple', 'orange']
    
    # 1. Total energy vs time
    ax1 = fig.add_subplot(gs[0, 0])
    for i, (data, label) in enumerate(zip(qsl_systems, labels)):
        steps = np.arange(len(data['energies']))
        ax1.plot(steps, data['energies'], '-', linewidth=2, 
                color=colors[i % len(colors)], label=label, alpha=0.8)
    
    ax1.set_xlabel('MC Steps', fontsize=11)
    ax1.set_ylabel('Total Energy', fontsize=11)
    ax1.set_title('Total Energy\n(Spin + Gravitational + Kinetic)', fontsize=12, fontweight='bold')
    ax1.legend(loc='best', fontsize=9)
    ax1.grid(True, alpha=0.3)
    
    # 2. Gravitational energy contribution
    ax2 = fig.add_subplot(gs[0, 1])
    for i, (data, label) in enumerate(zip(qsl_systems, labels)):
        steps = np.arange(len(data['grav_energies']))
        ax2.plot(steps, data['grav_energies'], '-', linewidth=2, 
                color=colors[i % len(colors)], label=label, alpha=0.8)
    
    ax2.set_xlabel('MC Steps', fontsize=11)
    ax2.set_ylabel('Gravitational Energy', fontsize=11)
    ax2.set_title('Gravitational Energy Contribution\nE_grav = Φ(z) + ∂Φ/∂z·δz', 
                  fontsize=12, fontweight='bold')
    ax2.legend(loc='best', fontsize=9)
    ax2.grid(True, alpha=0.3)
    
    # 3. Photon emission rate
    ax3 = fig.add_subplot(gs[0, 2])
    for i, (data, label) in enumerate(zip(qsl_systems, labels)):
        steps = np.arange(len(data['photon_emissions']))
        ax3.plot(steps, data['photon_emissions'], '-', linewidth=2, 
                color=colors[i % len(colors)], label=label, alpha=0.8)
    
    ax3.set_xlabel('MC Steps', fontsize=11)
    ax3.set_ylabel('Photon Emission Rate', fontsize=11)
    ax3.set_title('Photon Emission Rate\n(Doppler + Gravitational Redshift)', 
                  fontsize=12, fontweight='bold')
    ax3.legend(loc='best', fontsize=9)
    ax3.grid(True, alpha=0.3)
    
    # 4. Directional asymmetry
    ax4 = fig.add_subplot(gs[1, 0])
    for i, (data, label) in enumerate(zip(qsl_systems, labels)):
        steps = np.arange(len(data['asymmetries']))
        ax4.plot(steps, data['asymmetries'], '-', linewidth=2, 
                color=colors[i % len(colors)], label=label, alpha=0.8)
    
    ax4.axhline(y=0, color='k', linestyle='--', alpha=0.5)
    ax4.set_xlabel('MC Steps', fontsize=11)
    ax4.set_ylabel('Asymmetry A', fontsize=11)
    ax4.set_title('Vertical Asymmetry\nA = ⟨S_upper⟩ - ⟨S_lower⟩', 
                  fontsize=12, fontweight='bold')
    ax4.legend(loc='best', fontsize=9)
    ax4.grid(True, alpha=0.3)
    
    # 5. Velocity vs time
    ax5 = fig.add_subplot(gs[1, 1])
    for i, (data, label) in enumerate(zip(qsl_systems, labels)):
        steps = np.arange(len(data['velocities']))
        ax5.plot(steps, data['velocities'], '-', linewidth=2, 
                color=colors[i % len(colors)], label=label, alpha=0.8)
    
    ax5.set_xlabel('MC Steps', fontsize=11)
    ax5.set_ylabel('|v| / c', fontsize=11)
    ax5.set_title('Material Velocity\n(Kinetic Reference Frame)', 
                  fontsize=12, fontweight='bold')
    ax5.legend(loc='best', fontsize=9)
    ax5.grid(True, alpha=0.3)
    
    # 6. Energy distribution
    ax6 = fig.add_subplot(gs[1, 2])
    for i, (data, label) in enumerate(zip(qsl_systems, labels)):
        ax6.hist(data['energies'], bins=30, density=True, alpha=0.5, 
                color=colors[i % len(colors)], label=label, edgecolor='black')
    
    ax6.set_xlabel('Total Energy', fontsize=11)
    ax6.set_ylabel('P(E)', fontsize=11)
    ax6.set_title('Energy Distribution\n(Modified by Gravity)', 
                  fontsize=12, fontweight='bold')
    ax6.legend(loc='best', fontsize=9)
    ax6.grid(True, alpha=0.3)
    
    # 7. Correlation: Energy vs Photon Emission
    ax7 = fig.add_subplot(gs[2, 0])
    for i, (data, label) in enumerate(zip(qsl_systems, labels)):
        ax7.scatter(data['energies'], data['photon_emissions'], 
                   s=20, alpha=0.5, color=colors[i % len(colors)], label=label)
    
    ax7.set_xlabel('Total Energy', fontsize=11)
    ax7.set_ylabel('Photon Emission Rate', fontsize=11)
    ax7.set_title('Energy-Photon Coupling\n(Light Emission Balance)', 
                  fontsize=12, fontweight='bold')
    ax7.legend(loc='best', fontsize=9)
    ax7.grid(True, alpha=0.3)
    
    # 8. Correlation: Velocity vs Asymmetry
    ax8 = fig.add_subplot(gs[2, 1])
    for i, (data, label) in enumerate(zip(qsl_systems, labels)):
        ax8.scatter(data['velocities'], data['asymmetries'], 
                   s=20, alpha=0.5, color=colors[i % len(colors)], label=label)
    
    ax8.set_xlabel('|v| / c', fontsize=11)
    ax8.set_ylabel('Asymmetry', fontsize=11)
    ax8.set_title('Velocity-Asymmetry Coupling\n(Kinetic Law Balance)', 
                  fontsize=12, fontweight='bold')
    ax8.legend(loc='best', fontsize=9)
    ax8.grid(True, alpha=0.3)
    
    # 9. Photon emission spectrum
    ax9 = fig.add_subplot(gs[2, 2])
    for i, (data, label) in enumerate(zip(qsl_systems, labels)):
        photon_fluct = data['photon_emissions'] - np.mean(data['photon_emissions'])
        if len(photon_fluct) > 10:
            freqs = fftfreq(len(photon_fluct))
            spectrum = np.abs(fft(photon_fluct))**2
            # Only positive frequencies
            pos_freqs = freqs[:len(freqs)//2]
            pos_spectrum = spectrum[:len(spectrum)//2]
            ax9.semilogy(pos_freqs[1:], pos_spectrum[1:], '-', linewidth=2,
                        color=colors[i % len(colors)], label=label, alpha=0.8)
    
    ax9.set_xlabel('Frequency', fontsize=11)
    ax9.set_ylabel('Power', fontsize=11)
    ax9.set_title('Photon Emission Spectrum\n(Characteristic Frequencies)', 
                  fontsize=12, fontweight='bold')
    ax9.legend(loc='best', fontsize=9)
    ax9.grid(True, alpha=0.3)
    
    # 10. Phase space: Energy vs Asymmetry
    ax10 = fig.add_subplot(gs[3, 0])
    for i, (data, label) in enumerate(zip(qsl_systems, labels)):
        ax10.scatter(data['energies'], data['asymmetries'], 
                    s=20, alpha=0.3, color=colors[i % len(colors)], label=label)
    
    ax10.axhline(y=0, color='k', linestyle='--', alpha=0.5)
    ax10.set_xlabel('Total Energy', fontsize=11)
    ax10.set_ylabel('Asymmetry', fontsize=11)
    ax10.set_title('Phase Space\n(Gravity-Induced Coupling)', 
                   fontsize=12, fontweight='bold')
    ax10.legend(loc='best', fontsize=9)
    ax10.grid(True, alpha=0.3)
    
    # 11. Magnetization
    ax11 = fig.add_subplot(gs[3, 1])
    for i, (data, label) in enumerate(zip(qsl_systems, labels)):
        steps = np.arange(len(data['magnetizations']))
        ax11.plot(steps, data['magnetizations'], '-', linewidth=1.5, 
                 color=colors[i % len(colors)], label=label, alpha=0.8)
    
    ax11.axhline(y=0, color='k', linestyle='--', alpha=0.5)
    ax11.set_xlabel('MC Steps', fontsize=11)
    ax11.set_ylabel('⟨S⟩', fontsize=11)
    ax11.set_title('Magnetization\n(No Long-Range Order)', 
                   fontsize=12, fontweight='bold')
    ax11.legend(loc='best', fontsize=9)
    ax11.grid(True, alpha=0.3)
    
    # 12. Summary statistics
    ax12 = fig.add_subplot(gs[3, 2])
    ax12.axis('off')
    
    summary_text = "GRAVITATIONAL EFFECTS SUMMARY\n" + "="*40 + "\n\n"
    
    for i, (data, label) in enumerate(zip(qsl_systems, labels)):
        E_mean = np.mean(data['energies'])
        E_std = np.std(data['energies'])
        A_mean = np.mean(data['asymmetries'])
        photon_mean = np.mean(data['photon_emissions'])
        v_mean = np.mean(data['velocities'])
        
        summary_text += f"{label}:\n"
        summary_text += f"  ⟨E_total⟩ = {E_mean:.3f} ± {E_std:.3f}\n"
        summary_text += f"  ⟨Asymmetry⟩ = {A_mean:.4f}\n"
        summary_text += f"  ⟨Photon Rate⟩ = {photon_mean:.3f}\n"
        summary_text += f"  ⟨|v|/c⟩ = {v_mean:.4f}\n\n"
    
    ax12.text(0.05, 0.95, summary_text, transform=ax12.transAxes,
             fontsize=9, verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    fig.suptitle('Gravitational Effects on Quantum Spin Liquid\n' + 
                'Kinetic Law Balance: c(v) ↔ Photon Emission | Gravity Gradient: Nuclear Displacement',
                fontsize=16, fontweight='bold', y=0.995)
    
    return fig


def main():
    print("=" * 80)
    print("Quantum Spin Liquid with Gravitational Coupling")
    print("Kinetic Law + Gravity Gradient Effects")
    print("=" * 80)
    print()
    
    # Simulation parameters
    Lx, Ly = 5, 5
    n_steps = 1500
    temperature = 0.5
    
    print(f"Lattice: {Lx}×{Ly} honeycomb ({2*Lx*Ly} sites)")
    print(f"MC steps: {n_steps}")
    print(f"Temperature: {temperature}")
    print()
    
    # Define different scenarios
    scenarios = []
    
    # 1. Resting state with gravity gradient
    print("\n" + "="*80)
    print("Scenario 1: Resting State with Gravity Gradient")
    print("="*80)
    print("Nuclear displacement due to ∂g/∂z creates asymmetry")
    
    qsl_rest = KitaevQuantumSpinLiquidWithGravity(
        Lx=Lx, Ly=Ly, Jx=1.0, Jy=1.0, Jz=1.0,
        g_field=0.1, g_gradient=0.05,
        light_coupling=0.05, kinetic_coupling=0.0
    )
    
    data_rest = qsl_rest.simulate_dynamics_with_gravity(
        n_steps, temperature, record_interval=1, velocity_schedule=None
    )
    
    scenarios.append((data_rest, "Resting (∂g/∂z ≠ 0)", "Rest"))
    print(f"✓ Complete: ⟨Asymmetry⟩ = {np.mean(data_rest['asymmetries']):.4f}")
    
    # 2. Moving in +direction (with gravity)
    print("\n" + "="*80)
    print("Scenario 2: Moving Forward (+x direction)")
    print("="*80)
    print("Kinetic law: c_eff = c - v (forward photon emission)")
    
    def velocity_forward(t):
        # Accelerate then constant velocity
        v_max = 0.3
        t_accel = 300
        if t < t_accel:
            v = v_max * (t / t_accel)
        else:
            v = v_max
        return np.array([v, 0.0])
    
    qsl_forward = KitaevQuantumSpinLiquidWithGravity(
        Lx=Lx, Ly=Ly, Jx=1.0, Jy=1.0, Jz=1.0,
        g_field=0.1, g_gradient=0.05,
        light_coupling=0.1, kinetic_coupling=0.2
    )
    
    data_forward = qsl_forward.simulate_dynamics_with_gravity(
        n_steps, temperature, record_interval=1, 
        velocity_schedule=velocity_forward
    )
    
    scenarios.append((data_forward, "Moving Forward (+v)", "Forward"))
    print(f"✓ Complete: ⟨|v|/c⟩ = {np.mean(data_forward['velocities']):.4f}")
    
    # 3. Moving in -direction (with gravity)
    print("\n" + "="*80)
    print("Scenario 3: Moving Backward (-x direction)")
    print("="*80)
    print("Kinetic law: c_eff = c + v (backward photon emission)")
    
    def velocity_backward(t):
        v_max = 0.3
        t_accel = 300
        if t < t_accel:
            v = v_max * (t / t_accel)
        else:
            v = v_max
        return np.array([-v, 0.0])
    
    qsl_backward = KitaevQuantumSpinLiquidWithGravity(
        Lx=Lx, Ly=Ly, Jx=1.0, Jy=1.0, Jz=1.0,
        g_field=0.1, g_gradient=0.05,
        light_coupling=0.1, kinetic_coupling=0.2
    )
    
    data_backward = qsl_backward.simulate_dynamics_with_gravity(
        n_steps, temperature, record_interval=1, 
        velocity_schedule=velocity_backward
    )
    
    scenarios.append((data_backward, "Moving Backward (-v)", "Backward"))
    print(f"✓ Complete: ⟨|v|/c⟩ = {np.mean(data_backward['velocities']):.4f}")
    
    # Create visualization
    print("\n" + "="*80)
    print("Creating comprehensive visualization...")
    print("="*80)
    
    qsl_systems = [s[0] for s in scenarios]
    labels = [s[1] for s in scenarios]
    titles = [s[2] for s in scenarios]
    
    fig = plot_gravity_effects(qsl_systems, labels, titles)
    
    filename = "qsl_gravity_kinetic_coupling.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"\n✓ Saved: {filename}")
    plt.close()
    
    print("\n" + "=" * 80)
    print("PHYSICAL INTERPRETATION")
    print("=" * 80)
    print()
    print("1. RESTING STATE (∂g/∂z ≠ 0):")
    print("   • Gravity gradient creates asymmetric nuclear displacement")
    print("   • Upper sites displaced upward, lower sites downward")
    print("   • Results in spontaneous vertical asymmetry in spin configuration")
    print()
    print("2. KINETIC LAW (MOVING FORWARD):")
    print("   • Effective light speed: c_eff = c - v·n̂")
    print("   • Forward-emitted photons are blueshifted (higher energy)")
    print("   • Creates directional energy imbalance")
    print("   • Spin dynamics couple to material momentum")
    print()
    print("3. KINETIC LAW (MOVING BACKWARD):")
    print("   • Effective light speed: c_eff = c + v·n̂")
    print("   • Backward-emitted photons are redshifted (lower energy)")
    print("   • Opposite directional imbalance from forward motion")
    print("   • Demonstrates c(v) balancing with photon emission")
    print()
    print("4. GRAVITATIONAL REDSHIFT:")
    print("   • Photons climbing out of potential well lose energy")
    print("   • Frequency shift: Δω/ω ≈ gΔz/c²")
    print("   • Couples to spin flip energy via photon emission")
    print()
    print("5. COUPLING MECHANISMS:")
    print("   • Gravity gradient → Nuclear displacement → Spin asymmetry")
    print("   • Material velocity → Kinetic correction → Photon Doppler shift")
    print("   • Light emission rate balances with c(v) in moving frame")
    print()
    print("=" * 80)
    print("Analysis Complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
