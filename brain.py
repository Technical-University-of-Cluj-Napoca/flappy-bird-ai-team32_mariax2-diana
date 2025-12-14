import random
import math

class Brain:
    def __init__(self, weights=None):
        #4 weights: i0, i1, i2, bias
        if weights is None:
            self.weights=[random.uniform(-1, 1) for _ in range(4)]
        else:
            self.weights=weights[:]

    def sigmoid(self, x):
        return 1/(1 + math.exp(-x))

    def forward(self, inputs):
        #inputs=[i0, i1, i2, bias]
        total=0
        for w, i in zip(self.weights, inputs):
            total+=w*i
        return self.sigmoid(total)

    def decide(self, inputs, threshold=0.5):
        output=self.forward(inputs)
        return output>threshold

    def copy(self):
        return Brain(self.weights)

    def mutate(self, rate=0.1, strength=0.5):
        for i in range(len(self.weights)):
            if random.random()<rate:
                self.weights[i]+=random.uniform(-strength, strength)
