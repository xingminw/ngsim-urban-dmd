import numpy as np
import initiate.config as config


def get_ordinary_section_eulerian(trajectory_dict, section_id):
    # fetch the trajectory data in this section
    trajs_dict = {"north": {"times": [], "xs": [], "ys": [], "lanes": []},
                  "south": {"times": [], "xs": [], "ys": [], "lanes": []}}
    north_lane_list = []
    south_lane_list = []
    distance_start = 700
    distance_end = 0
    for veh_id in trajectory_dict.keys():
        trajectory = trajectory_dict[veh_id]
        x_list = trajectory.local_x_list
        y_list = trajectory.local_y_list
        section_list = trajectory.section_list
        direction_list = trajectory.direction_list
        lane_list = trajectory.lane_list
        time_list = trajectory.time_list

        local_xs = []
        local_ys = []
        local_dirs = []
        local_lanes = []
        local_times = []
        for idx in range(len(x_list)):
            if section_list[idx] == section_id:
                local_xs.append(x_list[idx])
                local_ys.append(y_list[idx])
                local_dirs.append(direction_list[idx])
                local_lanes.append(lane_list[idx])
                local_times.append(time_list[idx])
        if len(local_dirs) == 0:
            continue

        distance_end = max([distance_end] + local_ys)
        distance_start = min([distance_start] + local_ys)
        if local_dirs[0] == 2:
            direction_key = "north"
            north_lane_list = set(list(north_lane_list) + local_lanes)
        elif local_dirs[0] == 4:
            direction_key = "south"
            south_lane_list = set(list(south_lane_list) + local_lanes)
        else:
            # print(local_dirs)
            continue
        trajs_dict[direction_key]["times"].append(local_times)
        trajs_dict[direction_key]["xs"].append(local_xs)
        trajs_dict[direction_key]["ys"].append(local_ys)
        trajs_dict[direction_key]["lanes"].append(local_lanes)

    # convert the trajectory to Eulerian matrix
    distance_interval = 20
    distance_start = int(distance_start / distance_interval)
    distance_end = int(distance_end / distance_interval)
    distance_frames = distance_end - distance_start + 1
    # north_lanes = sum([val <= 5 for val in list(north_lane_list)])
    # south_lanes = sum([val <= 5 for val in list(south_lane_list)])
    north_lanes = 2
    south_lanes = 2
    total_geo_frames = distance_frames * north_lanes
    time_interval = 5
    total_time_frames = int(1000 / time_interval)
    print(north_lanes, south_lanes, distance_frames, total_geo_frames, total_time_frames)

    total_travel_distance_matrix = np.ones((total_geo_frames, total_time_frames)) * 0.01 * 12
    total_travel_time_matrix = np.ones((total_geo_frames, total_time_frames)) * 0.01
    density_matrix = np.zeros((total_geo_frames, total_time_frames))
    for idx in range(len(trajs_dict["north"]["times"])):
        vehicle_occupancy = np.zeros((total_geo_frames, total_time_frames))
        time_list = trajs_dict["north"]["times"][idx]
        lanes_list = trajs_dict["north"]["lanes"][idx]
        x_list = trajs_dict["north"]["xs"][idx]
        y_list = trajs_dict["north"]["ys"][idx]
        if len(time_list) < 5:
            continue

        for jdx in range(len(time_list) - 1):
            local_distance = np.sqrt(pow(x_list[jdx + 1] - x_list[jdx], 2)
                                     + pow(y_list[jdx + 1] - y_list[jdx], 2))
            local_time_interval = time_list[jdx + 1] - time_list[jdx]
            local_y_int = int(y_list[jdx] / distance_interval) - distance_start

            local_y_int = local_y_int + (lanes_list[jdx] - 1) * distance_frames
            local_t_int = int(time_list[jdx] / time_interval)

            if not (lanes_list[jdx]) in [1, 2]:
                continue
            if local_t_int < total_time_frames:
                total_travel_distance_matrix[local_y_int, local_t_int] += local_distance
                total_travel_time_matrix[local_y_int, local_t_int] += local_time_interval
                vehicle_occupancy[local_y_int, local_t_int] = 1
        density_matrix += vehicle_occupancy

    velocity_matrix = total_travel_distance_matrix / total_travel_time_matrix
    north_velocity_matrix = velocity_matrix
    north_density_matrix = density_matrix

    total_geo_frames = distance_frames * south_lanes
    total_travel_distance_matrix = np.ones((total_geo_frames, total_time_frames)) * 0.01 * 12
    total_travel_time_matrix = np.ones((total_geo_frames, total_time_frames)) * 0.01
    density_matrix = np.zeros((total_geo_frames, total_time_frames))
    for idx in range(len(trajs_dict["south"]["times"])):
        vehicle_occupancy = np.zeros((total_geo_frames, total_time_frames))
        time_list = trajs_dict["south"]["times"][idx]
        lanes_list = trajs_dict["south"]["lanes"][idx]
        x_list = trajs_dict["south"]["xs"][idx]
        y_list = trajs_dict["south"]["ys"][idx]
        if len(time_list) < 5:
            continue

        for jdx in range(len(time_list) - 1):
            local_distance = np.sqrt(pow(x_list[jdx + 1] - x_list[jdx], 2)
                                     + pow(y_list[jdx + 1] - y_list[jdx], 2))
            local_time_interval = time_list[jdx + 1] - time_list[jdx]
            local_y_int = int(y_list[jdx] / distance_interval) - distance_start

            local_y_int = local_y_int + (lanes_list[jdx] - 1) * distance_frames
            local_t_int = int(time_list[jdx] / time_interval)

            if not (lanes_list[jdx]) in [1, 2]:
                continue
            if local_t_int < total_time_frames:
                total_travel_distance_matrix[local_y_int, local_t_int] += local_distance
                total_travel_time_matrix[local_y_int, local_t_int] += local_time_interval
                vehicle_occupancy[local_y_int, local_t_int] = 1
        density_matrix += vehicle_occupancy

    velocity_matrix = total_travel_distance_matrix / total_travel_time_matrix
    south_density_matrix = density_matrix
    south_velocity_matrix = velocity_matrix

    import matplotlib.pyplot as plt
    plt.subplot(411)
    plt.imshow(north_velocity_matrix, cmap=config.congestion_color, aspect="auto")
    plt.colorbar()
    plt.subplot(412)
    plt.imshow(north_density_matrix, cmap=config.density_color, aspect="auto")
    plt.colorbar()
    plt.subplot(413)
    plt.imshow(south_velocity_matrix, cmap=config.congestion_color, aspect="auto")
    plt.colorbar()
    plt.subplot(414)
    plt.imshow(south_density_matrix, cmap=config.density_color, aspect="auto")
    plt.colorbar()
    plt.show()
    plt.close()

    # plt.figure()
    # overall_xs = []
    # overall_ys = []
    # lane1_xs = []
    # lane1_ys = []
    # lane2_xs = []
    # lane2_ys = []
    # lane3_xs = []
    # lane3_ys = []
    # for idx in range(len(trajs_dict["north"]["times"])):
    #     overall_xs += trajs_dict["north"]["xs"][idx]
    #     overall_ys += trajs_dict["north"]["ys"][idx]
    #     lane_list = trajs_dict["north"]["lanes"][idx]
    #     x_list = trajs_dict["north"]["xs"][idx]
    #     y_list = trajs_dict["north"]["ys"][idx]
    #     for jdx in range(len(x_list)):
    #         if lane_list[jdx] == 11:
    #             lane1_xs.append(x_list[jdx])
    #             lane1_ys.append(y_list[jdx])
    #         if lane_list[jdx] == 1:
    #             lane2_xs.append(x_list[jdx])
    #             lane2_ys.append(y_list[jdx])
    #         if lane_list[jdx] == 2:
    #             lane3_xs.append(x_list[jdx])
    #             lane3_ys.append(y_list[jdx])
    #
    # plt.plot(lane1_xs[::10], lane1_ys[::10], "r.", alpha=0.5, label="north lane 11")
    # plt.plot(lane2_xs[::10], lane2_ys[::10], "g.", alpha=0.5, label="north lane 1")
    # plt.plot(lane3_xs[::10], lane3_ys[::10], "b.", alpha=0.5, label="north lane 2")
    #
    # lane1_xs = []
    # lane1_ys = []
    # lane2_xs = []
    # lane2_ys = []
    # lane3_xs = []
    # lane3_ys = []
    # for idx in range(len(trajs_dict["south"]["times"])):
    #     overall_xs += trajs_dict["south"]["xs"][idx]
    #     overall_ys += trajs_dict["south"]["ys"][idx]
    #     lane_list = trajs_dict["south"]["lanes"][idx]
    #     x_list = trajs_dict["south"]["xs"][idx]
    #     y_list = trajs_dict["south"]["ys"][idx]
    #     for jdx in range(len(x_list)):
    #         if lane_list[jdx] == 11:
    #             lane1_xs.append(x_list[jdx])
    #             lane1_ys.append(y_list[jdx])
    #         if lane_list[jdx] == 1:
    #             lane2_xs.append(x_list[jdx])
    #             lane2_ys.append(y_list[jdx])
    #         if lane_list[jdx] == 2:
    #             lane3_xs.append(x_list[jdx])
    #             lane3_ys.append(y_list[jdx])
    #
    # plt.plot(lane1_xs[::10], lane1_ys[::10], "k.", alpha=0.5, label="south lane 11")
    # plt.plot(lane2_xs[::10], lane2_ys[::10], "m.", alpha=0.5, label="south lane 1")
    # plt.plot(lane3_xs[::10], lane3_ys[::10], "c.", alpha=0.5, label="south lane 2")
    # # plt.show()
    # plt.legend()
    # plt.xlabel("Local x (m)")
    # plt.ylabel("Local y (m)")
    # plt.tight_layout()
    # plt.savefig("figures/section_" + str(section_id) + ".png", dpi=300)
    # plt.close()
    # # exit()

    return north_density_matrix, north_velocity_matrix, south_density_matrix, south_velocity_matrix


def get_intersection_eulerian(trajectory_dict, section_id):
    pass

