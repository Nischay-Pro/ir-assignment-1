import svd
import numpy as np
import error
import timeit
import dataset



def cur_random(A):
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

    # Select Columns randomly
    C = np.zeros((rows, r))
    Col_A = np.copy(A)
    Col_A_index = np.random.choice(cols, r)
    for x in range(0, r):
            C[:, x] = Col_A[:, Col_A_index[x]]
    for x in range(0, rows):
        for y in range(0, r):
            C[x][y] = C[x][y]/((r*col_prob[Col_A_index[y]])**0.5)

    # Select Rows randomly
    R = np.zeros((r, cols))
    Row_A = np.copy(A)
    Row_A_index = np.random.choice(rows, r)
    for x in range(0, r):
            R[x, :] = Row_A[Row_A_index[x], :]
    for x in range(0, rows):
        for y in range(0, r):
            C[x][y] = C[x][y]/((r*row_prob[Row_A_index[y]])**0.5)

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
    sigma_plus = sigma

    # Calculating the Matrix U
    Y = Y_tran.transpose()
    X_tran = X.transpose()
    U = np.matmul(Y, sigma_plus)
    U = np.matmul(U, X_tran)

    # calculating the matrix A_cur_ran
    A_cur_ran = np.matmul(C, U)
    A_cur_ran = np.matmul(A_cur_ran, R)

    return A_cur_ran

start = timeit.default_timer()
print(error.rmse(dataset.data, cur_random(dataset.data)))
stop = timeit.default_timer()
