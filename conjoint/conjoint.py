# Conjoint Analysis for the InitialView Case Competition

'''
General Notes:
R respondents, T tasks, C concepts 
'''

import numpy as np
import matplotlib.pyplot as plt


filename = ''

class ConjointModel():
    def __init__(self):
        '''
        utilities: the values Ux of all the ideas of the concepts. 
        '''

    def read_data(self, filename):
        # read data from file
        pass


    def get_probability(self):
        # get the probability of choosing a concept
        pass


    def estimate(self):
        # max likelihood
        pass


if __name__ == "__main__":
    print("Conjoint Analysis")
    Model = ConjointModel()
    Model.read_data(filename)
    Model.estimate()

