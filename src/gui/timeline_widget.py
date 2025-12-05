"""
Timeline widget for simulation playback controls.
Contains play/pause, rewind, and speed controls.
"""

from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QPushButton, QSlider,
                             QLabel, QSpinBox, QDoubleSpinBox)
from PyQt6.QtCore import pyqtSignal, Qt
from .styles import get_button_style, TIMELINE_STYLESHEET


class TimelineWidget(QWidget):
    """
    Bottom bar with playback controls.
    """
    
    # Signals
    play_pause_clicked = pyqtSignal(bool)  # is_playing
    reset_clicked = pyqtSignal()
    speed_changed = pyqtSignal(float)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_playing = False
        self.init_ui()
        self.setup_shortcuts()
    
    def setup_shortcuts(self):
        """Setup keyboard shortcuts for timeline controls."""
        from PyQt6.QtGui import QShortcut, QKeySequence
        
        # Space bar for play/pause
        play_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Space), self)
        play_shortcut.activated.connect(self.on_play_pause)
        
        # Ctrl+R for reset
        reset_shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        reset_shortcut.activated.connect(self.on_reset)
    
    def init_ui(self):
        """Initialize the timeline UI."""
        self.setObjectName("timeline")
        self.setStyleSheet(TIMELINE_STYLESHEET)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(10)
        
        # Play/Pause button
        self.play_pause_btn = QPushButton("▶ Play")
        self.play_pause_btn.setFixedWidth(100)
        self.play_pause_btn.setStyleSheet(get_button_style("play"))
        self.play_pause_btn.setToolTip("Start simulation (Space)")
        self.play_pause_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.play_pause_btn.clicked.connect(self.on_play_pause)
        layout.addWidget(self.play_pause_btn)
        
        # Reset button
        self.reset_btn = QPushButton("⏮ Reset")
        self.reset_btn.setFixedWidth(100)
        self.reset_btn.setStyleSheet(get_button_style("reset"))
        self.reset_btn.setToolTip("Reset simulation to initial state")
        self.reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.reset_btn.clicked.connect(self.on_reset)
        layout.addWidget(self.reset_btn)
        
        # Spacer
        layout.addSpacing(20)
        
        # Time display
        time_label = QLabel("⏱ Time:")
        time_label.setProperty("class", "info")
        layout.addWidget(time_label)
        
        self.time_display = QLabel("0.00 s")
        self.time_display.setMinimumWidth(90)
        self.time_display.setProperty("class", "bold")
        self.time_display.setToolTip("Current simulation time")
        layout.addWidget(self.time_display)
        
        # Spacer
        layout.addSpacing(20)
        
        # Speed control
        speed_label = QLabel("⏱ Speed:")
        speed_label.setProperty("class", "info")
        layout.addWidget(speed_label)
        
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setMinimum(1)  # 0.1x
        self.speed_slider.setMaximum(100)  # 10.0x
        self.speed_slider.setValue(10)  # 1.0x
        self.speed_slider.setFixedWidth(180)
        self.speed_slider.setToolTip("Adjust simulation speed (0.1x - 10.0x)")
        self.speed_slider.setCursor(Qt.CursorShape.PointingHandCursor)
        self.speed_slider.valueChanged.connect(self.on_speed_changed)
        layout.addWidget(self.speed_slider)
        
        self.speed_display = QLabel("1.0x")
        self.speed_display.setMinimumWidth(60)
        self.speed_display.setProperty("class", "bold")
        self.speed_display.setToolTip("Current speed multiplier")
        layout.addWidget(self.speed_display)
        
        # Particle count display
        layout.addSpacing(20)
        particles_label = QLabel("✨ Particles:")
        particles_label.setProperty("class", "info")
        layout.addWidget(particles_label)
        
        self.particle_count_display = QLabel("0")
        self.particle_count_display.setMinimumWidth(80)
        self.particle_count_display.setProperty("class", "bold")
        self.particle_count_display.setToolTip("Total number of particles in simulation")
        layout.addWidget(self.particle_count_display)
        
        # Stretch to push everything to left
        layout.addStretch()
        
        self.setLayout(layout)
        self.setMaximumHeight(50)
    
    def on_play_pause(self):
        """Handle play/pause button click."""
        self.is_playing = not self.is_playing
        
        if self.is_playing:
            self.play_pause_btn.setText("⏸ Pause")
            self.play_pause_btn.setStyleSheet(get_button_style("pause"))
            self.play_pause_btn.setToolTip("Pause simulation (Space)")
        else:
            self.play_pause_btn.setText("▶ Play")
            self.play_pause_btn.setStyleSheet(get_button_style("play"))
            self.play_pause_btn.setToolTip("Start simulation (Space)")
        
        self.play_pause_clicked.emit(self.is_playing)
    
    def on_reset(self):
        """Handle reset button click."""
        self.is_playing = False
        self.play_pause_btn.setText("▶ Play")
        self.play_pause_btn.setStyleSheet(get_button_style("play"))
        self.play_pause_btn.setToolTip("Start simulation (Space)")
        self.update_time(0.0)
        self.reset_clicked.emit()
    
    def on_speed_changed(self, value: int):
        """Handle speed slider change."""
        speed = value / 10.0  # Convert to 0.1x - 10.0x range
        self.speed_display.setText(f"{speed:.1f}x")
        self.speed_changed.emit(speed)
    
    def update_time(self, time: float):
        """Update time display."""
        self.time_display.setText(f"{time:.2f} s")
    
    def update_particle_count(self, count: int):
        """Update particle count display."""
        self.particle_count_display.setText(f"{count:,}")
    
    def set_playing(self, playing: bool):
        """Set play state programmatically."""
        if self.is_playing != playing:
            self.on_play_pause()
