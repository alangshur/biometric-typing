import collections
import numpy as np

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def plotSigmoid():
    plt.plot(np.arange(-5, 5, 0.1), sigmoid(np.arange(-5, 5, 0.1))) 
    plt.title('Visualization of the Sigmoid Function')
    plt.show() 

class SVMClassification:

    def __init__(self, train, test, T):
        self.trainData = train
        self.testData = test
        self.threshold = T

    def train(self):
        x_pos = np.array()


        

