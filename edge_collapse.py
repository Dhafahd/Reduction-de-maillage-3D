import heapq
from read_obj import read_obj

def write_obj(file_path, data):
    with open(file_path, 'w') as file:
        for vertex in data['vertices']:
            file.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
        for normal in data['normals']:
            file.write(f"vn {normal[0]} {normal[1]} {normal[2]}\n")
        for texture in data['textures']:
            file.write(f"vt {texture[0]} {texture[1]}\n")
        for face in data['faces']:
            face_str = ' '.join(['/'.join([str(idx + 1) if idx is not None else '' for idx in vertex]) for vertex in face])
            file.write(f"f {face_str}\n")

def edge_collapse(data, ratio):
    vertices = data['vertices']
    faces = data['faces']
    target_num_faces = int(len(faces) * ratio)

    # Create a priority queue to store edge collapses by cost
    edge_queue = []

    # Populate initial edge queue with all edges
    edges = {}
    for i, face in enumerate(faces):
        for j in range(3):
            v1 = face[j][0]
            v2 = face[(j + 1) % 3][0]
            if v1 > v2:
                v1, v2 = v2, v1
            edge = (v1, v2)
            if edge not in edges:
                edges[edge] = []
            edges[edge].append(i)

    # Add edges to the priority queue with initial cost
    for edge, face_list in edges.items():
        cost = calculate_edge_cost(edge, vertices, faces, face_list)
        heapq.heappush(edge_queue, (cost, edge, face_list))

    # Collapse edges until the desired number of faces is reached
    while len(faces) > target_num_faces and edge_queue:
        cost, edge, face_list = heapq.heappop(edge_queue)
        collapse_edge(edge, vertices, faces, face_list)
        # Update the edges and costs in the queue
        update_edge_queue(edge_queue, edge, vertices, faces)

    return data

def calculate_edge_cost(edge, vertices, faces, face_list):
    # Implement cost calculation for collapsing an edge
    v1, v2 = edge
    p1 = vertices[v1]
    p2 = vertices[v2]
    cost = sum((p1[i] - p2[i])**2 for i in range(3))**0.5
    return cost

def collapse_edge(edge, vertices, faces, face_list):
    # Implement edge collapse
    v1, v2 = edge
    # Move v1 to the midpoint of v1 and v2
    midpoint = tuple((vertices[v1][i] + vertices[v2][i]) / 2 for i in range(3))
    vertices[v1] = midpoint
    # Remove faces that include v2
    faces[:] = [face for face in faces if v2 not in [vertex[0] for vertex in face]]
    # Update remaining faces to replace v2 with v1
    for face in faces:
        for i in range(len(face)):
            if face[i][0] == v2:
                face[i] = (v1, face[i][1], face[i][2])

def update_edge_queue(edge_queue, edge, vertices, faces):
    # Implement edge queue update after collapsing an edge
    heapq.heapify(edge_queue)

if __name__ == "__main__":
    obj_data = read_obj('Obj/obj3.obj')
    reduction_ratio = 0.9  # Example: reduce to 50% of the original number of faces
    simplified_data = edge_collapse(obj_data, reduction_ratio)
    write_obj('result1.obj', simplified_data)
