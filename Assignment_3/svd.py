import numpy as np
from numpy import linalg as LA

A = [[1, 1, 1, 0, 0],
     [3, 3, 3, 0, 0],
     [4, 4, 4, 0, 0],
     [5, 5, 5, 0, 0],
     [0, 2, 0, 4, 4],
     [0, 0, 0, 5, 5],
     [0, 1, 0, 2, 2]]

'''A = [[3, 2, 2],
     [2, 3, -2]]'''


def svd(A):
    A = np.array(A)
    A_tran = A.transpose()
    [movies, users] = A.shape

    # Calculate the eigen-values and eigen-vectors of A_tran_A
    A_tran_A = np.matmul(A_tran, A)
    eig_val_V, eig_vect_V = LA.eig(np.array(A_tran_A))
    for x in range(0, len(eig_val_V)-1):
        if eig_val_V[x] > eig_val_V[x+1]:
            continue
        else:
            eig_val_V[[x, x+1]] = eig_val_V[[x+1, x]]
            eig_vect_V[:, x] = -1*eig_vect_V[:, x]
            eig_vect_V[:, x+1] = -1*eig_vect_V[:, x+1]
            eig_vect_V[:, [x, x+1]] = eig_vect_V[:, [x+1, x]]
    V = eig_vect_V
    index = 0
    for x in range(0, len(eig_val_V)):
        if eig_val_V[x] > 0.01:
            index += 1
        else:
            break
    eig_val_V = np.delete(eig_val_V, np.s_[index:], 0)

    # Calculating Sigma
    sigma = np.zeros((index, index))
    for x in range(0, index):
        sigma[x][x] = eig_val_V[x]**0.5
    V = np.delete(V, np.s_[index:], 1)
    V_tran = V.transpose()

    # Calculate the matrix U
    A_V = np.matmul(A, V)
    row, col = A_V.shape
    for x in range(0, row):
        for y in range(0, col):
            A_V[x][y] = A_V[x][y]/sigma[y][y]
    U = A_V

    return U, sigma, V_tran

