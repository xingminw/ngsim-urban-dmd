import matplotlib.pyplot as plt
import config
import glob


chosen_intersection_id = 0
chosen_movement = 1


file_name_list = glob.glob(config.data_folder + "/*.txt")

with open(file_name_list[0], "r") as temp_file:
    all_lines = temp_file.readlines()

speed_list = []
headway_list = []

for single_line in all_lines[:]:
    split_info = single_line.split(" ")
    useful_info = []
    for info in split_info:
        if info is not "":
            useful_info.append(info)

    intersection_id = int(useful_info[16])
    movement_id = int(useful_info[19])
    speed = float(useful_info[11])
    distance_headway = float(useful_info[22])
    if distance_headway == 0:
        continue
    # if movement_id != chosen_movement:
    #     continue
    # if intersection_id != chosen_intersection_id:
    #     continue

    # print(intersection_id, movement_id, speed, distance_headway)
    # exit()
    # print(len(useful_info))
    # print(useful_info)
    if distance_headway == 0:
        continue
    speed_list.append(speed)
    headway_list.append(distance_headway)


plt.figure()
plt.plot(headway_list[::10], speed_list[::10], "b.", alpha=0.2)
plt.show()


