"""
Scenario management for saving and loading simulation states.
Handles persistence to JSON (settings) and HDF5 (particle data).
"""

import json
import h5py
import numpy as np
from pathlib import Path
from typing import Optional
from datetime import datetime

from .app_state import AppState


class ScenarioManager:
    """
    Manages saving and loading of simulation scenarios.
    Uses JSON for settings and HDF5 for large particle arrays.
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def save_scenario(self, app_state: AppState, name: Optional[str] = None) -> str:
        """
        Save the current scenario (settings + particle data).
        
        Args:
            app_state: The application state to save
            name: Optional scenario name (auto-generated if None)
        
        Returns:
            The name of the saved scenario
        """
        if name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = f"scenario_{timestamp}"
        
        # Save settings to JSON
        settings_path = self.data_dir / f"{name}_settings.json"
        settings = app_state.to_dict()
        settings['particle_count'] = app_state.get_particle_count()
        
        with open(settings_path, 'w') as f:
            json.dump(settings, f, indent=2)
        
        # Save particle data to HDF5
        if app_state.positions is not None:
            data_path = self.data_dir / f"{name}_particles.h5"
            with h5py.File(data_path, 'w') as f:
                f.create_dataset('positions', data=app_state.positions)
                
                if app_state.velocities is not None:
                    f.create_dataset('velocities', data=app_state.velocities)
                
                if app_state.masses is not None:
                    f.create_dataset('masses', data=app_state.masses)
                
                if app_state.colors is not None:
                    f.create_dataset('colors', data=app_state.colors)
                
                if app_state.types is not None:
                    f.create_dataset('types', data=app_state.types)
                
                # Save snapshots if any
                if app_state.snapshots:
                    snapshots_group = f.create_group('snapshots')
                    for i, snapshot in enumerate(app_state.snapshots):
                        snap_group = snapshots_group.create_group(f'snapshot_{i}')
                        snap_group.attrs['time'] = snapshot['time']
                        snap_group.create_dataset('positions', data=snapshot['positions'])
                        if snapshot['velocities'] is not None:
                            snap_group.create_dataset('velocities', data=snapshot['velocities'])
        
        return name
    
    def load_scenario(self, name: str, app_state: AppState) -> bool:
        """
        Load a saved scenario into the application state.
        
        Args:
            name: The scenario name to load
            app_state: The application state to populate
        
        Returns:
            True if successful, False otherwise
        """
        settings_path = self.data_dir / f"{name}_settings.json"
        data_path = self.data_dir / f"{name}_particles.h5"
        
        if not settings_path.exists():
            print(f"Settings file not found: {settings_path}")
            return False
        
        # Load settings from JSON
        with open(settings_path, 'r') as f:
            settings = json.load(f)
        
        app_state.from_dict(settings)
        
        # Load particle data from HDF5
        if data_path.exists():
            with h5py.File(data_path, 'r') as f:
                app_state.positions = f['positions'][:]
                
                if 'velocities' in f:
                    app_state.velocities = f['velocities'][:]
                
                if 'masses' in f:
                    app_state.masses = f['masses'][:]
                
                if 'colors' in f:
                    app_state.colors = f['colors'][:]
                
                if 'types' in f:
                    app_state.types = f['types'][:]
                
                # Load snapshots if any
                if 'snapshots' in f:
                    app_state.snapshots.clear()
                    snapshots_group = f['snapshots']
                    for snap_name in sorted(snapshots_group.keys()):
                        snap_group = snapshots_group[snap_name]
                        snapshot = {
                            'time': snap_group.attrs['time'],
                            'positions': snap_group['positions'][:],
                            'velocities': snap_group['velocities'][:] if 'velocities' in snap_group else None,
                            'masses': None,
                            'colors': None,
                            'types': None,
                        }
                        app_state.snapshots.append(snapshot)
        
        return True
    
    def list_scenarios(self) -> list:
        """Return a list of available scenario names."""
        scenarios = []
        for settings_file in self.data_dir.glob("*_settings.json"):
            scenario_name = settings_file.stem.replace("_settings", "")
            scenarios.append(scenario_name)
        return sorted(scenarios)
    
    def delete_scenario(self, name: str) -> bool:
        """Delete a scenario and its associated files."""
        settings_path = self.data_dir / f"{name}_settings.json"
        data_path = self.data_dir / f"{name}_particles.h5"
        
        deleted = False
        if settings_path.exists():
            settings_path.unlink()
            deleted = True
        
        if data_path.exists():
            data_path.unlink()
            deleted = True
        
        return deleted
    
    def export_to_json(self, name: str, output_path: str) -> bool:
        """
        Export a scenario to a single JSON file (for sharing/debugging).
        Note: Only suitable for small datasets.
        """
        settings_path = self.data_dir / f"{name}_settings.json"
        data_path = self.data_dir / f"{name}_particles.h5"
        
        if not settings_path.exists():
            return False
        
        with open(settings_path, 'r') as f:
            data = json.load(f)
        
        # Add particle data if available and not too large
        if data_path.exists():
            with h5py.File(data_path, 'r') as f:
                if 'positions' in f and len(f['positions']) < 10000:  # Limit for JSON export
                    data['positions'] = f['positions'][:].tolist()
                    if 'velocities' in f:
                        data['velocities'] = f['velocities'][:].tolist()
                    if 'colors' in f:
                        data['colors'] = f['colors'][:].tolist()
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        return True
