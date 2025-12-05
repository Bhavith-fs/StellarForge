"""
Engine bridge module for connecting to the C++ physics engine.
Contains mock implementations for testing UI without the real engine.
"""

from .simulation_engine import SimulationEngine
from .mock_engine import MockEngine

__all__ = ['SimulationEngine', 'MockEngine']
