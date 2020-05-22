import numpy as np
import matplotlib.pyplot as plt
import initiate.config as config


def svd_analysis(original_matrix, truncated_r, name="", cmap=config.density_color):
    # perform singular value decomposition to the matrices
    density_u, density_s, density_vh = np.linalg.svd(original_matrix)
    density_s_matrix = np.zeros(np.shape(original_matrix))
    for index_s in range(len(density_s)):
        if index_s >= truncated_r:
            continue
        density_s_matrix[index_s, index_s] = density_s[index_s]
    density_s_matrix = np.mat(density_s_matrix)

    # plot the svd results
    plt.figure(figsize=[12, 4])
    plt.subplot(131)
    plt.plot([val / np.sum(density_s) for val in density_s], "b.")
    plt.title("Singular values of " + name + " matrix")
    plt.subplot(132)
    plt.imshow(original_matrix, aspect="auto", cmap=cmap[0], vmin=cmap[1], vmax=cmap[2])
    plt.xticks([])
    plt.yticks([])
    plt.xlabel("Time")
    plt.ylabel("Location / lane")
    plt.title("Original " + name + " matrix")
    plt.subplot(133)
    plt.imshow(density_u * density_s_matrix * density_vh, aspect="auto",
               cmap=cmap[0], vmin=cmap[1], vmax=cmap[2])
    plt.xticks([])
    plt.yticks([])
    plt.xlabel("Time")
    plt.ylabel("Location / lane")
    plt.colorbar()
    plt.title("SVD truncated " + name + " matrix (r=" + str(truncated_r) + ")")
    plt.tight_layout()
    plt.savefig("figures/" + name + "_svd.png", dpi=300)
    # plt.show()
    plt.close()
