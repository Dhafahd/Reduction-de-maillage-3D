import numpy as np
from read_obj import read_obj

def create_grid(vertices, grid_size):
    """
    Creates a 3D grid for vertex clustering.
    
    :param vertices: List of (x, y, z) vertex coordinates
    :param grid_size: Size of each grid cell
    :return: Dictionary mapping grid cells to lists of vertex indices
    """
    grid = {}
    for idx, vertex in enumerate(vertices):
        # Calculate grid cell coordinates
        cell = tuple(int(coord // grid_size) for coord in vertex)
        if cell not in grid:
            grid[cell] = []
        grid[cell].append(idx)
    return grid

def compute_representative_vertex(vertices, vertex_indices):
    """
    Computes the representative vertex for a cell by averaging all vertices in it.
    
    :param vertices: List of all vertices
    :param vertex_indices: List of vertex indices in the cell
    :return: (x, y, z) coordinates of representative vertex
    """
    cell_vertices = [vertices[idx] for idx in vertex_indices]
    return tuple(np.mean(cell_vertices, axis=0))

def vertex_clustering(obj_data, grid_size):
    """
    Performs vertex clustering simplification on the mesh.
    
    :param obj_data: Dictionary containing mesh data from read_obj
    :param grid_size: Size of grid cells for clustering
    :return: Dictionary with simplified mesh data
    """
    # Create grid and map vertices to cells
    grid = create_grid(obj_data['vertices'], grid_size)
    
    # Create new vertices and build mapping from old to new indices
    new_vertices = []
    old_to_new_index = {}
    
    for cell, vertex_indices in grid.items():
        new_vertex = compute_representative_vertex(obj_data['vertices'], vertex_indices)
        new_idx = len(new_vertices)
        new_vertices.append(new_vertex)
        
        # Map all vertices in this cell to the new vertex index
        for old_idx in vertex_indices:
            old_to_new_index[old_idx] = new_idx
    
    # Create new faces using the new vertex indices
    new_faces = []
    for face in obj_data['faces']:
        # Map old vertex indices to new ones
        new_face = []
        for vertex_idx, texture_idx, normal_idx in face:
            new_vertex_idx = old_to_new_index[vertex_idx]
            new_face.append((new_vertex_idx, texture_idx, normal_idx))
        
        # Only add face if it's still valid (all vertices are different)
        if len(set(v[0] for v in new_face)) >= 3:
            new_faces.append(new_face)
    
    # Create simplified mesh data
    simplified_data = {
        'vertices': new_vertices,
        'textures': obj_data['textures'],
        'normals': obj_data['normals'],
        'faces': new_faces
    }
    
    return simplified_data

def write_obj(data, output_path):
    """
    Writes mesh data to an OBJ file.
    
    :param data: Dictionary containing mesh data
    :param output_path: Path to output OBJ file
    """
    with open(output_path, 'w') as f:
        # Write vertices
        for v in data['vertices']:
            f.write(f'v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n')
        
        # Write texture coordinates
        for vt in data['textures']:
            f.write(f'vt {vt[0]:.6f} {vt[1]:.6f}\n')
        
        # Write normals
        for vn in data['normals']:
            f.write(f'vn {vn[0]:.6f} {vn[1]:.6f} {vn[2]:.6f}\n')
        
        # Write faces
        for face in data['faces']:
            face_str = 'f'
            for v_idx, vt_idx, vn_idx in face:
                # Add 1 to indices since OBJ format is 1-based
                if vt_idx is not None and vn_idx is not None:
                    face_str += f' {v_idx+1}/{vt_idx+1}/{vn_idx+1}'
                elif vt_idx is not None:
                    face_str += f' {v_idx+1}/{vt_idx+1}'
                else:
                    face_str += f' {v_idx+1}'
            f.write(face_str + '\n')

def main():
    # Example usage
    input_path = 'Obj/obj1.obj'
    output_path = 'simplified.obj'
    grid_size = 0.1  # Adjust this value to control the level of simplification
    
    # Read input mesh
    obj_data = read_obj(input_path)
    
    # Perform vertex clustering
    simplified_data = vertex_clustering(obj_data, grid_size)
    
    # Write simplified mesh
    write_obj(simplified_data, output_path)
    
    # Print statistics
    print(f"Original vertices: {len(obj_data['vertices'])}")
    print(f"Simplified vertices: {len(simplified_data['vertices'])}")
    print(f"Original faces: {len(obj_data['faces'])}")
    print(f"Simplified faces: {len(simplified_data['faces'])}")

if __name__ == '__main__':
    main()