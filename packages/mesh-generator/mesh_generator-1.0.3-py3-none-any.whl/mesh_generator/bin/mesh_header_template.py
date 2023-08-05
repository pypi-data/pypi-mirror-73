"""
Template to write mesh_header.dat file that will later be used for
MAS MHD code.
"""
import numpy as np
import re
import os


def write_mesh_header(r_mesh=False):
    """ write mesh_header.dat file in bin folder. This formatting is copied from Cooper's IDL code."""
    os.chdir("/bin")
    cor_label = "mesh_header"
    name_of_file = cor_label + ".dat"
    f = open(os.path.join(os.path.dirname(__file__), name_of_file), "w+")
    theta = open(os.path.join(os.path.dirname(__file__), "output02_mesh_t.dat"), "r")
    phi = open(os.path.join(os.path.dirname(__file__), "output02_mesh_p.dat"), "r")
    data_t = theta.readlines()
    data_p = phi.readlines()
    theta.close()
    phi.close()

    if r_mesh:
        r = open(os.path.join(os.path.dirname(__file__), "output02_mesh_r.dat"), 'r')
        data_r = r.readlines()
        r.close()

    f.write("&topology \n")
    f.write(" nprocs=<NPROC_R>, <NPROC_T>, <NPROC_P> \n")
    if r_mesh:
        f.write(" nr=%s\n" % np.int(data_r[5]))
    f.write(" nt=%s\n" % np.int(data_t[5]))
    f.write(" np=%s\n/\n&data\n" % np.int(data_p[5]))
    if r_mesh:
        f.write(" r0=%s\n" % np.float(data_r[7][0:3]))
        f.write(" r1=%s\n" % np.float(data_r[7][5:8]))
        rfrac = str(data_r[9][:len(data_r[9]) - 3])
        rfrac_split = '\n    '.join(line.strip() for line in re.findall(r'.{1,70}(?:\s+|$)', rfrac))
        f.write(" rfrac=      " + str(rfrac_split) + "\n")
        drratio = str(data_r[11][:len(data_r[11]) - 3])
        drratio_split = '\n    '.join(line.strip() for line in re.findall(r'.{1,70}(?:\s+|$)', drratio))
        f.write(" drratio=      " + str(drratio_split) + "\n")
        f.write(" nfrmesh=" + str(data_r[-1]) + "\n")
    tfrac = str(data_t[9][:len(data_t[9]) - 3])
    tfrac_split = '\n    '.join(line.strip() for line in re.findall(r'.{1,70}(?:\s+|$)', tfrac))
    f.write(" tfrac=      " + str(tfrac_split) + "\n")
    dtratio = str(data_t[11][:len(data_t[11]) - 3])
    dtratio_split = '\n    '.join(line.strip() for line in re.findall(r'.{1,70}(?:\s+|$)', dtratio))
    f.write(" dtratio=      " + str(dtratio_split) + "\n")
    f.write(" nftmesh=" + str(data_t[-1]) + "\n")
    pfrac = str(data_p[9][:len(data_p[9]) - 3])
    pfrac_split = '\n    '.join(line.strip() for line in re.findall(r'.{1,70}(?:\s+|$)', pfrac))
    f.write(" pfrac=      " + str(pfrac_split) + "\n")
    dpratio = str(data_p[11][:len(data_p[11]) - 3])
    dpratio_split = '\n    '.join(line.strip() for line in re.findall(r'.{1,70}(?:\s+|$)', dpratio))
    f.write(" dpratio=      " + str(dpratio_split) + "\n")
    f.write(" nfpmesh=" + str(data_p[-1]) + "\n")
    f.write(" phishift=" + str(data_p[-3][1:]))
    f.close()


if __name__ == "__main__":
    write_mesh_header()
