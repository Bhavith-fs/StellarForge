"""
Core module for StellarForge application state and data management.
"""

from .app_state import AppState, SimulationMode
from .scenario_manager import ScenarioManager

__all__ = ['AppState', 'SimulationMode', 'ScenarioManager']
