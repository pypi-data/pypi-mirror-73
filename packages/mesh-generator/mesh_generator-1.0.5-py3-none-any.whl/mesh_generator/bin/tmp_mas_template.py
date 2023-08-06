"""Write mesh results in the mesh format for MAS.
Example file phi mesh: (tmp_mas_p.dat)
  np=182
  pfrac=      0.000000E+00, 2.891111E-01, 3.295278E-01, 8.093194E-01
  dpratio=    1.704159E-02, 1.000000E+00, 9.677468E+01, 6.063566E-01
  nfpmesh=5
  phishift= 6.257346E+00

Example file theta mesh: (tmp_mas_t.dat)
  nt=141
  tfrac=      0.000000E+00, 5.043889E-01, 5.606111E-01, 1.000000E+00
  dtratio=    1.826025E-02, 1.000000E+00, 4.525929E+01
  nftmesh=5

Example file radial mesh: (tmp_mas_r.dat)
  r1=10.00
  nr=107
  rfrac=      0.000000E+00, 5.555550E-03, 3.216801E-02, 3.333333E-02, 1.000000E+00
  drratio=    1.000000E+00, 3.359895E+00, 1.000000E+00, 8.819758E+01
  nfrmesh=5

"""
import re


def write_tmp_mas_file(mesh_type: str, tmp_mesh_dir_name: str, tmp_mas_dir_name: str):
    """Write mesh results in the mesh format for MAS."""
    with open(tmp_mesh_dir_name, 'r') as mesh_file:
        mesh_data = mesh_file.readlines()

    if mesh_type == "t":
        with open(tmp_mas_dir_name, "w") as f:
            f.write(" nt=%s\n" % int(mesh_data[5]))
            tfrac = str(mesh_data[9][:len(mesh_data[9]) - 3])
            tfrac_split = '\n    '.join(line.strip() for line in re.findall(r'.{1,70}(?:\s+|$)', tfrac))
            f.write(" tfrac=      " + str(tfrac_split) + "\n")
            dtratio = str(mesh_data[11][:len(mesh_data[11]) - 3])
            dtratio_split = '\n    '.join(line.strip() for line in re.findall(r'.{1,70}(?:\s+|$)', dtratio))
            f.write(" dtratio=      " + str(dtratio_split) + "\n")
            f.write(" nftmesh=" + str(mesh_data[-1]) + "\n")

    if mesh_type == "p":
        with open(tmp_mas_dir_name, "w") as f:
            f.write(" np=%s\n" % int(mesh_data[5]))
            pfrac = str(mesh_data[9][:len(mesh_data[9]) - 3])
            pfrac_split = '\n    '.join(line.strip() for line in re.findall(r'.{1,70}(?:\s+|$)', pfrac))
            f.write(" pfrac=      " + str(pfrac_split) + "\n")
            dpratio = str(mesh_data[11][:len(mesh_data[11]) - 3])
            dpratio_split = '\n    '.join(line.strip() for line in re.findall(r'.{1,70}(?:\s+|$)', dpratio))
            f.write(" dpratio=      " + str(dpratio_split) + "\n")
            f.write(" nfpmesh=" + str(mesh_data[-1]) + "\n")
            f.write(" phishift=" + str(mesh_data[-3][1:]))

    if mesh_type == "r":
        with open(tmp_mas_dir_name, "w") as f:
            f.write(" r1=%s\n" % float(mesh_data[7][5:8]))
            f.write(" nr=%s\n" % int(mesh_data[5]))
            rfrac = str(mesh_data[9][:len(mesh_data[9]) - 3])
            rfrac_split = '\n    '.join(line.strip() for line in re.findall(r'.{1,70}(?:\s+|$)', rfrac))
            f.write(" rfrac=      " + str(rfrac_split) + "\n")
            drratio = str(mesh_data[11][:len(mesh_data[11]) - 3])
            drratio_split = '\n    '.join(line.strip() for line in re.findall(r'.{1,70}(?:\s+|$)', drratio))
            f.write(" drratio=      " + str(drratio_split) + "\n")
            f.write(" nfrmesh=" + str(mesh_data[-1]) + "\n")


if __name__ == "__main__":
    write_tmp_mas_file("r", "tmp_mesh_r.dat", "tmp_mas_r.dat")
    write_tmp_mas_file("t", "tmp_mesh_t.dat", "tmp_mas_t.dat")
    write_tmp_mas_file("p", "tmp_mesh_p.dat", "tmp_mas_p.dat")
