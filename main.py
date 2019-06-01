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

# get train data
invalidData = data.getCSVFeatures()
# validData = None

# filter data
filteredData = []
for data in invalidData:
    entry = np.array(data.values())
    filteredData.append((entry, 0))
# for data in validData:
#     entry = np.array(data.values())
#     filteredData.append((entry, 1))

# partition data
invalidSplit = math.ceil(len(invalidData) * 0.85)
invalidTrain = invalidData[:invalidSplit]
invalidTest = invalidData[invalidSplit:]
# validSplit = math.ceil(len(validData) * 0.85)
# validTrain = validData[:validSplit]
# validTest = validData[validSplit:]


