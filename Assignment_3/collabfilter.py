import dataset
import numpy as np
import error

data = dataset.data
movies = dataset.movies
users = dataset.users
mean = [0]*movies
data = data.astype(float)


# Function to estimate the rating of item x with respect to user y
def predict(matrix, item, user):
    normalized = normalize(matrix)
    sim = similar(normalized, item)
    res = evaluate(dataset.data, sim, item, user)
    return res


# Obtain the normalized matrix
def normalize(arr):
    for x in range(0, movies):
        var = 0
        count = 0
        for y in range(0, users):
            if arr[x][y] > 0:
                count = count + 1
                var = var + arr[x][y]
        if count == 0:
            mean[x] = 0
        else:
            mean[x] = var/count
    for x in range(0, movies):
        for y in range(0, users):
            if arr[x][y] > 0:
                arr[x][y] = arr[x][y] - mean[x]
    return data


# Calculate similarity of an item with respect to other items
def similar(arr, item):
    sim = [0]*movies
    for x in range(0, movies):
        deni = 0.0
        denc = 0.0
        for y in range(0, users):
            sim[x] += arr[x][y]*arr[item][y]
            deni += arr[item][y]**2
            denc += arr[x][y]**2
        sim[x] = sim[x]/((deni*denc)**0.5)
    return sim


# Estimate the rating of item x by user y
def evaluate(arr, sim, item, user):
    den = 0.0
    num = 0.0
    for x in range(0, movies):
        if sim[x] > 0 and x != item:
            num += arr[x][user]*sim[x]
            den += sim[x]
    return num/den

# Function call to test the functionality of collaborative filtering
original = dataset.data
calculate = np.zeros((movies, users))
for x in range(0, movies):
    for y in range(0, users):
        if original[x][y] > 0:
            calculate[x][y] = predict(dataset.data, x, y)
