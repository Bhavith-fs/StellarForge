"""
Star field visualizer for rendering individual stars and celestial objects.
"""

import numpy as np
from vispy import scene
from vispy.scene import visuals


class StarFieldVisualizer:
    """
    Specialized visualizer for star fields.
    Handles rendering of stars with proper colors and sizes based on properties.
    """
    
    # Star type constants
    STAR = 0
    PLANET = 1
    BLACK_HOLE = 2
    
    def __init__(self, view: scene.ViewBox):
        """
        Initialize star field visualizer.
        
        Args:
            view: VisPy ViewBox to render in
        """
        self.view = view
        
        # Create separate visuals for different object types
        self.stars = visuals.Markers(parent=view.scene)
        self.planets = visuals.Markers(parent=view.scene)
        self.black_holes = visuals.Markers(parent=view.scene)
        
        # Configure rendering
        self.stars.set_gl_state('translucent', blend=True, depth_test=True)
        self.planets.set_gl_state('translucent', blend=True, depth_test=True)
        self.black_holes.set_gl_state('additive', blend=True, depth_test=True)
    
    def update(self, positions: np.ndarray, colors: np.ndarray, 
              types: np.ndarray, masses: np.ndarray = None):
        """
        Update star field visualization.
        
        Args:
            positions: Particle positions (N, 3)
            colors: Particle colors (N, 3)
            types: Particle types (N,)
            masses: Particle masses (N,) - used for sizing
        """
        if len(positions) == 0:
            return
        
        # Separate by type
        star_mask = types == self.STAR
        planet_mask = types == self.PLANET
        black_hole_mask = types == self.BLACK_HOLE
        
        # Render stars
        if np.any(star_mask):
            star_pos = positions[star_mask]
            star_colors = colors[star_mask]
            
            # Size based on mass if available
            if masses is not None:
                star_masses = masses[star_mask]
                star_sizes = 3 + np.log10(star_masses + 1) * 2
            else:
                star_sizes = 5.0
            
            self.stars.set_data(
                pos=star_pos,
                face_color=star_colors,
                edge_color=None,
                size=star_sizes
            )
        else:
            self.stars.set_data(pos=np.zeros((0, 3)))
        
        # Render planets (smaller)
        if np.any(planet_mask):
            planet_pos = positions[planet_mask]
            planet_colors = colors[planet_mask]
            
            self.planets.set_data(
                pos=planet_pos,
                face_color=planet_colors,
                edge_color=(1, 1, 1, 0.3),
                size=3.0
            )
        else:
            self.planets.set_data(pos=np.zeros((0, 3)))
        
        # Render black holes (large with glow effect)
        if np.any(black_hole_mask):
            bh_pos = positions[black_hole_mask]
            bh_colors = colors[black_hole_mask]
            
            self.black_holes.set_data(
                pos=bh_pos,
                face_color=bh_colors,
                edge_color=(0.8, 0.2, 0.8, 0.8),
                size=15.0
            )
        else:
            self.black_holes.set_data(pos=np.zeros((0, 3)))
    
    def clear(self):
        """Clear all objects."""
        self.stars.set_data(pos=np.zeros((0, 3)))
        self.planets.set_data(pos=np.zeros((0, 3)))
        self.black_holes.set_data(pos=np.zeros((0, 3)))
