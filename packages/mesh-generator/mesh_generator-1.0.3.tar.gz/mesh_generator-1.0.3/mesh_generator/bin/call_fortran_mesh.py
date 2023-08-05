"""calling psi_tools "mesh"

Step 4 of creating a 1D mesh:
    *create output files and call fortran Mesh code to create mesh_res.txt.
    *check if mesh is valid and adjust the legacy mesh total number of points.
    *plot mesh_res.txt results.
"""
from mesh_generator.bin.shell_command import run_shell_command
from mesh_generator.bin.plot_mesh_res import plot_mesh_res
from mesh_generator.bin.output_dat_template import write_output_file
from mesh_generator.bin.check_mesh_valid import check_mesh_valid
import os


def create_fortran_mesh(adjusted_mesh: dict, legacy_mesh: dict, mesh_type: str, show_plot: bool, save_plot=False):
    """
    Create output files and call fortran Mesh code to create mesh_res.txt.
    """
    os.chdir(os.path.dirname(__file__))  # change current directory to be ../mesh_generator/bin/

    """
    - "write_output_file"
    this function creates a file called output02_mesh_t.dat
    with the results of the legacy mesh so the fortran mesh will be able to read it.
    (0 filtering)
    """
    total_legacy_num = write_output_file(legacy_mesh, 0, mesh_type)

    call_shell_command(mesh_type)

    """
    - "check_mesh_valid"
    Check if mesh_res.txt is below user requests. Optimizes the total number of points. 
    """
    check_mesh_valid(mesh_type, adjusted_mesh, total_legacy_num)

    if save_plot or show_plot:
        """
        - "plot_mesh_res"
        this function will plot the data in mesh_res.txt
        """
        plot_mesh_res(adjusted_mesh=adjusted_mesh, save_plot=save_plot, show_plot=show_plot, label=mesh_type)


def call_shell_command(mesh_type):
    """
    - "run_shell_command"
    call the fortran mesh and create a txt file called mesh_res.txt with the resulting mesh points
    """
    command = "mesh output02_mesh_" + mesh_type + ".dat -o mesh_res.txt"
    run_shell_command(command, os.getcwd(), debug=True)


if __name__ == "__main__":
    from tests.ar_test import *
    #
    # print("adjusted mesh", adjust__mesh_theta_1())
    # print("legacy mesh", legacy__mesh_theta_1())
    # create_fortran_mesh(adjust__mesh_phi_1().json_dict(), legacy__mesh_phi_1().json_dict(), 'p', True)
    # create_fortran_mesh(adjust__mesh_phi_2().json_dict(), legacy__mesh_phi_2().json_dict(), 'p', True)
    # create_fortran_mesh(adjust__mesh_phi_3().json_dict(), legacy__mesh_phi_3().json_dict(), 'p', True)
    # create_fortran_mesh(adjust__mesh_phi_4().json_dict(), legacy__mesh_phi_4().json_dict(), 'p', True)
    # create_fortran_mesh(adjust__mesh_phi_5().json_dict(), legacy__mesh_phi_5().json_dict(), 'p', True)
    # create_fortran_mesh(adjust__mesh_phi_6().json_dict(), legacy__mesh_phi_6().json_dict(), 'p', True)
    # create_fortran_mesh(adjust__mesh_phi_7().json_dict(), legacy__mesh_phi_7().json_dict(), 'p', True)
    # create_fortran_mesh(adjust__mesh_phi_8().json_dict(), legacy__mesh_phi_8().json_dict(), 'p', True)
    # create_fortran_mesh(adjust__mesh_phi_9().json_dict(), legacy__mesh_phi_9().json_dict(), 'p', True)
    # create_fortran_mesh(adjust__mesh_phi_10().json_dict(), legacy__mesh_phi_10().json_dict(), 'p', True)
    # create_fortran_mesh(adjust__mesh_phi_11().json_dict(), legacy__mesh_phi_11().json_dict(), 'p', True)
    # create_fortran_mesh(adjust__mesh_phi_12().json_dict(), legacy__mesh_phi_12().json_dict(), 'p', True)
    # create_fortran_mesh(adjust__mesh_phi_13().json_dict(), legacy__mesh_phi_13().json_dict(), 'p', True)
    # create_fortran_mesh(adjust__mesh_phi_14().json_dict(), legacy__mesh_phi_14().json_dict(), 'p', True)
    # create_fortran_mesh(adjust__mesh_phi_15().json_dict(), legacy__mesh_phi_15().json_dict(), 'p', True)
    # create_fortran_mesh(adjust__mesh_phi_16().json_dict(), legacy__mesh_phi_16().json_dict(), 'p', True)
    # create_fortran_mesh(adjust__mesh_phi_17().json_dict(), legacy__mesh_phi_17().json_dict(), 'p', True)
    # create_fortran_mesh(adjust__mesh_phi_18().json_dict(), legacy__mesh_phi_18().json_dict(), 'p', True)
    # create_fortran_mesh(adjust__mesh_phi_19().json_dict(), legacy__mesh_phi_19().json_dict(), 'p', True)
    # create_fortran_mesh(adjust__mesh_phi_20().json_dict(), legacy__mesh_phi_20().json_dict(), 'p', True)
    # create_fortran_mesh(adjust__mesh_phi_21().json_dict(), legacy__mesh_phi_21().json_dict(), 'p', True)
    # create_fortran_mesh(adjust__mesh_phi_22().json_dict(), legacy__mesh_phi_22().json_dict(), 'p', True)
    # create_fortran_mesh(adjust__mesh_phi_23().json_dict(), legacy__mesh_phi_23().json_dict(), 'p', True)
    # create_fortran_mesh(adjust__mesh_phi_24().json_dict(), legacy__mesh_phi_24().json_dict(), 'p', True)
    # create_fortran_mesh(adjust__mesh_phi_25().json_dict(), legacy__mesh_phi_25().json_dict(), 'p', True)
    # create_fortran_mesh(adjust__mesh_phi_26().json_dict(), legacy__mesh_phi_26().json_dict(), 'p', True)
    # create_fortran_mesh(adjust__mesh_phi_27().json_dict(), legacy__mesh_phi_27().json_dict(), 'p', True)
    # create_fortran_mesh(adjust__mesh_phi_28().json_dict(), legacy__mesh_phi_28().json_dict(), 'p', True)
    # create_fortran_mesh(adjust__mesh_phi_29().json_dict(), legacy__mesh_phi_29().json_dict(), 'p', True)

    create_fortran_mesh(adjust__mesh_theta_1().json_dict(), legacy__mesh_theta_1().json_dict(), 't', True)
    # create_fortran_mesh(adjust__mesh_theta_2().json_dict(), legacy__mesh_theta_2().json_dict(), 't', True)
    # create_fortran_mesh(adjust__mesh_theta_3().json_dict(), legacy__mesh_theta_3().json_dict(), 't', True)
    # create_fortran_mesh(adjust__mesh_theta_4().json_dict(), legacy__mesh_theta_4().json_dict(), 't', True)
    # create_fortran_mesh(adjust__mesh_theta_5().json_dict(), legacy__mesh_theta_5().json_dict(), 't', True)
    # create_fortran_mesh(adjust__mesh_theta_6().json_dict(), legacy__mesh_theta_6().json_dict(), 't', True)
    # create_fortran_mesh(adjust__mesh_theta_7().json_dict(), legacy__mesh_theta_7().json_dict(), 't', True)
    # create_fortran_mesh(adjust__mesh_theta_8().json_dict(), legacy__mesh_theta_8().json_dict(), 't', True)
    # create_fortran_mesh(adjust__mesh_theta_9().json_dict(), legacy__mesh_theta_9().json_dict(), 't', True)
    # create_fortran_mesh(adjust__mesh_theta_10().json_dict(), legacy__mesh_theta_10().json_dict(), 't', True)
    # create_fortran_mesh(adjust__mesh_theta_11().json_dict(), legacy__mesh_theta_11().json_dict(), 't', True)
    # create_fortran_mesh(adjust__mesh_theta_12().json_dict(), legacy__mesh_theta_12().json_dict(), 't', True)
    # create_fortran_mesh(adjust__mesh_theta_13().json_dict(), legacy__mesh_theta_13().json_dict(), 't', True)
    # create_fortran_mesh(adjust__mesh_theta_14().json_dict(), legacy__mesh_theta_14().json_dict(), 't', True)
    # create_fortran_mesh(adjust__mesh_theta_15().json_dict(), legacy__mesh_theta_15().json_dict(), 't', True)
    # create_fortran_mesh(adjust__mesh_theta_16().json_dict(), legacy__mesh_theta_16().json_dict(), 't', True)

    # create_fortran_mesh(adjust__mesh_r_1().json_dict(), legacy__mesh_r_1().json_dict(), 'r', True)
    # create_fortran_mesh(adjust__mesh_r_2().json_dict(), legacy__mesh_r_2().json_dict(), 'r', True)
    # create_fortran_mesh(adjust__mesh_r_3().json_dict(), legacy__mesh_r_3().json_dict(), 'r', True)
    # create_fortran_mesh(adjust__mesh_r_4().json_dict(), legacy__mesh_r_4().json_dict(), 'r', True)
