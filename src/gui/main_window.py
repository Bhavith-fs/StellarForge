"""
Main window for StellarForge application.
Combines all UI components and integrates with VisPy rendering.
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QDockWidget, QMenuBar, QMenu, QFileDialog,
                             QMessageBox, QStatusBar)
from PyQt6.QtCore import QTimer, Qt
from vispy import scene, app

from .control_panel import ControlPanel
from .timeline_widget import TimelineWidget
from core import AppState, SimulationMode, ScenarioManager
from vis import UniverseRenderer
from engine_bridge import MockEngine
from proc_gen import UniverseGenerator

import numpy as np


class MainWindow(QMainWindow):
    """
    Main application window implementing the View in MVC pattern.
    Integrates PyQt6 UI with VisPy 3D rendering.
    """
    
    def __init__(self):
        super().__init__()
        
        # Initialize components
        self.app_state = AppState()
        self.engine = MockEngine()
        self.scenario_manager = ScenarioManager()
        self.universe_generator = UniverseGenerator()
        
        # UI components
        self.control_panel = None
        self.timeline_widget = None
        self.renderer = None
        self.canvas = None
        
        # Update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_simulation)
        self.update_timer.setInterval(16)  # ~60 FPS
        
        self.init_ui()
        self.init_engine()
    
    def init_ui(self):
        """Initialize the main window UI."""
        self.setWindowTitle("StellarForge - Cosmic Simulation")
        self.setGeometry(100, 100, 1280, 720)
        
        # Create central widget with VisPy canvas
        central_widget = QWidget()
        central_layout = QVBoxLayout()
        central_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create VisPy canvas
        self.canvas = scene.SceneCanvas(keys='interactive', show=False)
        self.canvas.native.setParent(central_widget)
        
        # Initialize renderer
        self.renderer = UniverseRenderer(self.canvas)
        self.renderer.set_background_color((0.02, 0.02, 0.05, 1.0))  # Dark space
        
        central_layout.addWidget(self.canvas.native)
        
        # Create timeline widget
        self.timeline_widget = TimelineWidget()
        self.timeline_widget.play_pause_clicked.connect(self.on_play_pause)
        self.timeline_widget.reset_clicked.connect(self.on_reset)
        self.timeline_widget.speed_changed.connect(self.on_speed_changed)
        central_layout.addWidget(self.timeline_widget)
        
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)
        
        # Create control panel dock
        self.control_panel = ControlPanel()
        self.control_panel.mode_changed.connect(self.on_mode_changed)
        self.control_panel.spawn_object.connect(self.on_spawn_object)
        self.control_panel.physics_toggle.connect(self.on_physics_toggle)
        
        dock = QDockWidget("Controls", self)
        dock.setWidget(self.control_panel)
        dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable |
                        QDockWidget.DockWidgetFeature.DockWidgetFloatable)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)
        
        # Create menu bar
        self.create_menus()
        
        # Create status bar
        self.statusBar().showMessage("Ready")
    
    def create_menus(self):
        """Create application menus."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        new_action = file_menu.addAction("New Simulation")
        new_action.triggered.connect(self.on_new_simulation)
        
        file_menu.addSeparator()
        
        save_action = file_menu.addAction("Save Scenario")
        save_action.triggered.connect(self.on_save_scenario)
        
        load_action = file_menu.addAction("Load Scenario")
        load_action.triggered.connect(self.on_load_scenario)
        
        file_menu.addSeparator()
        
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        reset_camera_action = view_menu.addAction("Reset Camera")
        reset_camera_action.triggered.connect(self.renderer.reset_camera)
        
        toggle_axis_action = view_menu.addAction("Toggle Axis")
        toggle_axis_action.triggered.connect(self.renderer.toggle_axis)
        
        toggle_grid_action = view_menu.addAction("Toggle Grid")
        toggle_grid_action.triggered.connect(self.renderer.toggle_grid)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.show_about)
    
    def init_engine(self):
        """Initialize simulation engine with default particles."""
        # Generate a small universe for demonstration
        print("Generating initial universe...")
        
        # Option 1: Use procedural generation
        positions, velocities, types = self.universe_generator.generate_universe(
            seed=42,
            volume_size=(32, 32, 32),
            num_galaxies=3,
            world_scale=150.0
        )
        
        # Initialize engine with generated data
        self.engine.initialize(len(positions), distribution='sphere', scale=50.0)
        self.engine.set_positions(positions)
        self.engine.set_velocities(velocities)
        
        # Update app state
        self.app_state.positions = self.engine.get_positions()
        self.app_state.velocities = self.engine.get_velocities()
        self.app_state.masses = self.engine.get_masses()
        self.app_state.colors = self.engine.get_colors()
        self.app_state.types = self.engine.get_types()
        
        # Initial render
        self.update_visualization()
        self.timeline_widget.update_particle_count(self.app_state.get_particle_count())
        
        self.statusBar().showMessage(f"Initialized with {self.app_state.get_particle_count()} particles")
    
    def update_simulation(self):
        """Update simulation step (called by timer)."""
        if not self.app_state.is_playing:
            return
        
        # Step the engine
        dt = self.app_state.dt * self.app_state.simulation_speed
        self.engine.step(dt)
        
        # Update app state
        self.app_state.positions = self.engine.get_positions()
        self.app_state.velocities = self.engine.get_velocities()
        self.app_state.update_time(self.app_state.dt)
        
        # Update visualization
        self.update_visualization()
        
        # Update UI
        self.timeline_widget.update_time(self.app_state.current_time)
    
    def update_visualization(self):
        """Update the 3D visualization."""
        if self.app_state.positions is not None:
            self.renderer.update_particles(
                self.app_state.positions,
                self.app_state.colors
            )
    
    def on_play_pause(self, is_playing: bool):
        """Handle play/pause."""
        self.app_state.is_playing = is_playing
        
        if is_playing:
            self.update_timer.start()
            self.statusBar().showMessage("Simulation running")
        else:
            self.update_timer.stop()
            self.statusBar().showMessage("Simulation paused")
    
    def on_reset(self):
        """Handle reset."""
        self.update_timer.stop()
        self.engine.reset()
        self.app_state.reset()
        
        # Update state
        self.app_state.positions = self.engine.get_positions()
        self.app_state.velocities = self.engine.get_velocities()
        
        self.update_visualization()
        self.statusBar().showMessage("Simulation reset")
    
    def on_speed_changed(self, speed: float):
        """Handle speed change."""
        self.app_state.set_speed(speed)
    
    def on_mode_changed(self, mode: SimulationMode):
        """Handle mode change."""
        self.app_state.set_mode(mode)
        mode_name = "Sandbox" if mode == SimulationMode.SANDBOX else "Observation"
        self.statusBar().showMessage(f"Switched to {mode_name} mode")
    
    def on_spawn_object(self, object_type: str):
        """Handle object spawning in sandbox mode."""
        if self.app_state.mode != SimulationMode.SANDBOX:
            return
        
        # Spawn at random position near camera
        position = np.random.uniform(-20, 20, 3)
        velocity = np.random.uniform(-1, 1, 3)
        mass = 1.0
        
        # Map object type
        type_map = {'star': 0, 'planet': 1, 'black_hole': 2}
        particle_type = type_map.get(object_type, 0)
        
        # Add to engine
        self.engine.add_particle(position, velocity, mass, particle_type)
        
        # Update state
        self.app_state.positions = self.engine.get_positions()
        self.app_state.velocities = self.engine.get_velocities()
        self.app_state.colors = self.engine.get_colors()
        self.app_state.types = self.engine.get_types()
        
        self.update_visualization()
        self.timeline_widget.update_particle_count(self.app_state.get_particle_count())
        self.statusBar().showMessage(f"Added {object_type}")
    
    def on_physics_toggle(self, setting: str, enabled: bool):
        """Handle physics setting toggle."""
        if setting == 'gravity_lines':
            self.app_state.show_gravity_lines = enabled
        elif setting == 'collisions':
            self.app_state.enable_collisions = enabled
        elif setting == 'relativistic':
            self.app_state.relativistic_mode = enabled
        
        self.statusBar().showMessage(f"{setting}: {'ON' if enabled else 'OFF'}")
    
    def on_new_simulation(self):
        """Create a new simulation."""
        # Stop current simulation
        self.update_timer.stop()
        self.app_state.reset()
        
        # Reinitialize engine
        self.init_engine()
        
        self.timeline_widget.set_playing(False)
        self.statusBar().showMessage("New simulation created")
    
    def on_save_scenario(self):
        """Save current scenario."""
        name, ok = QFileDialog.getSaveFileName(
            self,
            "Save Scenario",
            "",
            "Scenario Files (*.json)"
        )
        
        if ok and name:
            scenario_name = name.replace('.json', '').split('/')[-1].split('\\')[-1]
            self.scenario_manager.save_scenario(self.app_state, scenario_name)
            self.statusBar().showMessage(f"Scenario saved: {scenario_name}")
    
    def on_load_scenario(self):
        """Load a saved scenario."""
        scenarios = self.scenario_manager.list_scenarios()
        
        if not scenarios:
            QMessageBox.information(self, "No Scenarios", "No saved scenarios found.")
            return
        
        name, ok = QFileDialog.getOpenFileName(
            self,
            "Load Scenario",
            "data",
            "Settings Files (*_settings.json)"
        )
        
        if ok and name:
            scenario_name = name.replace('_settings.json', '').split('/')[-1].split('\\')[-1]
            
            if self.scenario_manager.load_scenario(scenario_name, self.app_state):
                # Update engine with loaded data
                if self.app_state.positions is not None:
                    self.engine.initialize(len(self.app_state.positions))
                    self.engine.set_positions(self.app_state.positions)
                    self.engine.set_velocities(self.app_state.velocities)
                
                self.update_visualization()
                self.timeline_widget.update_particle_count(self.app_state.get_particle_count())
                self.timeline_widget.update_time(self.app_state.current_time)
                self.statusBar().showMessage(f"Scenario loaded: {scenario_name}")
            else:
                QMessageBox.warning(self, "Load Failed", "Failed to load scenario.")
    
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About StellarForge",
            "<h2>StellarForge</h2>"
            "<p>Cosmic Simulation Application</p>"
            "<p>Built with PyQt6 and VisPy</p>"
            "<p>Features procedural galaxy generation, "
            "N-body simulation, and interactive 3D visualization.</p>"
        )
    
    def closeEvent(self, event):
        """Handle window close event."""
        self.update_timer.stop()
        event.accept()
