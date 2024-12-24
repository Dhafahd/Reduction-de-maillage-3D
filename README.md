# Mesh Simplification Toolkit

This repository provides a Python-based toolkit for simplifying 3D meshes, focusing on two primary algorithms: **edge collapse** and **vertex clustering**. These methods allow for efficient reduction of mesh complexity while preserving overall geometric structure.

## Features

- **Edge Collapse**:
  - Simplifies a mesh by iteratively collapsing edges with minimal cost.
  - Customizable reduction ratio for controlling the level of simplification.
  - Supports exporting the simplified mesh to an OBJ file.

- **Vertex Clustering**:
  - Groups vertices into a grid structure and computes representative vertices.
  - Adjustable grid size to control the level of simplification.
  - Ensures valid geometry by retaining unique vertices in each cluster.

- **OBJ File Support**:
  - Parses and writes standard `.obj` files with vertices, normals, textures, and faces.

## Files Overview

- **`read_obj.py`**:
  - Provides a utility for parsing `.obj` files.
  - Extracts vertices, normals, textures, and face data into a structured dictionary.

- **`edge_collapse.py`**:
  - Implements the edge collapse algorithm.
  - Prioritizes edge collapses based on computed cost.
  - Includes functions for reading and writing OBJ files.

- **`vertex_clustering.py`**:
  - Implements the vertex clustering algorithm.
  - Groups vertices into a 3D grid and averages their positions.
  - Exports the simplified mesh to an OBJ file.

