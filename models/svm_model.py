import collections
import numpy as np
import importlib

importlib.import_module('../data/data.py')

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

feat = getPhatPheatures()

class SVMClassification:

    def __init__(self, train, test, T):
        self.trainData = train
        self.testData = test
        self.threshold = T

    def train(self):
        x_pos = np.array()


        

