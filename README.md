# 🌌 StellarForge  
![Build](https://img.shields.io/badge/build-stable-brightgreen)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![CUDA](https://img.shields.io/badge/CUDA-11.8%2B-green)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows-lightgrey)
![License](https://img.shields.io/badge/license-MIT-purple)
![Status](https://img.shields.io/badge/status-active-success)

High-performance **N-body cosmic simulation engine** with GPU acceleration via **CUDA** and real-time **3D visualization**. Built with **Python (PyQt6, VisPy)** for UI and **C++** for physics computation.

---

## 🚀 Overview

**StellarForge** combines procedural galaxy generation with large-scale N-body physics using the **Barnes–Hut octree algorithm**.  
Its hybrid architecture cleanly separates the UI layer (Python) from the compute layer (C++ with optional CUDA), enabling **real-time simulation of 100k+ particles** on modern hardware.

Designed for:
- Astrophysics experimentation  
- High-performance computing demos  
- Simulation & visualization research  

---

## ✨ Features

- ⚡ GPU-accelerated N-body physics (CUDA 11.x+)
- 🌳 Barnes–Hut O(N log N) gravity solver
- 🎮 Real-time 3D rendering via VisPy (OpenGL)
- 🌌 Procedural galaxy generation (spiral, elliptical, irregular)
- 💾 Scenario save/load (HDF5 + JSON)
- 🔁 Dual modes: Observation & Sandbox
- ⏱ Timeline controls with variable simulation speed
- 🧩 MVC architecture with pluggable physics backends

---

## 🗂 Project Structure

StellarForge/
├── src/
│   ├── core/                   # State & error handling
│   ├── gui/                    # PyQt6 UI
│   ├── vis/                    # 3D visualization (VisPy)
│   ├── engine_bridge/          # Physics engine abstraction
│   └── proc_gen/               # Procedural universe generation
├── cpp_engine/                 # C++ / CUDA physics engine
├── config/                     # App configuration
├── data/                       # Saved simulations
├── main.py                     # Entry point
├── requirements.txt
└── setup.py

---

## 🛠 Installation

### Prerequisites

- Python 3.10+
- CMake 3.20+
- C++ Compiler (GCC / MSVC / Clang)
- CUDA Toolkit 11.8+ (optional)
- Git

---

### 🐧 Linux Setup

git clone https://github.com/SharonMathew4/StellarForge.git  
cd StellarForge  

python3 -m venv venv  
source venv/bin/activate  

pip install --upgrade pip  
pip install -r requirements.txt  

**CPU-only build**
./build_engine.sh  

**CUDA build**
./build_with_cuda.sh  

Run:
python main.py  
python main.py --engine cpp --backend openmp  
python main.py --engine cpp --backend cuda  

---

### 🪟 Windows Setup

git clone https://github.com/SharonMathew4/StellarForge.git  
cd StellarForge  

python -m venv venv  
venv\Scripts\activate  

pip install --upgrade pip  
pip install -r requirements.txt  

**CPU-only**
build_engine.bat  

**CUDA**
build_with_cuda.bat  

Run:
python main.py  
python main.py --engine cpp --backend openmp  
python main.py --engine cpp --backend cuda  

---

## ▶ Running the Application

python main.py  
python main.py --engine cpp --backend openmp  
python main.py --engine cpp --backend cuda  
python main.py --help  

---

## ⚙ Configuration

Config file: `config/default_settings.json`

- Window size & title
- Particle counts
- Camera & FOV
- Physics timestep
- Procedural generation parameters

---

## 🧠 Architecture

**Engine Bridge Pattern**

Backends:
- `MockEngine` → Pure Python (testing)
- `CppEngine` → C++ with OpenMP / CUDA (production)

Example:
from engine_bridge import CppEngine  
engine = CppEngine(backend='cuda')  
engine.initialize(100000)  
engine.step(0.016)  

---

## 📊 Performance Benchmarks

RTX 4050 Tested Results:

- MockEngine → 1k particles @ 60 FPS
- CppEngine (OpenMP) → 10k @ 60 FPS
- CppEngine (CUDA) → 100k @ 60 FPS
- CppEngine (CUDA) → 1M @ 30 FPS

---

## 🧪 Tech Stack

- UI: PyQt6  
- Rendering: VisPy + OpenGL  
- Physics: C++ / CUDA / OpenMP  
- Bindings: pybind11  
- Build: CMake  
- Storage: HDF5  

---

## 🧩 Dependencies

Python:
- PyQt6
- NumPy
- VisPy
- h5py
- scipy, astropy, noise

C++:
- CMake
- CUDA Toolkit (optional)
- OpenMP

---

## 🐞 Troubleshooting

Black screen → Update GPU drivers & VisPy  
C++ engine load error → python verify_engine.py  
Low performance → Reduce particles / enable CUDA  

---

## 📄 License

MIT License — see LICENSE file.

---

## 📚 References

- Barnes–Hut N-body algorithm  
- cpp_engine/README.md  
- config/default_settings.json  

✨ **StellarForge — Where galaxies are born in code.**
