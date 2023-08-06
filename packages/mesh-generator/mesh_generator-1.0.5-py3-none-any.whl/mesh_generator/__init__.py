"""Mesh Generator PSI

Create a 1D Mesh in Python.

Important subpackages:
src- mesh calculations.
bin- output .dat files, optimization, plotting.


Documentation: https://q.predsci.com/docs/mesh_generator/

"""
# import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from mesh_generator import src
from mesh_generator import bin
from mesh_generator.src.mesh import Mesh
from mesh_generator.src.mesh_segment import MeshSegment
from mesh_generator.bin.call_fortran_mesh import create_fortran_mesh