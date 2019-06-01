import collections, math, random
import numpy as np

def sigmoid(z):
    return 1 / (1 + math.exp(-1 * z))

def transpose(a, b):
    assert len(a) == len(b)
    result = 0
    for ea, eb in zip(a, b):
        result += ea * eb
    return result

class LogisticRegression:

    def __init__(self, train, test, wSize):
        self.train = train
        self.test = test
        self.w = np.array([0] * len(wSize))

    def SGA(self, epochs, eta):
        it = 1
        for _ in range(epochs):
            random.shuffle(self.train)
            for data in self.train:
                if it % 1000 == 0: print("Epoch {} of SGD.".format(it))
                x, y = data

                # update weights
                grad = x * (y - sigmoid(np.dot(self.w, x)))
                grad *= eta
                self.w = np.add(self.w, grad)
                it += 1
        
    def run(self, epochs, eta):
        self.SGA(epochs, eta)

        


        

