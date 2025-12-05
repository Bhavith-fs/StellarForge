"""
Tests for procedural generation.
"""

import unittest
import numpy as np
import sys
sys.path.insert(0, '../src')

from proc_gen import DensityField, GalaxyPlacer, UniverseGenerator


class TestDensityField(unittest.TestCase):
    """Test cases for DensityField."""
    
    def test_generation(self):
        """Test density field generation."""
        density = DensityField(volume_size=(32, 32, 32))
        field = density.generate(seed=42)
        
        self.assertEqual(field.shape, (32, 32, 32))
        self.assertTrue(np.all(field >= 0.0))
        self.assertTrue(np.all(field <= 1.0))
    
    def test_high_density_positions(self):
        """Test extracting high-density positions."""
        density = DensityField(volume_size=(16, 16, 16))
        density.generate(seed=42)
        
        positions = density.get_high_density_positions(threshold=0.6, max_positions=10)
        
        self.assertLessEqual(len(positions), 10)
        if len(positions) > 0:
            self.assertEqual(positions.shape[1], 3)


class TestGalaxyPlacer(unittest.TestCase):
    """Test cases for GalaxyPlacer."""
    
    def test_galaxy_placement(self):
        """Test galaxy placement."""
        placer = GalaxyPlacer()
        positions = np.random.randn(20, 3) * 10
        
        galaxy_pos, galaxy_props = placer.place_galaxies(
            positions,
            num_galaxies=5,
            min_separation=5.0
        )
        
        self.assertLessEqual(len(galaxy_pos), 5)
        self.assertEqual(len(galaxy_pos), len(galaxy_props))
    
    def test_galaxy_generation(self):
        """Test galaxy particle generation."""
        placer = GalaxyPlacer()
        positions = np.array([[0, 0, 0], [10, 10, 10]], dtype=np.float32)
        
        galaxy_pos, galaxy_props = placer.place_galaxies(positions, num_galaxies=2)
        
        for i in range(len(galaxy_pos)):
            particles, velocities = placer.generate_galaxy_particles(i)
            self.assertGreater(len(particles), 0)
            self.assertEqual(particles.shape[1], 3)
            self.assertEqual(velocities.shape, particles.shape)


class TestUniverseGenerator(unittest.TestCase):
    """Test cases for UniverseGenerator."""
    
    def test_universe_generation(self):
        """Test complete universe generation."""
        generator = UniverseGenerator()
        
        positions, velocities, types = generator.generate_universe(
            seed=42,
            volume_size=(16, 16, 16),
            num_galaxies=2,
            world_scale=50.0
        )
        
        self.assertGreater(len(positions), 0)
        self.assertEqual(positions.shape[1], 3)
        self.assertEqual(velocities.shape, positions.shape)
        self.assertEqual(len(types), len(positions))


if __name__ == '__main__':
    unittest.main()
