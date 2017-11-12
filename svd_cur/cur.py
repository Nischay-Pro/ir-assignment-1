import svd
import numpy as np
import timeit
import error
import dataset



def cur(A):
    A = np.array(A)
    [rows, cols] = A.shape
    total = 0
    row_prob = np.zeros(rows)
    col_prob = np.zeros(cols)

    # Squared Frobenius norm of all Elements
    for x in range(0, rows):
        for y in range(0, cols):
            total = total + A[x][y]**2

    # Squared Frobenius norm of Rows
    for x in range(0, rows):
        row_total = 0
        for y in range(0, cols):
            row_total += A[x][y]**2
        row_prob[x] = row_total/total

    # Squared Frobenius norm of Columns
    for y in range(0, cols):
        col_total = 0
        for x in range(0, rows):
            col_total += A[x][y] **2
        col_prob[y] = col_total/total

    # Calculate the number of rows and columns to be selected
    small = np.minimum(rows, cols)
    r = int(small/2 + 1)

    # Select Columns based on probability
    Col_A = np.copy(A)
    Col_A_index = np.arange(cols)
    for x in range(0, cols):
        for y in range(0, cols-1):
            if col_prob[y] < col_prob[y+1]:
                col_prob[[y, y+1]] = col_prob[[y+1, y]]
                Col_A_index[[y, y+1]] = Col_A_index[[y+1, y]]
                Col_A[:, [y, y+1]] = Col_A[:, [y+1, y]]
    Col_A_index = np.delete(Col_A_index, np.s_[r:], 0)
    Col_A = np.delete(Col_A, np.s_[r:], 1)

    # Select Rows based on probability
    Row_A = np.copy(A)
    Row_A_index = np.arange(rows)
    for x in range(0, rows):
        for y in range(0, rows-1):
            if row_prob[y] < row_prob[y+1]:
                row_prob[[y, y+1]] = row_prob[[y+1, y]]
                Row_A_index[[y, y+1]] = Row_A_index[[y+1, y]]
                Row_A[[y, y+1], :] = Row_A[[y+1, y], :]
    Row_A_index = np.delete(Row_A_index, np.s_[r:], 0)
    Row_A = np.delete(Row_A, np.s_[r:], 0)

    # Calculate W matrix
    W = np.zeros((r, r))
    for x in range(0, r):
        for y in range(0, r):
            W[x][y] = A[Row_A_index[x]][Col_A_index[x]]

    # Calculating final C and R matrices
    C = np.zeros((rows, r))
    for x in range(0, rows):
        for y in range(0, r):
            C[x][y] = Col_A[x][y]/((r*col_prob[y])**0.5)
    R = np.zeros((r, cols))
    for x in range(0, r):
        for y in range(0, cols):
            R[x][y] = Row_A[x][y]/((r*row_prob[x])**0.5)

    # Calculating the matrices X, sigma and Y_tran
    X, sigma, Y_tran = svd.svd(W)
    sigma_row, sigma_col = sigma.shape
    for x in range(0, sigma_row):
        for y in range(0, sigma_col):
            if sigma[x][y] > 0:
                sigma[x][y] = 1/sigma[x][y]

    # Calculating the Matrix U
    sigma_plus = sigma
    Y = Y_tran.transpose()
    X_tran = X.transpose()
    U = np.matmul(Y, sigma_plus)
    U = np.matmul(U, X_tran)

    # calculating the matrix A_cur
    A_cur = np.matmul(C, U)
    A_cur = np.matmul(A_cur, R)

    return A_cur

start = timeit.default_timer()
print(error.rmse(dataset.data, cur(dataset.data)))
stop = timeit.default_timer()
print(stop-start)