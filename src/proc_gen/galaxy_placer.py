"""
Galaxy placement logic based on density fields.
"""

import numpy as np
from typing import List, Tuple, Dict


class GalaxyPlacer:
    """
    Places galaxies in the universe based on density field analysis.
    """
    
    def __init__(self):
        self.galaxy_positions: List[np.ndarray] = []
        self.galaxy_properties: List[Dict] = []
    
    def place_galaxies(self, density_positions: np.ndarray,
                      num_galaxies: int = None,
                      min_separation: float = 10.0) -> Tuple[List[np.ndarray], List[Dict]]:
        """
        Place galaxies at high-density positions.
        
        Args:
            density_positions: High-density positions from density field (N, 3)
            num_galaxies: Number of galaxies to place (None = use all positions)
            min_separation: Minimum distance between galaxies
        
        Returns:
            Tuple of (positions list, properties list)
        """
        if len(density_positions) == 0:
            return [], []
        
        # Determine number of galaxies
        if num_galaxies is None:
            num_galaxies = len(density_positions)
        else:
            num_galaxies = min(num_galaxies, len(density_positions))
        
        # Select galaxy positions with minimum separation
        selected_positions = []
        selected_indices = []
        
        # Start with a random position
        available_indices = list(range(len(density_positions)))
        np.random.shuffle(available_indices)
        
        for idx in available_indices:
            if len(selected_positions) >= num_galaxies:
                break
            
            pos = density_positions[idx]
            
            # Check separation from existing galaxies
            if len(selected_positions) == 0:
                selected_positions.append(pos)
                selected_indices.append(idx)
            else:
                distances = np.linalg.norm(
                    np.array(selected_positions) - pos, axis=1
                )
                if np.all(distances >= min_separation):
                    selected_positions.append(pos)
                    selected_indices.append(idx)
        
        # Generate properties for each galaxy
        self.galaxy_positions = selected_positions
        self.galaxy_properties = []
        
        for i, pos in enumerate(selected_positions):
            properties = self._generate_galaxy_properties(pos)
            self.galaxy_properties.append(properties)
        
        return self.galaxy_positions, self.galaxy_properties
    
    def _generate_galaxy_properties(self, position: np.ndarray) -> Dict:
        """
        Generate random properties for a galaxy.
        
        Args:
            position: Galaxy center position
        
        Returns:
            Dictionary of galaxy properties
        """
        # Galaxy types: spiral, elliptical, irregular
        galaxy_type = np.random.choice(
            ['spiral', 'elliptical', 'irregular'],
            p=[0.6, 0.3, 0.1]
        )
        
        # Size (number of stars)
        if galaxy_type == 'spiral':
            star_count = np.random.randint(1000, 5000)
        elif galaxy_type == 'elliptical':
            star_count = np.random.randint(500, 3000)
        else:  # irregular
            star_count = np.random.randint(200, 1000)
        
        # Rotation (for spiral galaxies)
        rotation_speed = np.random.uniform(0.5, 2.0) if galaxy_type == 'spiral' else 0.0
        
        # Size scale
        size_scale = np.random.uniform(3.0, 10.0)
        
        # Orientation (axis of rotation)
        orientation = np.random.randn(3)
        orientation = orientation / np.linalg.norm(orientation)
        
        return {
            'type': galaxy_type,
            'position': position,
            'star_count': star_count,
            'size_scale': size_scale,
            'rotation_speed': rotation_speed,
            'orientation': orientation,
            'color_tint': np.random.uniform([0.8, 0.8, 0.9], [1.0, 1.0, 1.0])
        }
    
    def generate_galaxy_particles(self, galaxy_idx: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate particle positions and velocities for a specific galaxy.
        
        Args:
            galaxy_idx: Index of the galaxy
        
        Returns:
            Tuple of (positions, velocities) arrays
        """
        if galaxy_idx >= len(self.galaxy_properties):
            raise ValueError(f"Invalid galaxy index: {galaxy_idx}")
        
        props = self.galaxy_properties[galaxy_idx]
        center = props['position']
        count = props['star_count']
        scale = props['size_scale']
        galaxy_type = props['type']
        
        if galaxy_type == 'spiral':
            positions, velocities = self._generate_spiral_galaxy(
                center, count, scale, props['rotation_speed'], props['orientation']
            )
        elif galaxy_type == 'elliptical':
            positions, velocities = self._generate_elliptical_galaxy(
                center, count, scale
            )
        else:  # irregular
            positions, velocities = self._generate_irregular_galaxy(
                center, count, scale
            )
        
        return positions, velocities
    
    def _generate_spiral_galaxy(self, center: np.ndarray, count: int,
                               scale: float, rotation_speed: float,
                               orientation: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Generate spiral galaxy structure."""
        # Central bulge (30%) and spiral arms (70%)
        bulge_count = int(count * 0.3)
        arm_count = count - bulge_count
        
        # Bulge: spherical distribution
        bulge_pos = np.random.randn(bulge_count, 3) * scale * 0.3
        bulge_vel = np.zeros((bulge_count, 3))
        
        # Spiral arms
        r = np.random.exponential(scale * 0.4, arm_count)
        theta = np.random.uniform(0, 4 * np.pi, arm_count)
        theta += r / (scale * 0.2) * np.pi  # Spiral pattern
        z = np.random.normal(0, scale * 0.05, arm_count)
        
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        arm_pos = np.column_stack([x, y, z])
        
        # Orbital velocities
        v_mag = rotation_speed / np.sqrt(np.maximum(r, 0.1))
        vx = -np.sin(theta) * v_mag
        vy = np.cos(theta) * v_mag
        vz = np.random.normal(0, 0.05, arm_count)
        arm_vel = np.column_stack([vx, vy, vz])
        
        # Combine
        positions = np.vstack([bulge_pos, arm_pos]) + center
        velocities = np.vstack([bulge_vel, arm_vel])
        
        return positions, velocities
    
    def _generate_elliptical_galaxy(self, center: np.ndarray, count: int,
                                   scale: float) -> Tuple[np.ndarray, np.ndarray]:
        """Generate elliptical galaxy structure."""
        # Spherical with random motion
        positions = np.random.randn(count, 3)
        distances = np.linalg.norm(positions, axis=1, keepdims=True)
        positions = positions / np.maximum(distances, 0.01)
        
        # Random radii with preference for center
        radii = np.random.exponential(scale * 0.5, (count, 1))
        positions = positions * radii + center
        
        # Random velocities (no organized rotation)
        velocities = np.random.randn(count, 3) * 0.2
        
        return positions, velocities
    
    def _generate_irregular_galaxy(self, center: np.ndarray, count: int,
                                  scale: float) -> Tuple[np.ndarray, np.ndarray]:
        """Generate irregular galaxy structure."""
        # Clumpy, asymmetric distribution
        positions = np.random.uniform(-scale, scale, (count, 3))
        
        # Add some clumps
        num_clumps = np.random.randint(2, 5)
        for _ in range(num_clumps):
            clump_center = np.random.uniform(-scale * 0.5, scale * 0.5, 3)
            clump_size = np.random.uniform(scale * 0.2, scale * 0.4)
            clump_count = count // num_clumps
            
            clump_positions = np.random.randn(clump_count, 3) * clump_size + clump_center
            positions[:clump_count] = clump_positions
        
        positions += center
        
        # Chaotic velocities
        velocities = np.random.randn(count, 3) * 0.3
        
        return positions, velocities
