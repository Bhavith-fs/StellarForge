"""
Model loader for 3D assets (GLB/GLTF).
Uses trimesh to load geometry and materials.
"""

import trimesh
import numpy as np
from typing import Tuple, Optional
from core.error_logger import get_error_logger, ErrorSeverity

class ModelLoader:
    """Handles loading of 3D mesh files."""
    
    def __init__(self):
        self.logger = get_error_logger()

    def load_mesh(self, file_path: str) -> Tuple[np.ndarray, np.ndarray, Optional[np.ndarray]]:
        """
        Load a mesh from file.
        
        Args:
            file_path: Path to the .glb or .gltf file
            
        Returns:
            Tuple of (vertices, faces, colors)
            vertices: (N, 3) float array
            faces: (M, 3) int array
            colors: (N, 4) float array (RGBA) or None
            texture: (H, W, 3/4) array or None
            uvs: (N, 2) float array or None
        """
        try:
            # multiple=True ensures we get a scene or list, but for single mesh logic
            # force='mesh' might be better if we want to merge
            scene = trimesh.load(file_path, force='scene')
            
            # Merge all meshes in the scene into one
            if isinstance(scene, trimesh.Scene):
                # Concatenate all geometries
                if len(scene.geometry) == 0:
                    raise ValueError("Scene contains no geometry")
                
                # Dump the scene to a single mesh
                mesh = scene.dump(concatenate=True)
            else:
                mesh = scene

            vertices = np.array(mesh.vertices, dtype=np.float32)
            faces = np.array(mesh.faces, dtype=np.int32)
            
            # Extract colors if available
            colors = None
            if hasattr(mesh.visual, 'vertex_colors'):
                 colors = np.array(mesh.visual.vertex_colors, dtype=np.float32) / 255.0
            
            # Extract Texture and UVs
            texture = None
            uvs = None
            
            # Check if mesh has texture material
            if hasattr(mesh.visual, 'material') and hasattr(mesh.visual.material, 'image'):
                import PIL.Image
                img = mesh.visual.material.image
                # Convert to RGBA array
                if img:
                     # Handle different image formats (some might be bytes)
                    if not isinstance(img, PIL.Image.Image):
                        # Try to load if it's bytes or other format
                        try:
                            img = PIL.Image.open(img)
                        except:
                            pass
                            
                    if isinstance(img, PIL.Image.Image):
                        texture = np.array(img)
            
            # Extract UV coordinates (texture coordinates)
            if hasattr(mesh.visual, 'uv'):
                 # Ensure UVs separate from vertices count match (sometimes trimesh handles this)
                 uvs = np.array(mesh.visual.uv, dtype=np.float32)

            self.logger.log_error(
                f"Loaded mesh {file_path}: {len(vertices)} vertices, Texture: {texture is not None}",
                component="MODEL_LOADER",
                severity=ErrorSeverity.INFO
            )
            
            return vertices, faces, colors, texture, uvs

        except Exception as e:
            self.logger.log_exception(
                e,
                component="MODEL_LOADER",
                severity=ErrorSeverity.ERROR,
                context={'file': file_path}
            )
            # Return empty arrays on failure to prevent crash
            return (np.zeros((0, 3), dtype=np.float32), 
                    np.zeros((0, 3), dtype=np.int32), 
                    None)
