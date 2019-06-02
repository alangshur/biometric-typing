#          _____                    _____                    _____                    _____
#         /\    \                  /\    \                  /\    \                  /\    \
#        /::\____\                /::\    \                /::\    \                /::\____\
#       /::::|   |               /::::\    \               \:::\    \              /::::|   |
#      /:::::|   |              /::::::\    \               \:::\    \            /:::::|   |
#     /::::::|   |             /:::/\:::\    \               \:::\    \          /::::::|   |
#    /:::/|::|   |            /:::/__\:::\    \               \:::\    \        /:::/|::|   |
#   /:::/ |::|   |           /::::\   \:::\    \              /::::\    \      /:::/ |::|   |
#  /:::/  |::|___|______    /::::::\   \:::\    \    ____    /::::::\    \    /:::/  |::|   | _____
# /:::/   |::::::::\    \  /:::/\:::\   \:::\    \  /\   \  /:::/\:::\    \  /:::/   |::|   |/\    \
#/:::/    |:::::::::\____\/:::/  \:::\   \:::\____\/::\   \/:::/  \:::\____\/:: /    |::|   /::\____\
#\::/    / ~~~~~/:::/    /\::/    \:::\  /:::/    /\:::\  /:::/    \::/    /\::/    /|::|  /:::/    /
# \/____/      /:::/    /  \/____/ \:::\/:::/    /  \:::\/:::/    / \/____/  \/____/ |::| /:::/    /
#             /:::/    /            \::::::/    /    \::::::/    /                   |::|/:::/    /
#            /:::/    /              \::::/    /      \::::/____/                    |::::::/    /
#           /:::/    /               /:::/    /        \:::\    \                    |:::::/    /
#          /:::/    /               /:::/    /          \:::\    \                   |::::/    /
#         /:::/    /               /:::/    /            \:::\    \                  /:::/    /
#        /:::/    /               /:::/    /              \:::\____\                /:::/    /
#        \::/    /                \::/    /                \::/    /                \::/    /
#         \/____/                  \/____/                  \/____/                  \/____/
#                                                                                                    


from data import data
import numpy as np
import math
from models import log_reg
import random, sys

mode = sys.argv[1]

# get train data
validData, invalidData = data.generateAllFeatureSets(mode)

# filter data
filteredDataV, filteredDataIV, ordering = [], [], list(validData[0].keys())
for data in invalidData:
    values = []
    for key in ordering: values.append(data[key])
    entry = np.array(values)
    filteredDataIV.append((entry, 0))
for data in validData:
    weightSize = len(data)
    values = []
    for key in ordering: values.append(data[key])
    entry = np.array(values)
    filteredDataV.append((entry, 1))

# partition data
filteredTrainData, filteredTestData = [], []
validSplit = math.ceil(len(filteredDataV) * 0.85)
invalidSplit = math.ceil(len(filteredDataIV) * 0.85)
filteredTrainData = filteredDataIV[:invalidSplit] + filteredDataV[:validSplit]
filteredTestData = filteredDataIV[invalidSplit:] + filteredDataV[validSplit:]
random.shuffle(filteredTrainData)
random.shuffle(filteredTestData)

# train data
model = log_reg.LogisticRegression(filteredTrainData, filteredTestData, T = 0.56, wSize = weightSize)
model.trainLR(90, 0.01, 'normal')

# test data
model.testLR()