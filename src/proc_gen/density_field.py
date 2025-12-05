"""
Density field generation using Perlin/Simplex noise.
"""

import numpy as np
from typing import Tuple

# Try to import noise library, fallback to pure Python implementation
try:
    from noise import pnoise3, snoise3
    NOISE_AVAILABLE = True
except ImportError:
    NOISE_AVAILABLE = False
    print("Warning: 'noise' package not available. Using fallback random noise generation.")


class DensityField:
    """
    Generates 3D density fields using Perlin or Simplex noise.
    Used to determine where galaxies and structures should appear.
    """
    
    def __init__(self, volume_size: Tuple[int, int, int] = (64, 64, 64)):
        """
        Initialize density field generator.
        
        Args:
            volume_size: Dimensions of the 3D volume (x, y, z)
        """
        self.volume_size = volume_size
        self.field: np.ndarray = None
    
    def _fallback_noise(self, x: float, y: float, z: float, seed: int) -> float:
        """Simple fallback noise function using NumPy random."""
        # Use coordinates and seed to generate deterministic noise
        np.random.seed(int((x * 1000 + y * 100 + z * 10 + seed) % (2**32 - 1)))
        return np.random.random() * 2 - 1
    
    def generate(self, seed: int = None, noise_type: str = 'perlin',
                 octaves: int = 4, persistence: float = 0.5,
                 lacunarity: float = 2.0, scale: float = 0.05) -> np.ndarray:
        """
        Generate a 3D density field using noise.
        
        Args:
            seed: Random seed for reproducibility
            noise_type: 'perlin' or 'simplex'
            octaves: Number of noise octaves (detail levels)
            persistence: Amplitude factor for each octave
            lacunarity: Frequency factor for each octave
            scale: Spatial frequency scale
        
        Returns:
            3D numpy array of density values (0.0 to 1.0)
        """
        if seed is None:
            seed = np.random.randint(0, 10000)
        
        sx, sy, sz = self.volume_size
        self.field = np.zeros((sx, sy, sz), dtype=np.float32)
        
        if NOISE_AVAILABLE:
            noise_func = pnoise3 if noise_type == 'perlin' else snoise3
        
            for i in range(sx):
                for j in range(sy):
                    for k in range(sz):
                        # Generate noise value
                        value = noise_func(
                            i * scale,
                            j * scale,
                            k * scale,
                            octaves=octaves,
                            persistence=persistence,
                            lacunarity=lacunarity,
                            base=seed
                        )
                        # Normalize to [0, 1]
                        self.field[i, j, k] = (value + 1.0) / 2.0
        else:
            # Fallback: Use simple random noise with smoothing
            np.random.seed(seed)
            # Generate random field
            self.field = np.random.random((sx, sy, sz)).astype(np.float32)
            # Apply Gaussian smoothing for more natural appearance
            from scipy.ndimage import gaussian_filter
            self.field = gaussian_filter(self.field, sigma=2.0)
        
        return self.field
    
    def apply_threshold(self, threshold: float = 0.5) -> np.ndarray:
        """
        Apply threshold to create binary mask.
        
        Args:
            threshold: Values above this become 1, below become 0
        
        Returns:
            Binary mask array
        """
        if self.field is None:
            raise ValueError("Field not generated yet")
        
        return (self.field > threshold).astype(np.float32)
    
    def get_high_density_positions(self, threshold: float = 0.6,
                                   max_positions: int = 100) -> np.ndarray:
        """
        Extract positions of high-density regions.
        
        Args:
            threshold: Minimum density value
            max_positions: Maximum number of positions to return
        
        Returns:
            Array of shape (N, 3) with grid coordinates
        """
        if self.field is None:
            raise ValueError("Field not generated yet")
        
        # Find high-density voxels
        high_density = np.argwhere(self.field > threshold)
        
        if len(high_density) == 0:
            return np.array([]).reshape(0, 3)
        
        # Sample if too many
        if len(high_density) > max_positions:
            indices = np.random.choice(len(high_density), max_positions, replace=False)
            high_density = high_density[indices]
        
        return high_density.astype(np.float32)
    
    def normalize_positions(self, positions: np.ndarray,
                          world_scale: float = 100.0) -> np.ndarray:
        """
        Convert grid coordinates to world coordinates.
        
        Args:
            positions: Grid coordinates (N, 3)
            world_scale: World space scale factor
        
        Returns:
            World coordinates centered around origin
        """
        if len(positions) == 0:
            return positions
        
        # Center around origin
        centered = positions - np.array(self.volume_size) / 2.0
        
        # Scale to world space
        scale_factor = world_scale / max(self.volume_size)
        world_positions = centered * scale_factor
        
        return world_positions
    
    def add_gradient(self, center: Tuple[float, float, float],
                    falloff: float = 0.3):
        """
        Add a radial density gradient (denser toward center).
        
        Args:
            center: Center point in grid coordinates (x, y, z)
            falloff: Rate of density falloff
        """
        if self.field is None:
            raise ValueError("Field not generated yet")
        
        sx, sy, sz = self.volume_size
        cx, cy, cz = center
        
        for i in range(sx):
            for j in range(sy):
                for k in range(sz):
                    # Calculate distance from center
                    dx = (i - cx) / sx
                    dy = (j - cy) / sy
                    dz = (k - cz) / sz
                    dist = np.sqrt(dx**2 + dy**2 + dz**2)
                    
                    # Apply gaussian-like falloff
                    gradient = np.exp(-dist**2 / (2 * falloff**2))
                    
                    # Multiply with existing field
                    self.field[i, j, k] *= gradient
