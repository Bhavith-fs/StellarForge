"""
Basic tests for the simulation engine.
"""

import unittest
import numpy as np
import sys
sys.path.insert(0, '../src')

from engine_bridge import MockEngine


class TestMockEngine(unittest.TestCase):
    """Test cases for MockEngine."""
    
    def setUp(self):
        """Set up test engine."""
        self.engine = MockEngine()
    
    def test_initialization(self):
        """Test engine initialization."""
        self.engine.initialize(100, seed=42)
        self.assertTrue(self.engine.is_initialized())
        self.assertEqual(self.engine.get_particle_count(), 100)
    
    def test_positions(self):
        """Test position getter."""
        self.engine.initialize(50, seed=42)
        positions = self.engine.get_positions()
        self.assertEqual(positions.shape, (50, 3))
    
    def test_step(self):
        """Test simulation step."""
        self.engine.initialize(10, seed=42)
        initial_positions = self.engine.get_positions().copy()
        
        self.engine.step(0.1)
        new_positions = self.engine.get_positions()
        
        # Positions should have changed
        self.assertFalse(np.array_equal(initial_positions, new_positions))
    
    def test_add_particle(self):
        """Test adding a particle."""
        self.engine.initialize(10, seed=42)
        initial_count = self.engine.get_particle_count()
        
        self.engine.add_particle(
            np.array([0.0, 0.0, 0.0]),
            np.array([1.0, 0.0, 0.0]),
            1.0,
            0
        )
        
        self.assertEqual(self.engine.get_particle_count(), initial_count + 1)
    
    def test_reset(self):
        """Test engine reset."""
        self.engine.initialize(10, seed=42)
        initial_positions = self.engine.get_positions().copy()
        
        # Step and modify
        self.engine.step(1.0)
        
        # Reset
        self.engine.reset()
        reset_positions = self.engine.get_positions()
        
        # Should be back to initial state
        np.testing.assert_array_almost_equal(initial_positions, reset_positions)


if __name__ == '__main__':
    unittest.main()
