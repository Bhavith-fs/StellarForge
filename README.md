# 🌌✨ StellarForge
### Forge Galaxies. Bend Gravity. Simulate the Cosmos.

![Build](https://img.shields.io/badge/build-stable-brightgreen?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.10%2B-blue?style=for-the-badge)
![C++](https://img.shields.io/badge/C%2B%2B-17-blueviolet?style=for-the-badge)
![CUDA](https://img.shields.io/badge/CUDA-11.8%2B-76B900?style=for-the-badge&logo=nvidia)
![OpenGL](https://img.shields.io/badge/OpenGL-Real--Time-red?style=for-the-badge)
![HPC](https://img.shields.io/badge/HPC-Enabled-orange?style=for-the-badge)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows-lightgrey?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-purple?style=for-the-badge)
![Status](https://img.shields.io/badge/status-actively%20developed-success?style=for-the-badge)

🚀 **StellarForge** is a **high-performance N-body cosmic simulation engine** with **GPU acceleration** and **real-time 3D visualization**, built for large-scale astrophysical simulations and experimentation.

---

## 🌠 What is StellarForge?

StellarForge fuses **procedural galaxy generation** with **Barnes–Hut N-body physics** to simulate realistic cosmic systems at scale.

Its **hybrid architecture** separates:
- 🧠 **Physics computation** → C++ (CUDA / OpenMP)
- 🎨 **Visualization & UI** → Python (PyQt6 + VisPy)

This design enables **100k+ particles in real time**, scaling up to **1 million bodies** on modern GPUs.

Perfect for:
- Astrophysics & space simulations  
- High-Performance Computing demos  
- Research, visualization & education  
- GPU compute experimentation  

---

## 🔥 Key Features

- ⚡ **GPU-Accelerated Physics** (CUDA 11.x+)
- 🌳 **Barnes–Hut O(N log N)** gravity solver
- 🎮 **Real-time 3D rendering** (OpenGL via VisPy)
- 🌌 **Procedural galaxy generation**
  - Spiral
  - Elliptical
  - Irregular
- 🧪 **Dual simulation modes**
  - Observation Mode
  - Sandbox Mode
- ⏱ **Timeline & speed control**
- 💾 **Scenario save/load**
  - Particle data → HDF5
  - Metadata → JSON
- 🧩 **Modular MVC architecture**
- 🔌 **Pluggable physics backends**
- 🧠 Clean **Engine Bridge Pattern**
- 🛠 Designed for **scalability & experimentation**

---

## 🗂 Project Structure

StellarForge/
├── src/
│   ├── core/                   # State management & error handling
│   ├── gui/                    # PyQt6 UI components
│   ├── vis/                    # VisPy 3D rendering
│   ├── engine_bridge/          # Physics abstraction layer
│   └── proc_gen/               # Procedural universe generation
├── cpp_engine/                 # C++ / CUDA physics engine
├── config/                     # App configuration
├── data/                       # Saved simulations (HDF5 + JSON)
├── main.py                     # Application entry point
├── requirements.txt
└── setup.py

---

## 🛠 Installation

### 🔧 Prerequisites

- Python **3.10+**
- CMake **3.20+**
- C++ Compiler (GCC / MSVC / Clang)
- CUDA Toolkit **11.8+** (optional)
- Git

---

### 🐧 Linux

git clone https://github.com/SharonMathew4/StellarForge.git  
cd StellarForge  

python3 -m venv venv  
source venv/bin/activate  

pip install --upgrade pip  
pip install -r requirements.txt  

**CPU (OpenMP)**
./build_engine.sh  

**GPU (CUDA)**
./build_with_cuda.sh  

Run:
python main.py  
python main.py --engine cpp --backend openmp  
python main.py --engine cpp --backend cuda  

---

### 🪟 Windows

git clone https://github.com/SharonMathew4/StellarForge.git  
cd StellarForge  

python -m venv venv  
venv\Scripts\activate  

pip install --upgrade pip  
pip install -r requirements.txt  

**CPU**
build_engine.bat  

**GPU**
build_with_cuda.bat  

Run:
python main.py  
python main.py --engine cpp --backend openmp  
python main.py --engine cpp --backend cuda  

---

## ▶ Usage

python main.py  
python main.py --engine cpp --backend openmp  
python main.py --engine cpp --backend cuda  
python main.py --help  

---

## ⚙ Configuration

Edit `config/default_settings.json` to tweak:
- Window size & title
- Particle counts
- Camera FOV & zoom
- Physics timestep
- Procedural generation parameters

---

## 🧠 Architecture Overview

**Engine Bridge Pattern**

Available engines:
- `MockEngine` → Pure Python (testing & development)
- `CppEngine` → High-performance C++ backend

Backends:
- `single` → Single-threaded CPU
- `openmp` → Multi-threaded CPU
- `cuda` → NVIDIA GPU acceleration

Example:
from engine_bridge import CppEngine  
engine = CppEngine(backend='cuda')  
engine.initialize(100000)  
engine.step(0.016)  

---

## 📊 Performance Benchmarks

Tested on **RTX 4050**:

- MockEngine → 1k particles @ 60 FPS
- CppEngine (OpenMP) → 10k @ 60 FPS
- CppEngine (CUDA) → 100k @ 60 FPS
- CppEngine (CUDA) → 1M @ 30 FPS

---

## 🧪 Technology Stack

- UI → PyQt6
- Rendering → VisPy + OpenGL
- Physics → C++ / CUDA / OpenMP
- Bindings → pybind11
- Build → CMake
- Storage → HDF5

---

## 🐞 Troubleshooting

- Black screen → Update GPU drivers & VisPy
- Engine load error → python verify_engine.py
- Low FPS → Reduce particles or enable CUDA

---

## 📄 License

MIT License — see LICENSE file.

---

## 🌌 Final Note

**StellarForge isn’t just a simulator.  
It’s a sandbox for creating universes.**

⭐ If this project helped you, consider starring it.
