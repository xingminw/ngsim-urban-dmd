import numpy as np


def get_hankel_matrix(original_matrix, delay_embedding=10, debug=False):
    (m, n) = np.shape(original_matrix)
    if delay_embedding >= n - 10:
        print("delay embedding to large")
        exit()
    hankel_matrix = original_matrix[:, :n - delay_embedding]
    for i_d in range(delay_embedding - 1):
        matrix_to_append = original_matrix[:, i_d + 1: n - delay_embedding + i_d + 1]
        hankel_matrix = np.concatenate((hankel_matrix, matrix_to_append))

    if debug:
        import matplotlib.pyplot as plt
        plt.figure()
        plt.imshow(hankel_matrix, aspect="auto")
        plt.show()
    return hankel_matrix


