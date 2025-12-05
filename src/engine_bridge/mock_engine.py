"""
Mock physics engine for testing the UI without the C++ backend.
Implements simple linear motion for particles.
"""

import numpy as np
from typing import Optional
from .simulation_engine import SimulationEngine


class MockEngine(SimulationEngine):
    """
    Mock simulation engine that generates random particles and updates them
    with simple linear motion. Used for UI testing without the C++ engine.
    """
    
    # Particle type constants
    STAR = 0
    PLANET = 1
    BLACK_HOLE = 2
    
    def __init__(self):
        super().__init__()
        self.positions: Optional[np.ndarray] = None
        self.velocities: Optional[np.ndarray] = None
        self.masses: Optional[np.ndarray] = None
        self.types: Optional[np.ndarray] = None
        self.colors: Optional[np.ndarray] = None
        self.initial_positions: Optional[np.ndarray] = None
        self.initial_velocities: Optional[np.ndarray] = None
    
    def initialize(self, particle_count: int, **kwargs):
        """
        Initialize with random particles.
        
        Args:
            particle_count: Number of particles to create
            **kwargs: Additional parameters:
                - distribution: 'random', 'sphere', 'disk', 'galaxy' (default: 'sphere')
                - scale: Spatial scale factor (default: 50.0)
                - seed: Random seed for reproducibility (default: None)
        """
        distribution = kwargs.get('distribution', 'sphere')
        scale = kwargs.get('scale', 50.0)
        seed = kwargs.get('seed', None)
        
        if seed is not None:
            np.random.seed(seed)
        
        self.particle_count = particle_count
        
        # Generate positions based on distribution
        if distribution == 'sphere':
            self.positions = self._generate_sphere_distribution(particle_count, scale)
        elif distribution == 'disk':
            self.positions = self._generate_disk_distribution(particle_count, scale)
        elif distribution == 'galaxy':
            self.positions = self._generate_galaxy_distribution(particle_count, scale)
        else:  # random
            self.positions = np.random.uniform(-scale, scale, (particle_count, 3))
        
        # Generate velocities (orbital-ish motion around origin)
        self.velocities = self._generate_velocities(self.positions)
        
        # Generate masses (log-normal distribution for realistic variety)
        self.masses = np.random.lognormal(0, 1.5, particle_count)
        
        # Assign types and colors
        self.types = self._assign_types(particle_count)
        self.colors = self._generate_colors(self.types)
        
        # Store initial state for reset
        self.initial_positions = self.positions.copy()
        self.initial_velocities = self.velocities.copy()
        
        self.initialized = True
    
    def _generate_sphere_distribution(self, count: int, scale: float) -> np.ndarray:
        """Generate particles in a spherical distribution."""
        # Use rejection sampling for uniform sphere
        positions = []
        while len(positions) < count:
            candidate = np.random.uniform(-1, 1, (count - len(positions), 3))
            distances = np.linalg.norm(candidate, axis=1)
            valid = candidate[distances <= 1.0]
            positions.extend(valid)
        
        return np.array(positions[:count]) * scale
    
    def _generate_disk_distribution(self, count: int, scale: float) -> np.ndarray:
        """Generate particles in a disk distribution."""
        r = np.random.exponential(scale * 0.3, count)
        theta = np.random.uniform(0, 2 * np.pi, count)
        z = np.random.normal(0, scale * 0.05, count)
        
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        
        return np.column_stack([x, y, z])
    
    def _generate_galaxy_distribution(self, count: int, scale: float) -> np.ndarray:
        """Generate particles in a spiral galaxy distribution."""
        # Central bulge (30%) and spiral arms (70%)
        bulge_count = int(count * 0.3)
        arm_count = count - bulge_count
        
        # Bulge: spherical distribution
        bulge = self._generate_sphere_distribution(bulge_count, scale * 0.3)
        
        # Spiral arms
        r = np.random.exponential(scale * 0.4, arm_count)
        theta = np.random.uniform(0, 4 * np.pi, arm_count)
        # Add spiral pattern
        theta += r / (scale * 0.2) * np.pi
        z = np.random.normal(0, scale * 0.03, arm_count)
        
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        arms = np.column_stack([x, y, z])
        
        return np.vstack([bulge, arms])
    
    def _generate_velocities(self, positions: np.ndarray) -> np.ndarray:
        """Generate orbital velocities around the origin."""
        # Calculate distance from origin
        r = np.linalg.norm(positions[:, :2], axis=1, keepdims=True)
        r = np.maximum(r, 0.1)  # Avoid division by zero
        
        # Orbital velocity proportional to 1/sqrt(r) (Keplerian)
        v_magnitude = 2.0 / np.sqrt(r)
        
        # Perpendicular direction in XY plane
        vx = -positions[:, 1:2] / r * v_magnitude
        vy = positions[:, 0:1] / r * v_magnitude
        vz = np.random.normal(0, 0.1, (len(positions), 1))
        
        return np.hstack([vx, vy, vz])
    
    def _assign_types(self, count: int) -> np.ndarray:
        """Assign particle types (mostly stars, some planets, rare black holes)."""
        types = np.random.choice(
            [self.STAR, self.PLANET, self.BLACK_HOLE],
            size=count,
            p=[0.85, 0.14, 0.01]  # 85% stars, 14% planets, 1% black holes
        )
        return types
    
    def _generate_colors(self, types: np.ndarray) -> np.ndarray:
        """Generate colors based on particle types."""
        colors = np.zeros((len(types), 3))
        
        for i, ptype in enumerate(types):
            if ptype == self.STAR:
                # Stars: Various colors (blue, white, yellow, orange, red)
                temp = np.random.choice([0, 1, 2, 3, 4], p=[0.1, 0.2, 0.4, 0.2, 0.1])
                if temp == 0:  # Blue
                    colors[i] = [0.5, 0.7, 1.0]
                elif temp == 1:  # White
                    colors[i] = [1.0, 1.0, 1.0]
                elif temp == 2:  # Yellow
                    colors[i] = [1.0, 1.0, 0.6]
                elif temp == 3:  # Orange
                    colors[i] = [1.0, 0.7, 0.3]
                else:  # Red
                    colors[i] = [1.0, 0.3, 0.2]
            elif ptype == self.PLANET:
                # Planets: Earth-like colors
                colors[i] = np.random.uniform([0.2, 0.3, 0.5], [0.5, 0.6, 0.8])
            else:  # Black hole
                # Black holes: Purple/magenta
                colors[i] = [0.8, 0.2, 0.8]
        
        return colors
    
    def step(self, dt: float):
        """Advance simulation with simple linear motion."""
        if not self.initialized:
            raise RuntimeError("Engine not initialized")
        
        # Simple Euler integration
        self.positions += self.velocities * dt
        
        # Optional: Add some gravitational-like acceleration toward origin
        # (very simplified, just for visual effect)
        r = np.linalg.norm(self.positions, axis=1, keepdims=True)
        r = np.maximum(r, 1.0)
        acceleration = -0.5 * self.positions / (r ** 3)
        self.velocities += acceleration * dt
    
    def get_positions(self) -> np.ndarray:
        """Get current particle positions."""
        return self.positions
    
    def get_velocities(self) -> np.ndarray:
        """Get current particle velocities."""
        return self.velocities
    
    def get_masses(self) -> np.ndarray:
        """Get particle masses."""
        return self.masses
    
    def get_colors(self) -> np.ndarray:
        """Get particle colors (RGB)."""
        return self.colors
    
    def get_types(self) -> np.ndarray:
        """Get particle types."""
        return self.types
    
    def set_positions(self, positions: np.ndarray):
        """Set particle positions."""
        self.positions = positions.copy()
    
    def set_velocities(self, velocities: np.ndarray):
        """Set particle velocities."""
        self.velocities = velocities.copy()
    
    def add_particle(self, position: np.ndarray, velocity: np.ndarray, 
                    mass: float, particle_type: int = 0):
        """Add a single particle to the simulation."""
        if not self.initialized:
            raise RuntimeError("Engine not initialized")
        
        self.positions = np.vstack([self.positions, position])
        self.velocities = np.vstack([self.velocities, velocity])
        self.masses = np.append(self.masses, mass)
        self.types = np.append(self.types, particle_type)
        
        # Generate color for new particle
        new_color = self._generate_colors(np.array([particle_type]))[0]
        self.colors = np.vstack([self.colors, new_color])
        
        self.particle_count += 1
    
    def remove_particle(self, index: int):
        """Remove a particle from the simulation."""
        if not self.initialized or index >= self.particle_count:
            raise RuntimeError("Invalid particle index")
        
        self.positions = np.delete(self.positions, index, axis=0)
        self.velocities = np.delete(self.velocities, index, axis=0)
        self.masses = np.delete(self.masses, index)
        self.types = np.delete(self.types, index)
        self.colors = np.delete(self.colors, index, axis=0)
        
        self.particle_count -= 1
    
    def reset(self):
        """Reset to initial conditions."""
        if self.initial_positions is not None:
            self.positions = self.initial_positions.copy()
            self.velocities = self.initial_velocities.copy()
