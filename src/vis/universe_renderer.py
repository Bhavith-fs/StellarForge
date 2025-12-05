"""
Main universe renderer using VisPy SceneCanvas.
Handles the 3D visualization of particles.
"""

import numpy as np
from vispy import scene
from vispy.scene import visuals
from typing import Optional


class UniverseRenderer:
    """
    High-performance 3D renderer using VisPy.
    Renders particles as a point cloud with colors.
    """
    
    def __init__(self, canvas: scene.SceneCanvas):
        """
        Initialize the renderer.
        
        Args:
            canvas: VisPy SceneCanvas to render on
        """
        self.canvas = canvas
        self.view = canvas.central_widget.add_view()
        
        # Setup camera with turntable controller
        self.camera = scene.TurntableCamera(
            fov=60,
            distance=150,
            elevation=30,
            azimuth=45
        )
        self.view.camera = self.camera
        
        # Create markers visual for particles
        self.markers = visuals.Markers()
        self.markers.set_gl_state('translucent', blend=True, depth_test=True)
        self.view.add(self.markers)
        
        # Add axis for reference
        self.axis = visuals.XYZAxis(parent=self.view.scene)
        
        # Grid for reference (optional, can be toggled)
        self.grid = visuals.GridLines()
        self.grid.parent = self.view.scene
        self.grid.visible = False
        
        # Data
        self.positions: Optional[np.ndarray] = None
        self.colors: Optional[np.ndarray] = None
        self.sizes: Optional[np.ndarray] = None
        
        # Rendering settings
        self.point_size = 5.0
        self.show_axis = True
        self.show_grid = False
    
    def update_particles(self, positions: np.ndarray, 
                        colors: Optional[np.ndarray] = None,
                        sizes: Optional[np.ndarray] = None):
        """
        Update particle positions and colors.
        
        Args:
            positions: Array of shape (N, 3) with x, y, z coordinates
            colors: Array of shape (N, 3) or (N, 4) with RGB or RGBA values
            sizes: Array of shape (N,) with point sizes (optional)
        """
        if len(positions) == 0:
            return
        
        self.positions = positions
        
        # Handle colors
        if colors is None:
            # Default white color
            colors = np.ones((len(positions), 3), dtype=np.float32)
        
        # Ensure colors are in [0, 1] range
        if colors.max() > 1.0:
            colors = colors / 255.0
        
        self.colors = colors
        
        # Handle sizes
        if sizes is None:
            sizes = np.ones(len(positions)) * self.point_size
        
        self.sizes = sizes
        
        # Update markers
        self.markers.set_data(
            pos=self.positions,
            face_color=self.colors,
            edge_color=None,
            size=self.point_size
        )
    
    def clear(self):
        """Clear all particles from the view."""
        self.positions = None
        self.colors = None
        self.sizes = None
        self.markers.set_data(pos=np.zeros((0, 3)))
    
    def set_camera_position(self, distance: float = 150, 
                           elevation: float = 30,
                           azimuth: float = 45):
        """
        Set camera position.
        
        Args:
            distance: Distance from origin
            elevation: Elevation angle in degrees
            azimuth: Azimuth angle in degrees
        """
        if isinstance(self.camera, scene.TurntableCamera):
            self.camera.distance = distance
            self.camera.elevation = elevation
            self.camera.azimuth = azimuth
    
    def zoom(self, factor: float):
        """
        Zoom camera in/out.
        
        Args:
            factor: Zoom factor (>1 zooms in, <1 zooms out)
        """
        if isinstance(self.camera, scene.TurntableCamera):
            self.camera.distance /= factor
    
    def reset_camera(self):
        """Reset camera to default position."""
        self.set_camera_position(distance=150, elevation=30, azimuth=45)
    
    def toggle_axis(self):
        """Toggle visibility of coordinate axis."""
        self.show_axis = not self.show_axis
        self.axis.visible = self.show_axis
    
    def toggle_grid(self):
        """Toggle visibility of reference grid."""
        self.show_grid = not self.show_grid
        self.grid.visible = self.show_grid
    
    def set_point_size(self, size: float):
        """
        Set the size of rendered points.
        
        Args:
            size: Point size in pixels
        """
        self.point_size = size
        if self.positions is not None:
            self.markers.set_data(
                pos=self.positions,
                face_color=self.colors,
                size=self.point_size
            )
    
    def set_background_color(self, color: tuple):
        """
        Set background color.
        
        Args:
            color: RGB or RGBA tuple (values 0-1)
        """
        self.canvas.bgcolor = color
    
    def get_particle_count(self) -> int:
        """Get the number of rendered particles."""
        if self.positions is not None:
            return len(self.positions)
        return 0
    
    def screenshot(self, filename: str):
        """
        Save a screenshot of the current view.
        
        Args:
            filename: Output filename (e.g., 'screenshot.png')
        """
        img = self.canvas.render()
        from vispy.io import write_png
        write_png(filename, img)
