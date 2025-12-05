# Example: Using StellarForge Components

This directory contains example scripts demonstrating how to use StellarForge components.

## Examples

### 1. Basic Engine Usage

```python
from engine_bridge import MockEngine
import numpy as np

# Initialize engine
engine = MockEngine()
engine.initialize(1000, distribution='galaxy', scale=50.0, seed=42)

# Run simulation
for _ in range(100):
    engine.step(0.016)
    positions = engine.get_positions()
    print(f"Particle 0 position: {positions[0]}")
```

### 2. Procedural Generation

```python
from proc_gen import UniverseGenerator

# Generate universe
generator = UniverseGenerator()
positions, velocities, types = generator.generate_universe(
    seed=42,
    volume_size=(64, 64, 64),
    num_galaxies=10,
    world_scale=200.0
)

print(f"Generated {len(positions)} particles in {len(set(types))} galaxy types")
```

### 3. Saving and Loading

```python
from core import AppState, ScenarioManager

# Create state
state = AppState()
state.positions = positions
state.velocities = velocities

# Save
manager = ScenarioManager()
manager.save_scenario(state, "my_universe")

# Load
new_state = AppState()
manager.load_scenario("my_universe", new_state)
```

### 4. Custom Visualization

```python
from vispy import scene
from vis import UniverseRenderer

# Create canvas
canvas = scene.SceneCanvas(keys='interactive', show=True)

# Create renderer
renderer = UniverseRenderer(canvas)
renderer.update_particles(positions, colors)

# Run
canvas.app.run()
```

## Running Examples

To run any example, save it as a `.py` file and execute:

```powershell
python example_file.py
```

Make sure StellarForge is installed first:

```powershell
pip install -e .
```
