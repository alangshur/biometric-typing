from data import data
import math

# get train data
invalid_data = data.getPhatPheatures()
valid_data = None

# partition data
invalid_train_size = math.ceil(len(invalid_data) * 0.85)
invalid_test_size = len(invalid_data) - invalid_train_size
valid_train_size = math.ceil(len(valid_data) * 0.85)
valid_test_size = len(valid_data) - valid_train_size

# 


print(invalid_train_size)
print(invalid_test_size)