"""
Galaxy visualizer for rendering entire galaxies as structures.
"""

import numpy as np
from vispy import scene
from vispy.scene import visuals


class GalaxyVisualizer:
    """
    Visualizer for galaxy-level structures.
    Can render galaxies with spiral arms, elliptical halos, etc.
    """
    
    def __init__(self, view: scene.ViewBox):
        """
        Initialize galaxy visualizer.
        
        Args:
            view: VisPy ViewBox to render in
        """
        self.view = view
        
        # Create markers for galaxy particles
        self.markers = visuals.Markers(parent=view.scene)
        self.markers.set_gl_state('translucent', blend=True, depth_test=True)
        
        # Optional: Lines for spiral arms (not implemented yet)
        self.spiral_lines = []
    
    def update(self, positions: np.ndarray, colors: np.ndarray,
              galaxy_centers: np.ndarray = None):
        """
        Update galaxy visualization.
        
        Args:
            positions: All particle positions (N, 3)
            colors: Particle colors (N, 3)
            galaxy_centers: Positions of galaxy centers (M, 3) for highlighting
        """
        if len(positions) == 0:
            return
        
        # Render all particles
        self.markers.set_data(
            pos=positions,
            face_color=colors,
            edge_color=None,
            size=4.0
        )
        
        # TODO: Add galaxy center markers if provided
        # TODO: Add spiral arm lines for spiral galaxies
    
    def highlight_galaxy(self, galaxy_center: np.ndarray, radius: float = 10.0):
        """
        Highlight a specific galaxy (e.g., when selected).
        
        Args:
            galaxy_center: Center position of the galaxy
            radius: Approximate radius of the galaxy
        """
        # TODO: Add a sphere or circle overlay to highlight the galaxy
        pass
    
    def clear(self):
        """Clear all galaxy visualizations."""
        self.markers.set_data(pos=np.zeros((0, 3)))
