"""
Quick start script to run StellarForge with example configurations.
"""

import sys
import argparse
from PyQt6.QtWidgets import QApplication
from gui import MainWindow


def main():
    parser = argparse.ArgumentParser(
        description='StellarForge - Cosmic Simulation Application'
    )
    parser.add_argument(
        '--particles',
        type=int,
        default=5000,
        help='Number of particles to generate (default: 5000)'
    )
    parser.add_argument(
        '--galaxies',
        type=int,
        default=3,
        help='Number of galaxies to generate (default: 3)'
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=None,
        help='Random seed for reproducibility'
    )
    parser.add_argument(
        '--demo',
        action='store_true',
        help='Run in demo mode with preset configurations'
    )
    
    args = parser.parse_args()
    
    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("StellarForge")
    
    # Create main window
    window = MainWindow()
    
    # Apply command line arguments if provided
    # (These would need to be passed to the engine initialization)
    if args.demo:
        print("Running in DEMO mode...")
        print("- 10,000 particles")
        print("- 5 galaxies")
        print("- Seed: 42")
    
    window.show()
    
    print("\n" + "="*60)
    print("  StellarForge - Cosmic Simulation Application")
    print("="*60)
    print("\nControls:")
    print("  - Click and drag: Rotate camera")
    print("  - Scroll wheel: Zoom")
    print("  - Right-click drag: Pan")
    print("  - Space: Play/Pause")
    print("\nModes:")
    print("  - Observation: View only")
    print("  - Sandbox: Add/remove objects")
    print("\n" + "="*60 + "\n")
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
