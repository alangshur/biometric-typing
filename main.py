# ███╗   ███╗ █████╗ ██╗███╗   ██╗
# ████╗ ████║██╔══██╗██║████╗  ██║
# ██╔████╔██║███████║██║██╔██╗ ██║
# ██║╚██╔╝██║██╔══██║██║██║╚██╗██║
# ██║ ╚═╝ ██║██║  ██║██║██║ ╚████║
# ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝

from data import data
import numpy as np
import math
from models import log_reg
import random, sys
mode = sys.argv[1]

# get train data
validData, invalidData, phi = data.generateAllFeatureSets(mode)

# filter data
filteredDataV, filteredDataIV, ordering = [], [], list(validData[0].keys())
for datum in invalidData:
    values = []
    for key in ordering: values.append(datum[key])
    entry = np.array(values)
    filteredDataIV.append((entry, 0))
for datum in validData:
    weightSize = len(datum)
    values = []
    for key in ordering: values.append(datum[key])
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
model = log_reg.LogisticRegression(filteredTrainData, filteredTestData, T = 0.5, wSize = weightSize)
model.trainLR(1000, 0.01, 'adam')

# test data
model.testLR()

# live demo
def liveDemo(model, phi):
    while True:
        try:
            while True:
                print("Please enter password three times:\n")
                attempt1 = data.requestPasswordAttempt(phi)
                attempt2 = data.requestPasswordAttempt(phi)
                attempt3 = data.requestPasswordAttempt(phi)
                model.testDemo(attempt1, attempt2, attempt3, ordering)
        except: 
            print("\n\n\n\nCaught error. Would you like to continue?")
            response = ''
            while response != 'Yes' and response != 'No':
                response = input('(Yes/No): ')
            if response == 'No': break
if mode == 'demo':
    liveDemo(model, phi)
    
