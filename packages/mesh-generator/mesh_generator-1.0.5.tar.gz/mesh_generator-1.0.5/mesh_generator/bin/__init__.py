"""

Usage:
1. Call psi_tools fortran mesh to produce .dat output files with mesh points.
2. Optimize legacy total number of mesh points.
3. plot solution.

For more details: https://q.predsci.com/docs/mesh_generator/

Important modules:
call_fortran_mesh.py
plot_mesh_res.py
"""

from mesh_generator.bin.call_fortran_mesh import create_fortran_mesh
from mesh_generator.bin.mesh_header_template import write_mesh_header
from mesh_generator.bin.shell_command import run_shell_command