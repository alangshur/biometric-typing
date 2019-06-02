#██╗      ██████╗  ██████╗ ██╗███████╗████████╗██╗ ██████╗
#██║     ██╔═══██╗██╔════╝ ██║██╔════╝╚══██╔══╝██║██╔════╝
#██║     ██║   ██║██║  ███╗██║███████╗   ██║   ██║██║
#██║     ██║   ██║██║   ██║██║╚════██║   ██║   ██║██║
#███████╗╚██████╔╝╚██████╔╝██║███████║   ██║   ██║╚██████╗
#╚══════╝ ╚═════╝  ╚═════╝ ╚═╝╚══════╝   ╚═╝   ╚═╝ ╚═════╝
#
#██████╗ ███████╗ ██████╗ ██████╗ ███████╗███████╗███████╗██╗ ██████╗ ███╗   ██╗
#██╔══██╗██╔════╝██╔════╝ ██╔══██╗██╔════╝██╔════╝██╔════╝██║██╔═══██╗████╗  ██║
#██████╔╝█████╗  ██║  ███╗██████╔╝█████╗  ███████╗███████╗██║██║   ██║██╔██╗ ██║
#██╔══██╗██╔══╝  ██║   ██║██╔══██╗██╔══╝  ╚════██║╚════██║██║██║   ██║██║╚██╗██║
#██║  ██║███████╗╚██████╔╝██║  ██║███████╗███████║███████║██║╚██████╔╝██║ ╚████║
#╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝


import collections, math, random
import numpy as np

def sigmoid(z, s = 1, d = 0):
    return 1 / (1 + math.exp(-1 * s * z + d))

class LogisticRegression:

    def __init__(self, train, test, T, wSize):
        self.train = train
        self.test = test
        self.w = np.array([0] * len(wSize))
        self.wSize = wSize
        self.d = -1 * math.log(T / (1 - T))
        self.trained = False

    def SGA(self, epochs, eta = 0.001, b1 = 0.9, b2 = 0.999, e = 10e-8, s = 1):
        m = np.array([0] * len(self.wSize))
        v = np.array([0] * len(self.wSize))

        it = 1
        for _ in range(epochs):
            random.shuffle(self.train)
            for data in self.train:
                if it % 10 == 0: print("Epoch {} of SGD.".format(it))
                x, y = data

                # update ADAM hyperparameters
                grad = x * (y - sigmoid(np.dot(self.w, x), s, self.d))
                m = b1 * m + (1 - b1) * grad
                v = b2 * v + (1 - b2) * np.square(grad)
                m_hat = m / (1 - np.power(b1, it))
                v_hat = v / (1 - np.power(b2, it))

                # update weights
                update = eta * m_hat / (np.sqrt(v_hat) + e)
                self.w = self.w + update
                it += 1
        self.trained = True
        
    def trainLR(self, epochs, eta):
        self.SGA(epochs, eta)

    def testLR(self, s = 1):
        assert self.trained == True
        totalV, totalIV, corrV, corrIV = 0, 0, 0, 0
        predictV, predictIV = 0, 0
        for data in self.test:
            x, y = data
            res = np.dot(self.w, x)
            prediction = int(res > 0)
            if prediction == 1: predictV += 1
            elif prediction == 0: predictIV += 1
            if y == 0:
                totalIV += 1
                if prediction == 0: corrIV += 1
            elif y == 1:
                totalV += 1
                if prediction == 1: corrV += 1
        accuracy = (corrV + corrIV) / (totalV + totalIV)
        precision = corrV / predictV
        recall = corrV / (corrV + (predictIV - corrIV))
        print("Total Accuracy: {}".format(accuracy))
        print("Precision: {}".format(precision))
        print("Recall: {}".format(recall))
        print("False-positive rate: {}".format((predictV - corrV) / predictIV))
        print("F1 Score: {}".format(2 * (precision * recall) / (precision + recall)))


        


        

