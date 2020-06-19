# Conjoint Analysis for the InitialView Case Competition

'''
General Notes:
R respondents, T tasks, C concepts 
'''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


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


    def estimate(self, estimator='max_likelihood'):
        if estimator == 'max_likelihood':
            self.max_likelihood()
        elif estimator == 'logistic_regression':
            self.logistic_regression()
        else:
            print("Invalid estimation method.")
        return

    
    def max_likelihood(self):
        pass


    def logistic_regression(self):
        pass


    def generate_result(self):
        pass


    def generate_graph(self):
        pass



if __name__ == "__main__":
    print("Conjoint Analysis")
    Model = ConjointModel()
    Model.read_data(filename)
    Model.estimate()
    Model.generate_graph()


