def read_obj(file_path):
    """
    Reads an OBJ file and stores vertices, normals, texture coordinates, and faces in appropriate data structures.

    :param file_path: Path to the .obj file
    :return: A dictionary with keys:
        - 'vertices': List of tuples (x, y, z)
        - 'normals': List of tuples (nx, ny, nz)
        - 'textures': List of tuples (u, v)
        - 'faces': List of faces, each represented as a list of tuples (vertex_idx, texture_idx, normal_idx)
    """
    
    data = {
        'vertices': [],
        'normals': [],
        'textures': [],
        'faces': []
    }

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()

            # Skip comments
            if line.startswith('#'):
                continue

            # Parse vertices
            if line.startswith('v '):
                parts = line.split()
                x, y, z = map(float, parts[1:4])
                data['vertices'].append((x, y, z))

            # Parse texture coordinates
            elif line.startswith('vt '):
                parts = line.split()
                u, v = map(float, parts[1:3])  # Texture coordinates are typically 2D
                data['textures'].append((u, v))

            # Parse normals
            elif line.startswith('vn '):
                parts = line.split()
                nx, ny, nz = map(float, parts[1:4])
                data['normals'].append((nx, ny, nz))

            # Parse faces
            elif line.startswith('f '):
                parts = line.split()
                face = []
                for part in parts[1:]:
                    # Split into vertex/texture/normal indices
                    indices = part.split('/')
                    vertex_idx = int(indices[0]) - 1  # Vertex index
                    texture_idx = int(indices[1]) - 1 if len(indices) > 1 and indices[1] else None  # Texture index
                    normal_idx = int(indices[2]) - 1 if len(indices) > 2 else None  # Normal index
                    face.append((vertex_idx, texture_idx, normal_idx))
                data['faces'].append(face)

    return data


# Load your OBJ file
# file_path = "Obj/obj5.obj"
# obj_data = read_obj(file_path)

# # Show the parsed data
# print("Number of vertices:", len(obj_data['vertices']))
# print("Number of texture coordinates:", len(obj_data['textures']))
# print("Number of normals:", len(obj_data['normals']))
# print("Number of faces:", len(obj_data['faces']))

# Print the first 3 faces
# print("\nFirst 3 faces (with vertex, texture, and normal indices):")
# for i, face in enumerate(obj_data['faces'][:3], start=1):
#     print(f"Face {i}: {face}")
# print(obj_data['vertices'][-1])
# print(obj_data['textures'][-1])
# print(obj_data['normals'][-1])