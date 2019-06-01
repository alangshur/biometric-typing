import collections, math, random
import numpy as np

def sigmoid(z):
    return 1 / (1 + math.exp(-1 * z))

class LogisticRegression:

    def __init__(self, train, test, wSize):
        self.train = train
        self.test = test
        self.w = np.array([0] * len(wSize))
        self.wSize = wSize

    def SGA(self, epochs, eta = 0.001, b1 = 0.9, b2 = 0.999, e = 10e-8):

        m = np.array([0] * len(self.wSize))
        v = np.array([0] * len(self.wSize))

        it = 1
        for _ in range(epochs):

            random.shuffle(self.train)

            for data in self.train:

                if it % 10 == 0: print("Epoch {} of SGD.".format(it))
                x, y = data

                # update ADAM hyperparameters
                grad = x * (y - sigmoid(np.dot(self.w, x)))
                m = b1 * m + (1 - b1) * grad
                v = b2 * v + (1 - b2) * np.square(grad)
                m_hat = m * (1 / (1 - (b1 ** it)))
                v_hat = v * (1 / (1 - (b2 ** it)))

                # update weights
                update = eta * m_hat * np.reciprocal(np.sqrt(v_hat) + e)
                self.w = self.w + update
                it += 1
        
    def run(self, epochs, eta):
        # self.SGA(epochs, eta)
        pass

        


        

