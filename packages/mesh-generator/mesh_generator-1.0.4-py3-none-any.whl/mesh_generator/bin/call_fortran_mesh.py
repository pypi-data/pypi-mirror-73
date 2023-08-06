"""calling psi_tools "mesh"

Step 4 of creating a 1D mesh:
    *create output files and call fortran "mesh" tool to create a file with mesh points.
    *check if mesh is valid and adjust the legacy mesh total number of points.
    *plot mesh results.
"""
from mesh_generator.bin.plot_mesh_res import plot_mesh_res
from mesh_generator.bin.output_dat_template import write_output_file
from mesh_generator.bin.check_mesh_valid import check_mesh_valid
from mesh_generator.bin.call_mesh_shell_command import call_shell_command
import os


def create_fortran_mesh(adjusted_mesh: dict, legacy_mesh: dict, mesh_type: str, dir_name: str, output_file_name=None,
                        mesh_res_file_name=None, save_plot=False, show_plot=False, save_plot_path=None,
                        plot_file_name=None):
    """
    Create output files and call fortran "mesh" code to create a txt file with mesh points and respective resolution,
    and cell-to-cell ratio.
    :param plot_file_name: file name to save plot.
    :param dir_name: path to output file.
    :param mesh_res_file_name: name of file with mesh points. (t,dt, ratio) essential for plotting.
    :param output_file_name: name of file with mesh results. ex: output02_mesh_t.dat
    :param adjusted_mesh: adjusted mesh dictionary (step 2)
    :param save_plot_path: path where to save plot.
    :param save_plot: save plot as png.
    :param show_plot: bool. show matplotlib plot in interactive window.
    :param mesh_type: 't'/'p'/'r', used for plot title.
    :param legacy_mesh: legacy mesh dictionary (step 3)
    """

    # mesh output files full path
    output_path = os.path.join(dir_name, output_file_name)
    mesh_res_path = os.path.join(dir_name, mesh_res_file_name)

    # "write_output_file"
    # this function creates a file with the results of the legacy mesh so the fortran mesh will be able to read it.
    # (0 filtering)
    total_legacy_num = write_output_file(legacy_mesh, 0, mesh_type, output_path)

    # call fortran tool "mesh" and write a mesh_res file with all the mesh points, respective resolution and ratio from
    # cell to cell.
    call_shell_command(output_path, mesh_res_path)

    # - "check_mesh_valid" : Check if tmp_mesh_r.dat is below user requests. Optimizes the total number of points.
    check_mesh_valid(adjusted_mesh, total_legacy_num, output_path, mesh_res_path)

    if save_plot or show_plot:
        # "plot_mesh_res": this function will plot the data in mesh_res.txt
        plot_mesh_res(adjusted_mesh=adjusted_mesh, save_plot=save_plot, show_plot=show_plot,
                      mesh_res_file_name=mesh_res_path, label=mesh_type, save_plot_path=save_plot_path,
                      plot_file_name=plot_file_name)


if __name__ == "__main__":
    from tests.ar_test import *

    WorkDir = os.getcwd()
    PlotDir = "../../plots/"

    create_fortran_mesh(adjust__mesh_phi_1().json_dict(), legacy__mesh_phi_1().json_dict(), 'p', WorkDir,
                        output_file_name="tmp_mesh_p.dat", mesh_res_file_name="mesh_res_p.txt",
                        save_plot=True, show_plot=True, save_plot_path=PlotDir, plot_file_name="phi_1_mesh.png")
    #
    # create_fortran_mesh(adjust__mesh_theta_1().json_dict(), legacy__mesh_theta_1().json_dict(), 't', WorkDir,
    #                     output_file_name="tmp_mesh_t.dat", mesh_res_file_name="mesh_res_t.txt",
    #                     save_plot=True, show_plot=True, save_plot_path=PlotDir, plot_file_name="theta_1_mesh.png")
    #
    # create_fortran_mesh(adjust__mesh_r_1().json_dict(), legacy__mesh_r_1().json_dict(), 'r', WorkDir,
    #                     output_file_name="tmp_mesh_r.dat", mesh_res_file_name="mesh_res_r.txt",
    #                     save_plot=True, show_plot=True, save_plot_path=PlotDir, plot_file_name="radial_1_mesh.png")

