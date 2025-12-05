"""
Control panel widget for simulation controls and settings.
Contains mode toggles, object spawner, and physics settings.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                             QPushButton, QCheckBox, QLabel, QButtonGroup,
                             QRadioButton)
from PyQt6.QtCore import pyqtSignal

from core import SimulationMode


class ControlPanel(QWidget):
    """
    Side panel with simulation controls.
    Implements the Control aspect of the MVC pattern.
    """
    
    # Signals
    mode_changed = pyqtSignal(SimulationMode)
    spawn_object = pyqtSignal(str)  # 'star', 'planet', 'black_hole'
    physics_toggle = pyqtSignal(str, bool)  # setting name, enabled
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_mode = SimulationMode.OBSERVATION
        self.init_ui()
    
    def init_ui(self):
        """Initialize the control panel UI."""
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # Mode selection
        mode_group = self.create_mode_group()
        layout.addWidget(mode_group)
        
        # Object spawner (sandbox mode only)
        self.spawner_group = self.create_spawner_group()
        layout.addWidget(self.spawner_group)
        self.spawner_group.setEnabled(False)  # Disabled by default
        
        # Physics settings
        physics_group = self.create_physics_group()
        layout.addWidget(physics_group)
        
        # Stretch to push everything to top
        layout.addStretch()
        
        self.setLayout(layout)
        self.setMaximumWidth(250)
    
    def create_mode_group(self) -> QGroupBox:
        """Create user mode selection group."""
        group = QGroupBox("User Mode")
        layout = QVBoxLayout()
        
        # Radio buttons for mode selection
        self.observation_radio = QRadioButton("Observation Mode")
        self.sandbox_radio = QRadioButton("Sandbox Mode")
        
        self.observation_radio.setChecked(True)
        
        # Connect signals
        self.observation_radio.toggled.connect(self.on_mode_changed)
        
        layout.addWidget(self.observation_radio)
        layout.addWidget(self.sandbox_radio)
        
        # Add description
        desc = QLabel("Observation: View only\nSandbox: Add/remove objects")
        desc.setStyleSheet("color: gray; font-size: 9pt;")
        layout.addWidget(desc)
        
        group.setLayout(layout)
        return group
    
    def create_spawner_group(self) -> QGroupBox:
        """Create object spawner group."""
        group = QGroupBox("Object Spawner")
        layout = QVBoxLayout()
        
        # Spawn buttons
        self.spawn_star_btn = QPushButton("🌟 Add Star")
        self.spawn_planet_btn = QPushButton("🌍 Add Planet")
        self.spawn_blackhole_btn = QPushButton("⚫ Add Black Hole")
        
        # Connect signals
        self.spawn_star_btn.clicked.connect(lambda: self.spawn_object.emit('star'))
        self.spawn_planet_btn.clicked.connect(lambda: self.spawn_object.emit('planet'))
        self.spawn_blackhole_btn.clicked.connect(lambda: self.spawn_object.emit('black_hole'))
        
        layout.addWidget(self.spawn_star_btn)
        layout.addWidget(self.spawn_planet_btn)
        layout.addWidget(self.spawn_blackhole_btn)
        
        group.setLayout(layout)
        return group
    
    def create_physics_group(self) -> QGroupBox:
        """Create physics settings group."""
        group = QGroupBox("Physics Settings")
        layout = QVBoxLayout()
        
        # Physics toggles
        self.gravity_lines_cb = QCheckBox("Show Gravity Lines")
        self.collisions_cb = QCheckBox("Enable Collisions")
        self.relativistic_cb = QCheckBox("Relativistic Mode")
        
        # Set default states
        self.collisions_cb.setChecked(True)
        
        # Connect signals
        self.gravity_lines_cb.toggled.connect(
            lambda checked: self.physics_toggle.emit('gravity_lines', checked)
        )
        self.collisions_cb.toggled.connect(
            lambda checked: self.physics_toggle.emit('collisions', checked)
        )
        self.relativistic_cb.toggled.connect(
            lambda checked: self.physics_toggle.emit('relativistic', checked)
        )
        
        layout.addWidget(self.gravity_lines_cb)
        layout.addWidget(self.collisions_cb)
        layout.addWidget(self.relativistic_cb)
        
        # Add note about relativistic mode
        note = QLabel("(Relativistic: Mock only)")
        note.setStyleSheet("color: gray; font-size: 8pt;")
        layout.addWidget(note)
        
        group.setLayout(layout)
        return group
    
    def on_mode_changed(self, checked: bool):
        """Handle mode change."""
        if self.observation_radio.isChecked():
            self.current_mode = SimulationMode.OBSERVATION
            self.spawner_group.setEnabled(False)
        else:
            self.current_mode = SimulationMode.SANDBOX
            self.spawner_group.setEnabled(True)
        
        self.mode_changed.emit(self.current_mode)
    
    def set_mode(self, mode: SimulationMode):
        """Set the current mode programmatically."""
        if mode == SimulationMode.OBSERVATION:
            self.observation_radio.setChecked(True)
        else:
            self.sandbox_radio.setChecked(True)
    
    def get_physics_settings(self) -> dict:
        """Get current physics settings."""
        return {
            'gravity_lines': self.gravity_lines_cb.isChecked(),
            'collisions': self.collisions_cb.isChecked(),
            'relativistic': self.relativistic_cb.isChecked(),
        }
