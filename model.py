import csv, sys
import numpy as np
import re

# get subject
assert len(sys.argv) == 2
subject_id = sys.argv[1]
assert re.match(r'^s[0]*[0-9]*$', subject_id) != None

# collect subject data
seen_data = False
subject_data = np.array([[0, 0], [0, 0]])
with open('password-data.csv') as file:
    data = csv.reader(file, delimiter = ',')
    for row in data:
        if row[0] == 'subject': continue
        if row[0] != subject_id and seen_data == True: 
            print("Finished data collection.")
            break
        elif row[0] != subject_id and seen_data == False: continue
        elif seen_data == False: seen_data = True
        num_row = [float(d) for d in row[3:]]
        new_data = np.array(num_row)
        if subject_data.shape == (2, 2): subject_data = new_data
        else: subject_data = np.vstack([subject_data, new_data])
assert np.sum(subject_data) > 0.

# partition data
data_partition = (0.90, 0.10)
assert sum(data_partition) == 1.0
dimensions = subject_data.shape
train_size = int(round(dimensions[0] * data_partition[0]))
test_size = dimensions[0] - train_size
print("Finished data partition.")

# train data
mean_vector = [0] * dimensions[1]
for i in range(train_size):
    mean_vector = np.add(mean_vector, subject_data[i,:])
mean_vector = np.multiply(1. / float(train_size), mean_vector)
print("Finished data training.")

# test data
scores = []
for i in range(0, test_size):
    j = i + train_size
    score = np.subtract(mean_vector, subject_data[j,:])
    score = np.absolute(score)
    scores.append(np.sum(score))
print("Final score: {}".format(sum(scores) / len(scores)))
