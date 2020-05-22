import initiate.config as config
import matplotlib.pyplot as plt
from initiate.load_data import load_data
from data_format.eulerian import get_eulerian_density_velocity


trajectory_dict = load_data(config.data_folder)
get_eulerian_density_velocity(trajectory_dict, debug=False)

select_intersection = 7
overall_x_list = []
overall_y_list = []
section_x_list = [[] for temp in range(7)]
section_y_list = [[] for temp in range(7)]
overall_time_list = []
overall_section_list = []
overall_speed_list = []

for veh_id in trajectory_dict.keys():
    trajectory = trajectory_dict[veh_id]
    x_list = trajectory.local_x_list
    y_list = trajectory.local_y_list
    section_list = trajectory.section_list
    for idx in range(len(section_list)):
        section_x_list[section_list[idx]].append(x_list[idx])
        section_y_list[section_list[idx]].append(y_list[idx])
        if not (section_list[idx] in overall_section_list):
            overall_section_list.append(section_list[idx])
    overall_x_list += x_list
    overall_y_list += y_list
    overall_time_list += trajectory.time_list
    overall_speed_list += trajectory.velocity_list

plt.figure()
plt.hist(overall_speed_list, bins=100)
plt.savefig("figures/speed_hist.png", dpi=300)
plt.title("Histogram of velocity (m/s)")
plt.close()

plt.figure()
plt.hist(overall_time_list, bins=100)
# print(np.min(overall_time_list), np.max(overall_time_list))
plt.title("Histogram of time (s)")
plt.savefig("figures/time_hist.png", dpi=300)
plt.close()

# print(overall_section_list)

color_list = ["purple", "b", "r", "g", "c", "gold", "m"]
plt.figure(figsize=[5, 10])
for sec_id in range(len(section_x_list)):
    plt.plot(section_x_list[sec_id], section_y_list[sec_id], ".", color=color_list[sec_id], alpha=0.05)
# plt.plot(overall_x_list, overall_y_list, "k.", alpha=0.005)
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.xlim([-20, 20])
plt.legend()
plt.tight_layout()
plt.savefig("figures/section.png", dpi=300)
plt.close()
