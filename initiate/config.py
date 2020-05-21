from matplotlib.colors import ListedColormap, LinearSegmentedColormap


data_folder = "H:\\Data\\Peachtree-Main-Data\\vehicle-trajectory-data\\0400pm-0415pm"
# data_folder = "H:\\Data\Peachtree-Main-Data\\vehicle-trajectory-data\\1245pm-0100pm"

colors = ["red", "yellow", "green"]
congestion_color = LinearSegmentedColormap.from_list("mycmap", colors)

colors = ["green", "yellow", "red"]
density_color = LinearSegmentedColormap.from_list("mycmap", colors)

