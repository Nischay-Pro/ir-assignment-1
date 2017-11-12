import svd
import numpy as np
import dataset
import error
import timeit


def svd_90(A):
    [U, sigma, V_tran] = svd.svd(A)
    index = 0
    eng_total = 0
    eng_90 = 0
    order = 0
    row, col = sigma.shape
    # Calculate the Total energy of the Sigma matrix
    while row > index:
        eng_total += sigma[index][index]**2
        index += 1
    # Gives the order of the Sigma matrix which constitutes 90% of the energy of the original matrix
    for x in range(0, index):
        eng_90 += sigma[x][x]**2
        if eng_90/eng_total > 0.9:
            order = x+1
            break
    # Reduce the Sigma matrix to the acquired order
    sigma = np.delete(sigma, np.s_[2:], 0)
    sigma = np.delete(sigma, np.s_[2:], 1)
    row_sigma, col_sigma = sigma.shape
    U = np.delete(U, np.s_[2:], 1)
    V_tran = np.delete(V_tran, np.s_[2:], 0)

    A_svd_90 = np.matmul(U, sigma)
    A_svd_90 = np.matmul(A_svd_90, V_tran)

    return A_svd_90
start = timeit.default_timer()
print(error.rmse(dataset.data, svd_90(dataset.data)))
stop = timeit.default_timer()
print(stop-start)
