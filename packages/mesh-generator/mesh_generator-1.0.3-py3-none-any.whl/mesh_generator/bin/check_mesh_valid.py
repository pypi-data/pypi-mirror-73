"""Mesh Optimization tool

adding or subtracting points from legacy mesh total number of points which will move the mesh up or down.
This is done iteratively.

- Checks if the mesh exceeds the user constant mesh segment requirements - if so, it will add points to the mesh to
lower its ds. It will do so by editing the file "output02_mesh_t.dat" and rerunning the fortran code to get a
new mesh_res.txt.
"""

from mesh_generator.bin.shell_command import run_shell_command
import os


def check_seg(mesh_adj: dict):
    """
    This test will check if the mesh is below all constant mesh segments that the user specified.
    It will save all the mesh segments with ds=1 (constant segements) and will read mesh_res.txt to see if points are
    below segment requirements.
    Iteratively.
    :param mesh_adj: dictionary of adjusted mesh segments.
    :return: bool True/False
    """
    epsilon = 10. ** (-10.)
    exceed_seg = False

    new_constant_list = []  # a list with all constant segments
    phi_shift = mesh_adj['phi_shift']
    for segments in mesh_adj['segment_list']:
        if segments['ratio'] == 1.:
            new_constant_list.append(segments)

    idx = 0
    with open("mesh_res.txt", "r") as f:
        while idx < len(new_constant_list):
            s0 = (new_constant_list[idx]['s0']) + phi_shift
            s1 = (new_constant_list[idx]['s1']) + phi_shift
            ds = (new_constant_list[idx]['ds0'])
            for i, line in enumerate(f):
                if idx == 0 and i == 0:  # very first line of the mesh_res.txt skip.
                    i += 1
                else:
                    x = float(line.split()[1:2][0])  # s
                    y = float(line.split()[2:3][0])  # ds
                    if s0 < x < s1:
                        if y > ds + epsilon:
                            # mesh is above user requests! -> break then call add_num.
                            exceed_seg = True
                            return exceed_seg
                    if x > s1:
                        # break -> move to the next constant mesh segment.
                        break
            idx += 1
    return exceed_seg


def check_ratio(adj_mesh: dict):
    """
    Check if the the new legacy mesh exceeds 100.5% of BG_RATIO
    :param adj_mesh: dictionary with adjusted mesh results.
    :return: bool True/False
    """
    percent = 0.005
    exceed_ratio = False
    ratio_max = adj_mesh['BG_RATIO'] * (1 + percent)
    ratio_min = (1. / adj_mesh['BG_RATIO']) * (1 - percent)
    with open("mesh_res.txt", "r") as f:
        for idx, line in enumerate(f):
            if idx >= 1:
                for word in line.split()[3:4]:
                    if float(word) > ratio_max:
                        exceed_ratio = True
                        print("CURRENT RATIO " + str(word) + " > " + str(ratio_max) + " BG_RATIO")
                        return exceed_ratio
                    if float(word) < ratio_min:
                        exceed_ratio = True
                        print("CURRENT RATIO " + str(word) + " < " + str(ratio_min) + " 1/BG_RATIO")
                        return exceed_ratio
    return exceed_ratio


def adjust_txt_file(name_of_file: str, replace_num: int):
    """
    :param replace_num: adjusted number of points in legacy mesh
    :param name_of_file: for example, output02_mesh_t.dat
    :return: a modified output02_mesh_t.dat with num_of_points -1 / +1
    """

    with open(name_of_file, 'r') as f:
        file_data = f.readlines()

    # Replace the total number of points line #5 in mesh_res.txt
    file_data[5] = str(replace_num) + '\n'

    # # Write the file out again
    with open(name_of_file, 'w') as f:
        f.writelines(file_data)


def reduce_num(mesh_type: str, adj_mesh: dict, total_num: int):
    """
    Iteratively find the optimized number of points for mesh by reducing the total number of points (-1).
    :param total_num: total number of points in legacy mesh.
    :param mesh_type: p or t or r
    :param adj_mesh: dictionary with adjusted mesh segments.
    :return: now the mesh_res.txt is optimal.
    """
    print("Initial total number of points:", total_num)
    name_of_file = "output02_mesh_" + mesh_type + ".dat"
    command = "mesh output02_mesh_" + mesh_type + ".dat -o mesh_res.txt"
    idx = 0

    if check_ratio(adj_mesh) is False:
        while idx <= int(total_num):
            total_num += - 1
            adjust_txt_file(name_of_file, total_num)  # modify output02_mesh_t.dat
            run_shell_command(command, os.getcwd(), debug=True)  # recalculate mesh_res.txt

            if check_seg(adj_mesh) is False and \
                    check_ratio(adj_mesh) is False:
                idx += 1
            else:
                print("Final num_of_points is", total_num + 1)
                adjust_txt_file(name_of_file, (total_num + 1))
                break
    else:
        print("Final num_of_points is ", total_num)


def add_num(mesh_type: str, adj_mesh: dict, total_num: int):
    """
    Mesh is exceeding the user requests more points are needed (+1).
    :param total_num: total number of points in legacy mesh.
    :param mesh_type: p or t or r
    :param adj_mesh: dictionary of adjusted mesh segments.
    """
    print("Initial total number of points:", total_num)

    name_of_file = "output02_mesh_" + mesh_type + ".dat"
    command = "mesh output02_mesh_" + mesh_type + ".dat -o mesh_res.txt"
    total_num = total_num + 1
    adjust_txt_file(name_of_file, total_num)  # modify output02_mesh_t.dat (+1 total number of points).
    run_shell_command(command, os.getcwd(), debug=True)  # recalculate mesh_res.txt
    idx = 0

    while idx <= int(total_num):
        if check_seg(adj_mesh) is True:
            total_num += 1
            adjust_txt_file(name_of_file, total_num)  # modify output02_mesh_t.dat
            run_shell_command(command, os.getcwd(), debug=True)
            idx += 1
        else:
            print("Final num_of_points is", total_num)
            break


def apply_filter(mesh_type, NUM_OF_FILTER):
    """ Function to adjust the output.dat last line to be 5. """
    with open("output02_mesh_" + str(mesh_type) + ".dat", "r") as file:
        # Read a list of lines into data
        data = file.readlines()

    # Now change the last line.
    data[-1] = str(NUM_OF_FILTER)

    # Write everything back
    with open("output02_mesh_" + str(mesh_type) + ".dat", 'w') as file2:
        file2.writelines(data)


def check_mesh_valid(mesh_type: str, adj_mesh: dict, total_legacy_num: int):
    if check_seg(adj_mesh):
        print("Original mesh is above user requests, calling add_num.")  # needs to add points to lower the mesh (+1).
        add_num(mesh_type, adj_mesh, total_legacy_num)
    else:  # need to optimize your mesh by deleting points (-1).
        print("Original mesh is below user requests, calling reduce_num to optimize mesh results.")
        reduce_num(mesh_type, adj_mesh, total_legacy_num)

    print("Mesh is valid. Applying filter = 5 to smooth mesh.")
    apply_filter(mesh_type, 5)
    command = "mesh output02_mesh_" + mesh_type + ".dat -o mesh_res.txt"
    run_shell_command(command, os.getcwd(), debug=True)
