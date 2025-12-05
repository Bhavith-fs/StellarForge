# StellarForge Quick Start Guide

Welcome to StellarForge! This guide will get you up and running in minutes.

## Prerequisites

- Windows 10/11
- Python 3.10 or higher
- PowerShell or Command Prompt

## Installation Steps

### 1. Open PowerShell
Press `Win + X` and select "Windows PowerShell" or "Terminal"

### 2. Navigate to Project Directory
```powershell
cd "C:\Users\Lenovo\Documents\StellarForge"
```

### 3. Create Virtual Environment (Recommended)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Note**: If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. Install Dependencies
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- PyQt6 (GUI framework)
- VisPy (3D visualization)
- NumPy, SciPy (numerical computing)
- Astropy (astronomy tools)
- noise (procedural generation)
- h5py (data storage)
- And other dependencies...

### 5. Verify Installation
```powershell
python -c "import PyQt6, vispy, numpy; print('All dependencies installed!')"
```

## Running StellarForge

### Method 1: Basic Launch
```powershell
python main.py
```

### Method 2: With Options
```powershell
python run.py --particles 10000 --galaxies 5 --seed 42
```

### Method 3: Demo Mode
```powershell
python run.py --demo
```

## First Time Usage

When you launch StellarForge for the first time:

1. **Wait for generation**: The app will generate an initial universe (3-5 seconds)
2. **Explore the view**: Use your mouse to rotate and zoom
3. **Try the controls**: Click the Play button in the timeline
4. **Switch modes**: Try Sandbox mode to add objects

## Basic Controls

### Camera Navigation
- **Rotate**: Click and drag with left mouse button
- **Zoom**: Scroll wheel up/down
- **Pan**: Right-click and drag

### Simulation Controls
- **Play/Pause**: Click the ▶/⏸ button
- **Reset**: Click ⏮ to reset to start
- **Speed**: Drag the speed slider (0.1x - 10.0x)

### Modes
- **Observation Mode**: View-only mode for exploring
- **Sandbox Mode**: Add stars, planets, and black holes

## Example Workflows

### Workflow 1: Generate a Custom Universe
1. Launch the app: `python main.py`
2. File → New Simulation
3. Watch the procedural generation
4. Click Play to start simulation
5. File → Save Scenario to save your universe

### Workflow 2: Add Objects in Sandbox Mode
1. Switch to Sandbox Mode (right panel)
2. Click "🌟 Add Star" to spawn a star
3. Click "🌍 Add Planet" to add a planet
4. Click Play to see them interact

### Workflow 3: Save and Load
1. Create an interesting simulation
2. File → Save Scenario
3. Name it (e.g., "my_galaxy")
4. Close and reopen the app
5. File → Load Scenario → Select "my_galaxy"

## Troubleshooting

### Problem: "Python is not recognized..."
**Solution**: Make sure Python is in your PATH. Try:
```powershell
py main.py
```

### Problem: Import errors
**Solution**: Activate virtual environment and reinstall:
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Problem: Black screen in 3D view
**Solution**: Update graphics drivers or try software rendering by editing `main.py`:
```python
# Add at the top after imports
import vispy
vispy.use('pyqt6', 'gl2')
```

### Problem: Slow performance
**Solution**: Reduce particle count by editing `config/default_settings.json`:
```json
"simulation": {
  "default_particle_count": 1000
}
```

### Problem: Window too large/small
**Solution**: Edit `config/default_settings.json`:
```json
"window": {
  "width": 1024,
  "height": 768
}
```

## Next Steps

1. **Read the README**: Full documentation in `README.md`
2. **Try Examples**: Check `examples/` directory
3. **Run Tests**: `python -m unittest discover tests`
4. **Customize**: Edit `config/default_settings.json`
5. **Experiment**: Generate different galaxy configurations

## Getting Help

- Check `README.md` for detailed documentation
- Review `examples/` for code samples
- Open an issue on GitHub if you encounter bugs

## Performance Tips

- Start with fewer particles (~1000) on slower machines
- Disable "Show Gravity Lines" for better performance
- Use lower simulation speeds for smoother visuals
- Close other GPU-intensive applications

## Advanced Usage

### Running Tests
```powershell
python -m unittest tests/test_engine.py
python -m unittest tests/test_proc_gen.py
```

### Generating Specific Configurations
Edit the initialization in `src/gui/main_window.py`:
```python
positions, velocities, types = self.universe_generator.generate_universe(
    seed=42,              # Change for different results
    num_galaxies=10,      # More galaxies
    world_scale=200.0     # Larger universe
)
```

### Viewing Saved Data
Scenarios are saved in the `data/` directory:
- `*_settings.json` - Simulation settings
- `*_particles.h5` - Particle data (HDF5 format)

## What's Next?

Now that you're set up, explore these features:

- ✨ **Procedural Generation**: Create unique universes
- 🎮 **Interactive Sandbox**: Build your own cosmos
- 💾 **Save/Load**: Preserve your creations
- 🎬 **Timeline**: Control time itself
- 🔭 **Observation**: Study cosmic structures

**Enjoy exploring the cosmos with StellarForge!** 🌌

---

*For more information, see the full README.md*
