import pyvista as pv
from read_obj import read_obj

def visualize_two_objs(file_path1, file_path2):
    """
    Visualize two 3D OBJ files side-by-side using PyVista.
    Shows the original and adjusted models for comparison.
    
    :param file_path1: Path to the first OBJ file (original).
    :param file_path2: Path to the second OBJ file (adjusted).
    """
    # Parse the OBJ files
    obj_data1 = read_obj(file_path1)
    obj_data2 = read_obj(file_path2)

    # Create PyVista meshes
    vertices1 = obj_data1['vertices']
    faces1 = []
    for face in obj_data1['faces']:
        face_vertices = [vertex[0] for vertex in face]  # Extract vertex indices
        faces1.append(len(face_vertices))  # Number of vertices in this face
        faces1.extend(face_vertices)      # Add vertex indices
    faces1 = pv.convert_array(faces1)
    mesh1 = pv.PolyData(vertices1, faces1)

    vertices2 = obj_data2['vertices']
    faces2 = []
    for face in obj_data2['faces']:
        face_vertices = [vertex[0] for vertex in face]  # Extract vertex indices
        faces2.append(len(face_vertices))  # Number of vertices in this face
        faces2.extend(face_vertices)      # Add vertex indices
    faces2 = pv.convert_array(faces2)
    mesh2 = pv.PolyData(vertices2, faces2)

    # Create a PyVista plotter
    plotter = pv.Plotter(shape=(1, 2))  # One row, two columns layout

    # First view: Original model
    plotter.subplot(0, 0)  # Left plot
    plotter.add_mesh(mesh1, color="white", show_edges=True)
    plotter.add_text("Original Model", font_size=12, color="black")
    plotter.set_background("black")

    # Second view: Adjusted model
    plotter.subplot(0, 1)  # Right plot
    plotter.add_mesh(mesh2, color="lightblue", show_edges=True)
    plotter.add_text("Simplified Model", font_size=12, color="black")
    plotter.set_background("white")

    # Show the plot
    plotter.show()

if __name__ == "__main__":
    # Hardcode the paths to your OBJ files
    obj_file1 = "Obj/obj3.obj"  # Replace with the path to the first OBJ file
    obj_file2 = "result1.obj"  # Replace with the path to the second OBJ file

    visualize_two_objs(obj_file1, obj_file2)
