"""
Example: Generate and visualize a galaxy using StellarForge components.
"""

import sys
sys.path.insert(0, '../src')

from vispy import scene, app
from vis import UniverseRenderer
from proc_gen import UniverseGenerator
import numpy as np


def main():
    """Generate and display a procedural galaxy."""
    
    print("Generating universe...")
    generator = UniverseGenerator()
    
    # Generate universe
    positions, velocities, types = generator.generate_universe(
        seed=42,
        volume_size=(32, 32, 32),
        num_galaxies=5,
        world_scale=100.0
    )
    
    # Generate colors based on types
    colors = np.zeros((len(positions), 3))
    for i, t in enumerate(types):
        if t == 0:  # Star
            colors[i] = [1.0, 1.0, 0.8]
        elif t == 1:  # Planet
            colors[i] = [0.5, 0.7, 1.0]
        else:  # Black hole
            colors[i] = [1.0, 0.2, 1.0]
    
    print(f"Generated {len(positions)} particles")
    
    # Create visualization
    canvas = scene.SceneCanvas(
        keys='interactive',
        show=True,
        title="StellarForge - Procedural Galaxy",
        size=(1024, 768)
    )
    
    renderer = UniverseRenderer(canvas)
    renderer.set_background_color((0.02, 0.02, 0.05, 1.0))
    renderer.update_particles(positions, colors)
    
    print("\nControls:")
    print("  - Drag: Rotate")
    print("  - Scroll: Zoom")
    print("  - Right-click drag: Pan")
    print("\nPress ESC to exit")
    
    app.run()


if __name__ == '__main__':
    main()
