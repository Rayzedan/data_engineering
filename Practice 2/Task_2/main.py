import os
import numpy as np


def filter_matrix(path: str) -> None:
    matrix = np.load(path)
    indices1, indices2, values = [], [], []
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i, j] > 555:
                indices1.append(i)
                indices2.append(j)
                values.append(matrix[i, j])
    if save_file(indices1, indices2, values):
        compare_size_files('values.npz', 'values_compressed.npz')


def save_file(indices1, indices2, values) -> bool:
    np.savez('values.npz', indices1=indices1, indices2=indices2, values=values)
    np.savez_compressed('values_compressed.npz', indices1=indices1, indices2=indices2, values=values)
    return os.path.exists('values.npz') and os.path.exists('values.npz')


def compare_size_files(first_file: str, second_file: str) -> None:
    print('values size:', round(os.path.getsize(first_file) / 1024, 2), 'KB')
    print('values_compressed size:', round(os.path.getsize(second_file) / 1024, 2), 'KB')


if __name__ == '__main__':
    filter_matrix('matrix_55_2.npy')
