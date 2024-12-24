import pyvista as pv
from read_obj import read_obj
from vertex_clustering import vertex_clustering, write_obj
import numpy as np

def obj_data_to_pyvista(obj_data):
    """
    Convert OBJ data to PyVista format with correctly structured faces.
    """
    # Convert vertices to numpy array
    vertices = np.array(obj_data['vertices'])

    # Convert faces to PyVista-compatible format
    faces = []
    for face in obj_data['faces']:
        # Each face starts with the number of vertices (always 3 for triangles here)
        face_indices = [len(face)] + [v[0] for v in face]  # Extract vertex indices
        faces.extend(face_indices)

    # Convert faces to numpy array
    faces = np.array(faces, dtype=np.int32)

    # Create PyVista mesh
    return pv.PolyData(vertices, faces)

# Testing the conversion with the given OBJ data
# Testing the conversion with the given OBJ data
try:
    mesh = obj_data_to_pyvista("original_file")
    valid_conversion = True
except Exception as e:
    valid_conversion = False
    conversion_error = str(e)

valid_conversion, conversion_error if not valid_conversion else "Conversion successful"

def visualize_models(original_path, simplified_path=None, grid_size=0.1, save_simplified=True):
    """
    Visualize original and simplified meshes side by side
    
    :param original_path: Path to original OBJ file
    :param simplified_path: Path to simplified OBJ file (optional)
    :param grid_size: Grid size for simplification if simplified_path is not provided
    :param save_simplified: Whether to save the simplified model if generated
    """
    # Create plotter
    plotter = pv.Plotter(shape=(1, 2))
    
    # Load and display original model
    original_data = read_obj(original_path)
    original_mesh = obj_data_to_pyvista(original_data)
    plotter.subplot(0, 0)
    plotter.add_mesh(original_mesh, show_edges=True, color='white')
    plotter.add_text(f"Original\nVertices: {len(original_data['vertices'])}\nFaces: {len(original_data['faces'])}")
    
    # Load or create simplified model
    if simplified_path and not save_simplified:
        # Load existing simplified model
        simplified_data = read_obj(simplified_path)
    else:
        # Create new simplified model
        simplified_data = vertex_clustering(original_data, grid_size)
        if save_simplified:
            # Generate output path if not provided
            output_path = simplified_path or original_path.replace('.obj', '_simplified.obj')
            write_obj(simplified_data, output_path)
            print(f"Simplified model saved to: {output_path}")
        
    # Display simplified model
    simplified_mesh = obj_data_to_pyvista(simplified_data)
    plotter.subplot(0, 1)
    plotter.add_mesh(simplified_mesh, show_edges=True, color='lightblue')
    plotter.add_text(f"Simplified\nVertices: {len(simplified_data['vertices'])}\nFaces: {len(simplified_data['faces'])}")
    
    # Link cameras for synchronized rotation/zoom
    plotter.link_views()
    
    # Show reduction statistics
    vertex_reduction = (1 - len(simplified_data['vertices']) / len(original_data['vertices'])) * 100
    face_reduction = (1 - len(simplified_data['faces']) / len(original_data['faces'])) * 100
    print(f"\nReduction Statistics:")
    print(f"Vertices: {len(original_data['vertices'])} → {len(simplified_data['vertices'])} ({vertex_reduction:.1f}% reduction)")
    print(f"Faces: {len(original_data['faces'])} → {len(simplified_data['faces'])} ({face_reduction:.1f}% reduction)")
    
    # Show the comparison
    plotter.show()

if __name__ == '__main__':
    # Example usage
    original_file = "Obj/obj3.obj"  # Replace with your original file path
    grid_size = 0.1 # Adjust this value to control simplification level
    
    # Option 1: Generate and save simplified model while visualizing
    visualize_models(
        original_file,
        simplified_path="simplified.obj",  # Specify output path
        grid_size=grid_size,
        save_simplified=True
    )
    
    # Option 2: Just visualize without saving
    # visualize_models(original_file, grid_size=grid_size, save_simplified=False)
    
    # Option 3: Load and visualize existing simplified model
    # visualize_models(original_file, "existing_simplified.obj", save_simplified=False)
    
