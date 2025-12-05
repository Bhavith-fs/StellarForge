"""
Main universe generator that combines density fields and galaxy placement.
"""

import numpy as np
from typing import Tuple, Optional

from .density_field import DensityField
from .galaxy_placer import GalaxyPlacer


class UniverseGenerator:
    """
    High-level universe generation orchestrator.
    Combines density field generation and galaxy placement.
    """
    
    def __init__(self):
        self.density_field = None
        self.galaxy_placer = GalaxyPlacer()
        self.generated_positions = None
        self.generated_velocities = None
        self.generated_types = None
    
    def generate_universe(self, seed: Optional[int] = None,
                         volume_size: Tuple[int, int, int] = (64, 64, 64),
                         num_galaxies: int = 10,
                         world_scale: float = 200.0) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Generate a complete universe with galaxies.
        
        Args:
            seed: Random seed for reproducibility
            volume_size: Size of density field volume
            num_galaxies: Number of galaxies to generate
            world_scale: Spatial scale of the universe
        
        Returns:
            Tuple of (positions, velocities, types) arrays
        """
        if seed is not None:
            np.random.seed(seed)
        
        # Step 1: Generate density field
        print(f"Generating density field {volume_size}...")
        density = DensityField(volume_size=volume_size)
        field = density.generate(
            seed=seed,
            noise_type='perlin',
            octaves=4,
            persistence=0.5,
            scale=0.05
        )
        
        # Add radial gradient to make universe center denser
        center = tuple(s // 2 for s in volume_size)
        density.add_gradient(center, falloff=0.4)
        
        # Step 2: Extract high-density positions
        print("Extracting high-density regions...")
        high_density_positions = density.get_high_density_positions(
            threshold=0.5,
            max_positions=num_galaxies * 2  # Get more candidates
        )
        
        # Convert to world coordinates
        world_positions = density.normalize_positions(
            high_density_positions,
            world_scale=world_scale
        )
        
        # Step 3: Place galaxies
        print(f"Placing {num_galaxies} galaxies...")
        galaxy_positions, galaxy_properties = self.galaxy_placer.place_galaxies(
            world_positions,
            num_galaxies=num_galaxies,
            min_separation=world_scale * 0.15
        )
        
        if len(galaxy_positions) == 0:
            print("Warning: No suitable galaxy positions found. Using random placement.")
            return self._generate_random_universe(num_galaxies, world_scale)
        
        # Step 4: Generate particles for each galaxy
        print(f"Generating particles for {len(galaxy_positions)} galaxies...")
        all_positions = []
        all_velocities = []
        all_types = []
        
        for i in range(len(galaxy_positions)):
            positions, velocities = self.galaxy_placer.generate_galaxy_particles(i)
            
            # Assign types (mostly stars)
            count = len(positions)
            types = np.zeros(count, dtype=np.int32)  # 0 = star
            
            all_positions.append(positions)
            all_velocities.append(velocities)
            all_types.append(types)
        
        # Combine all galaxies
        self.generated_positions = np.vstack(all_positions)
        self.generated_velocities = np.vstack(all_velocities)
        self.generated_types = np.concatenate(all_types)
        
        print(f"Universe generated: {len(self.generated_positions)} particles in {len(galaxy_positions)} galaxies")
        
        return self.generated_positions, self.generated_velocities, self.generated_types
    
    def _generate_random_universe(self, num_galaxies: int, 
                                  world_scale: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Fallback: Generate random universe if density field fails."""
        total_particles = num_galaxies * 1000
        positions = np.random.uniform(-world_scale/2, world_scale/2, (total_particles, 3))
        velocities = np.random.randn(total_particles, 3) * 0.5
        types = np.zeros(total_particles, dtype=np.int32)
        
        self.generated_positions = positions
        self.generated_velocities = velocities
        self.generated_types = types
        
        return positions, velocities, types
    
    def generate_density_field(self, volume_size: Tuple[int, int, int] = (64, 64, 64),
                              seed: Optional[int] = None) -> np.ndarray:
        """
        Generate just a density field (for visualization or analysis).
        
        Args:
            volume_size: Size of the 3D volume
            seed: Random seed
        
        Returns:
            3D numpy array of density values
        """
        self.density_field = DensityField(volume_size=volume_size)
        return self.density_field.generate(seed=seed)
    
    def place_galaxies(self, density_field: np.ndarray,
                      threshold: float = 0.6,
                      num_galaxies: int = 10) -> list:
        """
        Place galaxies based on an existing density field.
        
        Args:
            density_field: 3D numpy array of density values
            threshold: Minimum density for galaxy placement
            num_galaxies: Number of galaxies to place
        
        Returns:
            List of galaxy positions
        """
        # Create density field object with existing data
        self.density_field = DensityField(volume_size=density_field.shape)
        self.density_field.field = density_field
        
        # Extract high-density positions
        high_density_positions = self.density_field.get_high_density_positions(
            threshold=threshold,
            max_positions=num_galaxies * 2
        )
        
        # Normalize to world coordinates
        world_positions = self.density_field.normalize_positions(high_density_positions)
        
        # Place galaxies
        galaxy_positions, _ = self.galaxy_placer.place_galaxies(
            world_positions,
            num_galaxies=num_galaxies
        )
        
        return galaxy_positions
