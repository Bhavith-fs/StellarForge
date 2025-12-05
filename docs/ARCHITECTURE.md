# StellarForge Architecture Overview

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE LAYER                      │
│                           (PyQt6)                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ MainWindow   │  │ ControlPanel │  │TimelineWidget│         │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤         │
│  │ - Menu Bar   │  │ - Mode Toggle│  │ - Play/Pause │         │
│  │ - Canvas     │  │ - Spawner    │  │ - Speed      │         │
│  │ - Timer      │  │ - Physics    │  │ - Time Info  │         │
│  │ - Signals    │  │ - Signals    │  │ - Signals    │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
│         │                  │                  │                  │
└─────────┼──────────────────┼──────────────────┼─────────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      APPLICATION STATE                           │
│                         (Core)                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────┐    ┌─────────────────────────┐    │
│  │      AppState          │    │   ScenarioManager       │    │
│  ├────────────────────────┤    ├─────────────────────────┤    │
│  │ - mode                 │    │ - save_scenario()       │    │
│  │ - is_playing           │    │ - load_scenario()       │    │
│  │ - positions (N×3)      │    │ - list_scenarios()      │    │
│  │ - velocities (N×3)     │    │ - HDF5 + JSON          │    │
│  │ - colors (N×3)         │    │                         │    │
│  │ - types (N)            │    │                         │    │
│  │ - snapshots []         │    │                         │    │
│  └────────┬───────────────┘    └─────────────────────────┘    │
│           │                                                     │
└───────────┼─────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   VISUALIZATION LAYER                            │
│                        (VisPy)                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐  ┌───────────────────┐  ┌─────────────┐ │
│  │ UniverseRenderer │  │StarFieldVisualizer│  │   Galaxy    │ │
│  ├──────────────────┤  ├───────────────────┤  │ Visualizer  │ │
│  │ - SceneCanvas    │  │ - Stars visual    │  │ - Structure │ │
│  │ - Markers        │  │ - Planets visual  │  │ - Highlight │ │
│  │ - Camera         │  │ - BlackHoles vis. │  │             │ │
│  │ - update()       │  │ - Type separation │  │             │ │
│  └──────────────────┘  └───────────────────┘  └─────────────┘ │
│                                                                  │
│         OpenGL Hardware Acceleration (GPU)                      │
└─────────────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SIMULATION ENGINE                             │
│                     (Engine Bridge)                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              SimulationEngine (ABC)                      │   │
│  │  ┌──────────────────────────────────────────────────┐   │   │
│  │  │ + initialize(count, **kwargs)                    │   │   │
│  │  │ + step(dt)                                       │   │   │
│  │  │ + get_positions() → ndarray                      │   │   │
│  │  │ + get_velocities() → ndarray                     │   │   │
│  │  │ + add_particle(pos, vel, mass, type)            │   │   │
│  │  │ + remove_particle(index)                         │   │   │
│  │  └──────────────────────────────────────────────────┘   │   │
│  └──────────────────┬────────────────────────────────────────┘   │
│                     │                                             │
│        ┌────────────┴────────────┐                              │
│        │                         │                              │
│   ┌────▼──────┐          ┌──────▼────────┐                     │
│   │MockEngine │          │  C++ Engine   │  (Future)           │
│   ├───────────┤          ├───────────────┤                     │
│   │ - Random  │          │ - Real N-body │                     │
│   │ - Linear  │          │ - Collisions  │                     │
│   │ - Simple  │          │ - Optimized   │                     │
│   │   gravity │          │ - Parallel    │                     │
│   └───────────┘          └───────────────┘                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────────┐
│                 PROCEDURAL GENERATION                            │
│                      (ProcGen)                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────┐  ┌─────────────┐  ┌──────────────────┐    │
│  │ DensityField   │  │GalaxyPlacer │  │UniverseGenerator │    │
│  ├────────────────┤  ├─────────────┤  ├──────────────────┤    │
│  │ - Perlin noise │─▶│ - Placement │─▶│ - Orchestrate    │    │
│  │ - Simplex noise│  │ - Separation│  │ - Generate all   │    │
│  │ - Threshold    │  │ - Properties│  │ - Combine        │    │
│  │ - Positions    │  │ - Types     │  │                  │    │
│  └────────────────┘  └─────────────┘  └──────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### Initialization Flow
```
MainWindow.__init__()
    │
    ├─▶ Create AppState()
    ├─▶ Create MockEngine()
    ├─▶ Create ScenarioManager()
    ├─▶ Create UniverseGenerator()
    │
    ├─▶ init_ui()
    │   ├─▶ Create VisPy Canvas
    │   ├─▶ Create UniverseRenderer()
    │   ├─▶ Create ControlPanel()
    │   ├─▶ Create TimelineWidget()
    │   └─▶ Connect signals/slots
    │
    └─▶ init_engine()
        ├─▶ UniverseGenerator.generate_universe()
        │   ├─▶ DensityField.generate()
        │   ├─▶ GalaxyPlacer.place_galaxies()
        │   └─▶ Generate particles
        │
        ├─▶ MockEngine.initialize()
        ├─▶ Update AppState
        └─▶ UniverseRenderer.update_particles()
```

### Simulation Loop Flow
```
User clicks Play
    │
    ▼
TimelineWidget.play_pause_clicked (signal)
    │
    ▼
MainWindow.on_play_pause()
    │
    ├─▶ AppState.is_playing = True
    └─▶ update_timer.start() [16ms interval]
        │
        └─▶ MainWindow.update_simulation() [every frame]
            │
            ├─▶ MockEngine.step(dt)
            │   └─▶ Update particle positions/velocities
            │
            ├─▶ AppState.update_time()
            │   └─▶ Check for snapshot
            │
            ├─▶ Update AppState arrays
            │
            ├─▶ UniverseRenderer.update_particles()
            │   └─▶ VisPy GPU rendering
            │
            └─▶ TimelineWidget.update_time()
```

### Object Spawning Flow (Sandbox Mode)
```
User clicks "Add Star"
    │
    ▼
ControlPanel.spawn_object (signal)
    │
    ▼
MainWindow.on_spawn_object('star')
    │
    ├─▶ Check mode == SANDBOX
    │
    ├─▶ Generate random position/velocity
    │
    ├─▶ MockEngine.add_particle()
    │   ├─▶ Append to positions array
    │   ├─▶ Append to velocities array
    │   ├─▶ Append to colors array
    │   └─▶ particle_count++
    │
    ├─▶ Update AppState arrays
    │
    ├─▶ UniverseRenderer.update_particles()
    │
    └─▶ TimelineWidget.update_particle_count()
```

### Save/Load Flow
```
Save:
    User → File → Save Scenario
        │
        ▼
    MainWindow.on_save_scenario()
        │
        ├─▶ QFileDialog (get name)
        │
        └─▶ ScenarioManager.save_scenario()
            ├─▶ AppState.to_dict() → JSON
            │   └─▶ data/scenario_settings.json
            │
            └─▶ Particle arrays → HDF5
                └─▶ data/scenario_particles.h5
                    ├─▶ /positions
                    ├─▶ /velocities
                    ├─▶ /colors
                    └─▶ /snapshots/*

Load:
    User → File → Load Scenario
        │
        ▼
    MainWindow.on_load_scenario()
        │
        ├─▶ QFileDialog (select scenario)
        │
        └─▶ ScenarioManager.load_scenario()
            ├─▶ Read JSON → AppState.from_dict()
            ├─▶ Read HDF5 → AppState arrays
            ├─▶ MockEngine.set_positions()
            ├─▶ MockEngine.set_velocities()
            └─▶ UniverseRenderer.update_particles()
```

## Component Interactions

### Signal/Slot Connections
```
ControlPanel signals:
    - mode_changed → MainWindow.on_mode_changed
    - spawn_object → MainWindow.on_spawn_object
    - physics_toggle → MainWindow.on_physics_toggle

TimelineWidget signals:
    - play_pause_clicked → MainWindow.on_play_pause
    - reset_clicked → MainWindow.on_reset
    - speed_changed → MainWindow.on_speed_changed
```

## Technology Stack Layers

```
┌───────────────────────────────────────────┐
│         User Interface (Python)           │
│              PyQt6 Widgets                │
└───────────────┬───────────────────────────┘
                │
┌───────────────▼───────────────────────────┐
│       3D Rendering (Python/OpenGL)        │
│         VisPy Scene Graph API             │
└───────────────┬───────────────────────────┘
                │
┌───────────────▼───────────────────────────┐
│      Numerical Computing (Python)         │
│    NumPy Arrays, SciPy Functions          │
└───────────────┬───────────────────────────┘
                │
┌───────────────▼───────────────────────────┐
│         Physics Engine (Python)           │
│        MockEngine (Current)               │
│        C++ Engine (Future)                │
└───────────────────────────────────────────┘
```

## Design Patterns Used

### 1. Model-View-Controller (MVC)
- **Model**: AppState, ScenarioManager
- **View**: MainWindow, ControlPanel, TimelineWidget
- **Controller**: Signal/slot connections, event handlers

### 2. Bridge Pattern
- **Abstraction**: SimulationEngine (interface)
- **Implementation**: MockEngine, (future: CppEngine)

### 3. Strategy Pattern
- **Context**: UniverseGenerator
- **Strategies**: DensityField, GalaxyPlacer (different algorithms)

### 4. Observer Pattern
- **Subject**: UI widgets (ControlPanel, TimelineWidget)
- **Observers**: MainWindow (via signals/slots)

### 5. Facade Pattern
- **Facade**: UniverseGenerator
- **Subsystems**: DensityField, GalaxyPlacer

## Module Dependencies

```
main.py
  └─▶ gui.MainWindow
      ├─▶ gui.ControlPanel
      ├─▶ gui.TimelineWidget
      ├─▶ vis.UniverseRenderer
      ├─▶ core.AppState
      ├─▶ core.ScenarioManager
      ├─▶ engine_bridge.MockEngine
      └─▶ proc_gen.UniverseGenerator
          ├─▶ proc_gen.DensityField
          └─▶ proc_gen.GalaxyPlacer
```

## File Organization by Responsibility

### Presentation Layer
- `gui/main_window.py` - Main application window
- `gui/control_panel.py` - User controls
- `gui/timeline_widget.py` - Timeline controls

### Visualization Layer
- `vis/universe_renderer.py` - Core rendering
- `vis/star_field_visualizer.py` - Star-specific rendering
- `vis/galaxy_visualizer.py` - Galaxy-specific rendering

### Business Logic Layer
- `core/app_state.py` - Application state
- `core/scenario_manager.py` - Persistence

### Data Layer
- `engine_bridge/simulation_engine.py` - Engine interface
- `engine_bridge/mock_engine.py` - Mock implementation

### Generation Layer
- `proc_gen/universe_generator.py` - Main orchestrator
- `proc_gen/density_field.py` - Noise generation
- `proc_gen/galaxy_placer.py` - Placement logic

## Thread and Process Model

### Main Thread
- PyQt6 event loop
- UI updates
- Signal/slot processing

### Render Thread (implicit)
- VisPy OpenGL context
- GPU command submission

### Future: Worker Threads
- Physics calculations (C++ engine)
- Heavy computations (galaxy generation)
- I/O operations (save/load)

## Memory Management

### Static Allocations
- UI widgets (created once)
- OpenGL buffers (updated, not recreated)
- Configuration data

### Dynamic Allocations
- NumPy arrays (positions, velocities, colors)
- Particle data grows/shrinks with add/remove
- Snapshots (circular buffer, limited size)

### Memory Optimization
- GPU memory for rendering (VisPy handles)
- CPU memory for physics (NumPy contiguous arrays)
- HDF5 compression for saved scenarios

## Performance Considerations

### Bottlenecks
1. **Physics calculations** (CPU-bound) → C++ engine will solve
2. **Rendering** (GPU-bound) → Already optimized with VisPy
3. **Memory bandwidth** (large arrays) → Use contiguous arrays

### Optimizations Applied
- GPU-accelerated rendering (VisPy)
- Efficient array operations (NumPy)
- Minimal Python loops (vectorized operations)
- Timer-based updates (60 FPS)

### Future Optimizations
- Multi-threading (C++ engine)
- LOD (Level of Detail) for distant particles
- Spatial partitioning (octree/BVH)
- Instanced rendering for repeated shapes
