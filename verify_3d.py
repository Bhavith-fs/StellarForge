
import sys
import os
import numpy as np
from PyQt6.QtWidgets import QApplication
from vispy import scene
from src.vis.universe_renderer import UniverseRenderer

def verify_3d_loading():
    print("Initializing Application...")
    app = QApplication(sys.argv)
    canvas = scene.SceneCanvas(keys='interactive', show=True)
    
    print("Initializing Renderer...")
    renderer = UniverseRenderer(canvas)
    
    mesh_path = os.path.abspath("src/assets/voyager.glb")
    print(f"Loading mesh from: {mesh_path}")
    
    if not os.path.exists(mesh_path):
        print("ERROR: Mesh file not found!")
        return
        
    try:
        renderer.add_mesh(mesh_path, scale=0.1)
        print("SUCCESS: Mesh added to scene.")
        
        # Verify mesh visual exists
        if len(renderer.meshes) == 1:
            print("Verified: Mesh visual is present in renderer.")
            v = renderer.meshes[0]
            print(f"Mesh stats: {len(v.mesh_data.get_vertices())} vertices")
        else:
            print("ERROR: No mesh found in renderer list.")
            
    except Exception as e:
        print(f"FAILED to load mesh: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Add src to path
    sys.path.append(os.path.abspath("src"))
    verify_3d_loading()
