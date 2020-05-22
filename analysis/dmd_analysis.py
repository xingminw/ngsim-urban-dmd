import numpy as np
import matplotlib.pyplot as plt
from analysis.hankel import get_hankel_matrix


def hankel_dmd_analysis(original_matrix, truncated_r, delay_embedding, name, cmap):
    (real_m, n) = np.shape(original_matrix)
    bg_matrix = np.mean(original_matrix, 1) * np.ones((1, n))
    subtracted_matrix = original_matrix - bg_matrix

    hankel_matrix = get_hankel_matrix(subtracted_matrix, delay_embedding)
    bg_matrix = bg_matrix[:, : -delay_embedding]
    (m, n) = np.shape(hankel_matrix)
    truncated_r = min(m - 1, n - 1, truncated_r)

    current_matrix = hankel_matrix[:, :n-1]
    next_matrix = hankel_matrix[:, 1:]
    print(np.shape(current_matrix), np.shape(next_matrix))

    u, s, vh = np.linalg.svd(current_matrix)
    u_r = u[:, : min(truncated_r, m)]
    vh_r = vh[: min(truncated_r, n), :]

    s_matrix = np.mat(np.diag(s[: min(truncated_r, m, n)]))

    a_tilde = u_r.H * next_matrix * vh_r.H * np.linalg.inv(s_matrix)
    w, v = np.linalg.eig(a_tilde)

    modes_phi = next_matrix * vh_r.H * np.linalg.inv(s_matrix) * v
    b = np.linalg.pinv(modes_phi) * current_matrix[:, 0]

    epsilon = 0.01
    unstable_w = []
    periodic_w = []
    stable_w = []
    for mode_w in w:
        if abs(mode_w) > 1 + epsilon / 10:
            unstable_w.append(mode_w)
        elif abs(mode_w) < 1 - epsilon:
            stable_w.append(mode_w)
        else:
            periodic_w.append(mode_w)

    # plot the distribution of the eigenvalues
    plt.figure(figsize=[9, 8])
    circle_angle = np.linspace(0, 2 * np.pi, 1000)
    circle_x = np.sin(circle_angle)
    circle_y = np.cos(circle_angle)
    plt.plot(circle_x, circle_y, "k--")
    plt.plot([val.real for val in stable_w], [val.imag for val in stable_w], "go", label="Stable modes")
    plt.plot([val.real for val in unstable_w], [val.imag for val in unstable_w], "ro", label="Unstable modes")
    plt.plot([val.real for val in periodic_w], [val.imag for val in periodic_w], "bo", label="Periodic modes")
    plt.axis("equal")
    # display_range = 1.2
    # plt.xlim([-display_range, display_range])
    # plt.ylim([-display_range, display_range])
    plt.xlabel("Re")
    plt.ylabel("Im")
    plt.legend()
    plt.grid()
    plt.savefig("figures/eigen-values-" + name + ".png", dpi=300)
    plt.close()

    cycle_list = []
    for val in w:
        if val.imag == 0:
            cycle_list.append(10000000000000000)
        else:
            cycle_list.append(abs(2 * np.pi / np.arctan(val.imag / val.real)))

    # plot the modes
    modes_matrix_list = []
    overall_reconstruct_matrix = np.zeros((real_m, n))
    for imode in range(len(w)):
        mode_matrix = (modes_phi[:, imode] * b[imode]).real
        for i_t in range(n - 1):
            current_state = modes_phi[:, imode] * (w[imode] ** (i_t + 1)) * b[imode]
            current_state = current_state.real
            mode_matrix = np.concatenate((mode_matrix.T, current_state.T)).T

        modes_matrix_list.append(mode_matrix[:real_m, :])
        overall_reconstruct_matrix += mode_matrix[:real_m, :]

    energy_list = []
    for mode_matrix in modes_matrix_list:
        energy_list.append(np.sqrt(np.average(np.square(mode_matrix))))

    xticks = [int(val) for val in np.linspace(0, int(n / 12 / 2) * 12 * 2, int(n / 12 / 2) + 1)]
    xticks_labels = [str(2 * val) for val in range(len(xticks))]

    display_modes_num = min(10, truncated_r)
    top_energy_mode_index = np.argsort(energy_list)[::-1][:display_modes_num]

    for i_dmode in range(len(top_energy_mode_index)):
        mode_idx = int(top_energy_mode_index[i_dmode])
        mode_matrix = modes_matrix_list[mode_idx]
        plt.imshow(mode_matrix + bg_matrix, cmap=cmap[0], vmin=cmap[1], vmax=cmap[2], aspect="auto")
        plt.title("Handel-DMD Reconstructed " + name + " mode " + str(i_dmode))
        plt.xticks(xticks, xticks_labels)
        plt.xlabel("Time (minute)")
        plt.ylabel("Location/lane")
        plt.colorbar()
        plt.tight_layout()
        plt.savefig("figures/" + name + "_mode-" + str(i_dmode) + ".png", dpi=300)
        plt.close()

    plt.figure()
    plt.plot([1 / val for val in cycle_list], energy_list, "b*")
    # plt.ylim([0, 0.3])
    plt.xlim([0, 0.25])
    cycle_lengths_ticks = [500, 150, 80, 40, 20]
    frequency_ticks = [1 / (val / 5) for val in cycle_lengths_ticks]
    plt.xticks(frequency_ticks, [str(val) for val in cycle_lengths_ticks])
    plt.xlabel("Frequency (Cycle: seconds)")
    plt.ylabel("Average amplitude")
    plt.title("Amplitude frequency distribution of " + name)
    plt.savefig("figures/amplitude_" + name + ".png", dpi=300)
    plt.close()

    # plot the overall reconstructed matrix
    plt.figure(figsize=[8, 6])
    plt.imshow(overall_reconstruct_matrix + bg_matrix, cmap=cmap[0], vmin=cmap[1], vmax=cmap[2], aspect="auto")
    plt.title("Handel-DMD Reconstructed " + name + " heatmap")
    plt.xticks(xticks, xticks_labels)
    plt.xlabel("Time (minute)")
    plt.ylabel("Location/lane")
    plt.colorbar()
    plt.tight_layout()
    plt.savefig("figures/constructed_" + name + ".png", dpi=300)
    plt.close()

    # plot the original matrix
    plt.figure(figsize=[8, 6])
    plt.imshow(original_matrix, cmap=cmap[0], vmin=cmap[1], vmax=cmap[2], aspect="auto")
    plt.title(name + " heatmap")
    plt.xticks(xticks, xticks_labels)
    plt.xlabel("Time (minute)")
    plt.ylabel("Location/lane")
    plt.colorbar()
    plt.tight_layout()
    plt.savefig("figures/original_" + name + ".png", dpi=300)
    plt.close()
    return w, modes_phi, b, overall_reconstruct_matrix


if __name__ == '__main__':
    a = np.mat([[1], [2]])
    b = np.mat([[2], [5]])
    print(np.concatenate((a.T, b.T)).T, type(a))
    a = np.array([1, 2, 3, 4])
    print(a ** 2)
