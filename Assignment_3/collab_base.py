import dataset
import math as m
import error
import numpy as np

movies = dataset.movies
users = dataset.users
mean = [0]*movies
data = dataset.data.astype(float)


# Function to estimate the rating using collaborative filtering along with global baseline approach
def predict_base(matrix, item, user):
    mean_all = cal_mean(matrix)
    base_est = mean_all + dev_item(item, mean_all) + dev_user(user, mean_all)
    collab_base = base_est + collab(data, item, user, mean_all)
    return collab_base


# Collaborative with baseline estimate
def collab(arr, item, user, mu):
    normalized = normalize(arr)
    sim = similar(normalized, item)
    den, res = 0, 0.0
    temp = dataset.data.astype(float)
    for x in range(0, movies):
        if sim[x] > 0 and x != item:
            res += (temp[x][user] - (mu + dev_user(user, mu) + dev_item(x, mu)))*sim[x]
            den += sim[x]
    return res/den


# Deviation of item rating
def dev_item(item, mu):
    arr = dataset.data
    count_i = 0.0
    num_i = 0.0
    for y in range(0, users):
        if arr[item][y] > 0:
            num_i += arr[item][y]
            count_i += 1
    res = num_i/count_i - mu
    return res


# Deviation of User rating
def dev_user(user, mu):
    arr = dataset.data
    count_u = 0.0
    num_u = 0.0
    for x in range(0, movies):
        if arr[x][user] > 0:
            num_u += arr[x][user]
            count_u += 1
    res = (num_u/count_u) - mu
    return res


# Calculating the mean rating
def cal_mean(arr):
    count = 0.0
    num = 0.0
    for x in range(0, movies):
        for y in range (0, users):
            if arr[x][y] > 0:
                num += arr[x][y]
                count += 1
    return num/count


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
        sim[x] = sim[x]/m.sqrt(deni*denc)
    return sim


# Function Call to check the functionality of collaborative filtering along with baseline approach
original = dataset.data[0:100, 0:100]
calculate = np.zeros((100, 100))
for x in range(0, 100):
    for y in range(0, 100):
        if original[x][y] > 0:
            calculate[x][y] = predict_base(dataset.data, x, y)


