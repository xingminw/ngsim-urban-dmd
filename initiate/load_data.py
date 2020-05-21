import glob
from classes.trajectory import Trajectory


def load_data(data_folder):
    file_name_list = glob.glob(data_folder + "/*.txt")

    with open(file_name_list[0], "r") as temp_file:
        all_lines = temp_file.readlines()

    trajectory_dict = {}

    for single_line in all_lines[:]:
        split_info = single_line.split(" ")
        useful_info = []
        for info in split_info:
            if info is not "":
                useful_info.append(info)

        vehicle_id = str(useful_info[0])
        time_slot = 0.1 * int(useful_info[1])
        epoch_time = int(useful_info[3])
        local_x = float(useful_info[4]) * 0.3048
        local_y = float(useful_info[5]) * 0.3048
        global_x = float(useful_info[6])
        global_y = float(useful_info[7])
        vehicle_length = float(useful_info[8])
        vehicle_width = float(useful_info[9])
        vehicle_class = float(useful_info[10])
        acc = float(useful_info[12])
        lane_id = int(useful_info[13])
        origin_zone = int(useful_info[14])
        destination_zone = int(useful_info[15])
        intersection_id = int(useful_info[16])
        movement_id = int(useful_info[19])
        speed = float(useful_info[11]) * 0.3048
        distance_headway = float(useful_info[22])
        section_id = int(useful_info[17])
        direction_id = int(useful_info[18])
        preceding_id = useful_info[20]
        following_id = useful_info[21]

        if not (vehicle_id in trajectory_dict.keys()):
            new_trajectory = Trajectory(vehicle_id)
            new_trajectory.origin_zone = origin_zone
            new_trajectory.destination_zone = destination_zone
            new_trajectory.vehicle_length = vehicle_length
            new_trajectory.vehicle_width = vehicle_width
            new_trajectory.vehicle_class = vehicle_class
            trajectory_dict[vehicle_id] = new_trajectory

        trajectory_dict[vehicle_id].space_headway_list.append(distance_headway)
        trajectory_dict[vehicle_id].velocity_list.append(speed)
        trajectory_dict[vehicle_id].following_list.append(following_id)
        trajectory_dict[vehicle_id].preceding_list.append(preceding_id)
        trajectory_dict[vehicle_id].movement_list.append(movement_id)
        trajectory_dict[vehicle_id].section_list.append(section_id)
        trajectory_dict[vehicle_id].direction_list.append(direction_id)
        trajectory_dict[vehicle_id].intersection_list.append(intersection_id)
        trajectory_dict[vehicle_id].lane_list.append(lane_id)
        trajectory_dict[vehicle_id].local_x_list.append(local_x)
        trajectory_dict[vehicle_id].local_y_list.append(local_y)
        trajectory_dict[vehicle_id].global_x_list.append(global_x)
        trajectory_dict[vehicle_id].global_y_list.append(global_y)
        trajectory_dict[vehicle_id].acc_list.append(acc)
        trajectory_dict[vehicle_id].time_list.append(time_slot)
        trajectory_dict[vehicle_id].epoch_list.append(epoch_time)
    return trajectory_dict

