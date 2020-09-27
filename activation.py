import numpy as np

class Activation():
    @staticmethod
    def relu(matrix):
        for row in range(len(matrix)):
            for col in range(len(matrix[0])):
                if matrix[row][col] < 0:
                    matrix[row][col] = 0
        return matrix

    @staticmethod
    def sigmoid(matrix):
        return 1/(1 + np.exp(-matrix))
    
    @staticmethod
    def tanh(matrix):
        return np.tanh(matrix)