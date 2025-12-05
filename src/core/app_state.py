"""
Application state management for StellarForge.
Implements the Model in the MVC pattern.
"""

from enum import Enum
from typing import Optional, Dict, Any
import numpy as np


class SimulationMode(Enum):
    """User interaction modes."""
    OBSERVATION = "observation"
    SANDBOX = "sandbox"


class AppState:
    """
    Central application state manager.
    Holds the current state of the simulation and UI settings.
    """
    
    def __init__(self):
        # Simulation state
        self.mode: SimulationMode = SimulationMode.OBSERVATION
        self.is_playing: bool = False
        self.simulation_speed: float = 1.0
        self.current_time: float = 0.0
        self.dt: float = 0.016  # Default time step (~60 FPS)
        
        # Physics toggles
        self.show_gravity_lines: bool = False
        self.enable_collisions: bool = True
        self.relativistic_mode: bool = False
        
        # Particle data (will be populated by engine)
        self.positions: Optional[np.ndarray] = None  # Shape: (N, 3)
        self.velocities: Optional[np.ndarray] = None  # Shape: (N, 3)
        self.masses: Optional[np.ndarray] = None  # Shape: (N,)
        self.colors: Optional[np.ndarray] = None  # Shape: (N, 3) RGB
        self.types: Optional[np.ndarray] = None  # Shape: (N,) particle types
        
        # Snapshot system
        self.snapshots: list = []  # List of saved states
        self.snapshot_interval: float = 1.0  # seconds between snapshots
        self.last_snapshot_time: float = 0.0
        
        # Camera state
        self.camera_position: np.ndarray = np.array([0.0, 0.0, 100.0])
        self.camera_target: np.ndarray = np.array([0.0, 0.0, 0.0])
        
        # Selected object
        self.selected_object_index: Optional[int] = None
    
    def set_mode(self, mode: SimulationMode):
        """Switch between observation and sandbox modes."""
        self.mode = mode
    
    def toggle_play_pause(self):
        """Toggle simulation play/pause state."""
        self.is_playing = not self.is_playing
    
    def set_speed(self, speed: float):
        """Set simulation speed multiplier."""
        self.simulation_speed = max(0.1, min(10.0, speed))
    
    def update_time(self, dt: float):
        """Update simulation time."""
        self.current_time += dt * self.simulation_speed
        
        # Check if we should take a snapshot
        if self.current_time - self.last_snapshot_time >= self.snapshot_interval:
            self.take_snapshot()
            self.last_snapshot_time = self.current_time
    
    def take_snapshot(self):
        """Save current simulation state."""
        if self.positions is not None:
            snapshot = {
                'time': self.current_time,
                'positions': self.positions.copy(),
                'velocities': self.velocities.copy() if self.velocities is not None else None,
                'masses': self.masses.copy() if self.masses is not None else None,
                'colors': self.colors.copy() if self.colors is not None else None,
                'types': self.types.copy() if self.types is not None else None,
            }
            self.snapshots.append(snapshot)
    
    def reset(self):
        """Reset simulation to initial state."""
        self.is_playing = False
        self.current_time = 0.0
        self.last_snapshot_time = 0.0
        self.snapshots.clear()
        self.selected_object_index = None
    
    def get_particle_count(self) -> int:
        """Return the number of particles in the simulation."""
        if self.positions is not None:
            return len(self.positions)
        return 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize state to dictionary for saving."""
        return {
            'mode': self.mode.value,
            'simulation_speed': self.simulation_speed,
            'current_time': self.current_time,
            'show_gravity_lines': self.show_gravity_lines,
            'enable_collisions': self.enable_collisions,
            'relativistic_mode': self.relativistic_mode,
            'snapshot_interval': self.snapshot_interval,
            'camera_position': self.camera_position.tolist(),
            'camera_target': self.camera_target.tolist(),
        }
    
    def from_dict(self, data: Dict[str, Any]):
        """Restore state from dictionary."""
        self.mode = SimulationMode(data.get('mode', 'observation'))
        self.simulation_speed = data.get('simulation_speed', 1.0)
        self.current_time = data.get('current_time', 0.0)
        self.show_gravity_lines = data.get('show_gravity_lines', False)
        self.enable_collisions = data.get('enable_collisions', True)
        self.relativistic_mode = data.get('relativistic_mode', False)
        self.snapshot_interval = data.get('snapshot_interval', 1.0)
        self.camera_position = np.array(data.get('camera_position', [0.0, 0.0, 100.0]))
        self.camera_target = np.array(data.get('camera_target', [0.0, 0.0, 0.0]))
