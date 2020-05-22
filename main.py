import json
import numpy as np
import matplotlib.pyplot as plt
import initiate.config as config
from analysis.svd_analysis import svd_analysis
from analysis.hankel import get_hankel_matrix
from analysis.dmd_analysis import hankel_dmd_analysis


matrix_file_name = "figures/matrix.json"


def main():
    with open(matrix_file_name, "r") as temp_file:
        matrix_json = json.load(temp_file)

    # print(xticks)
    density_matrix = np.mat(matrix_json["density"])
    velocity_matrix = np.mat(matrix_json["velocity"])

    # svd analysis for the two matrices
    svd_analysis(density_matrix, 50, "density", cmap=config.density_color)
    svd_analysis(velocity_matrix, 50, "velocity", cmap=config.congestion_color)

    # dmd analysis for density matrix and velocity matrix
    delay_embedding = 30
    selected_ranks = 121

    hankel_dmd_analysis(velocity_matrix, selected_ranks, delay_embedding, "velocity", cmap=config.congestion_color)
    hankel_dmd_analysis(density_matrix, selected_ranks, delay_embedding, "density", cmap=config.density_color)


if __name__ == '__main__':
    main()
