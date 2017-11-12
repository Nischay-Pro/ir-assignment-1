import csv
import numpy as np
users = 943
movies = 1682
ratings = np.zeros((movies, users))
count = 0
with open('ratings.csv') as csv_file:
    readCSV = csv.reader(csv_file,delimiter=',')
    for row in readCSV:
        if count == 0:
            count += 1
            continue
        u = int(row[0])-1
        m = int(row[1])-1
        r = float(row[2])
        if u < 943 and m < 1682:
            ratings[m][u] = r
data = ratings