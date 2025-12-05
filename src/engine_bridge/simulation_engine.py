"""
Base simulation engine interface.
This defines the contract that the real C++ engine will implement.
"""

from abc import ABC, abstractmethod
import numpy as np
from typing import Tuple, Optional


class SimulationEngine(ABC):
    """
    Abstract base class for simulation engines.
    The C++ engine will implement this interface.
    """
    
    def __init__(self):
        self.initialized = False
        self.particle_count = 0
    
    @abstractmethod
    def initialize(self, particle_count: int, **kwargs):
        """
        Initialize the simulation with a given number of particles.
        
        Args:
            particle_count: Number of particles to simulate
            **kwargs: Additional initialization parameters
        """
        pass
    
    @abstractmethod
    def step(self, dt: float):
        """
        Advance the simulation by one time step.
        
        Args:
            dt: Time step in simulation units
        """
        pass
    
    @abstractmethod
    def get_positions(self) -> np.ndarray:
        """
        Get current particle positions.
        
        Returns:
            Array of shape (N, 3) with x, y, z coordinates
        """
        pass
    
    @abstractmethod
    def get_velocities(self) -> np.ndarray:
        """
        Get current particle velocities.
        
        Returns:
            Array of shape (N, 3) with vx, vy, vz components
        """
        pass
    
    @abstractmethod
    def get_masses(self) -> np.ndarray:
        """
        Get particle masses.
        
        Returns:
            Array of shape (N,) with mass values
        """
        pass
    
    @abstractmethod
    def set_positions(self, positions: np.ndarray):
        """
        Set particle positions.
        
        Args:
            positions: Array of shape (N, 3)
        """
        pass
    
    @abstractmethod
    def set_velocities(self, velocities: np.ndarray):
        """
        Set particle velocities.
        
        Args:
            velocities: Array of shape (N, 3)
        """
        pass
    
    @abstractmethod
    def add_particle(self, position: np.ndarray, velocity: np.ndarray, 
                    mass: float, particle_type: int = 0):
        """
        Add a single particle to the simulation.
        
        Args:
            position: 3D position vector
            velocity: 3D velocity vector
            mass: Particle mass
            particle_type: Type identifier (0=star, 1=planet, 2=black_hole)
        """
        pass
    
    @abstractmethod
    def remove_particle(self, index: int):
        """
        Remove a particle from the simulation.
        
        Args:
            index: Index of particle to remove
        """
        pass
    
    @abstractmethod
    def reset(self):
        """Reset the simulation to initial conditions."""
        pass
    
    def get_particle_count(self) -> int:
        """Get the current number of particles."""
        return self.particle_count
    
    def is_initialized(self) -> bool:
        """Check if the engine is initialized."""
        return self.initialized
