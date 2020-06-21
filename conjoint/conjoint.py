# Conjoint Analysis for the InitialView Case Competition

'''
General Notes:
R respondents (unknown)
T tasks (15)
C concepts (3 or 4)
4 attributes: theme color icon font
Size of vector x and w: 4+4+4+4 = 16
'''

import numpy as np
import pandas as pd
from scipy.optimize import minimize


def index_to_array(pic_index):
    # index of 4 attributes
    pic_index = pic_index - 1
    attribute1 = int(pic_index / 64)
    pic_index = pic_index % 64
    attribute2 = int(pic_index / 16)
    pic_index = pic_index % 16
    attribute3 = int(pic_index / 4)
    pic_index = pic_index % 4
    attribute4 = pic_index
    res = np.zeros(15)
    res[attribute1] = 1
    res[3 + attribute2] = 1
    res[7 + attribute3] = 1
    res[11 + attribute4] = 1
    return res


class ConjointModel():
    def __init__(self):
        """
        utilities: the values Ux of all the ideas of the concepts.
        """
        self.num_total_attributes = 15
        self.num_tasks = 32
        self.num_concepts = 3
        self.question = None
        self.question_vec = None
        self.ans = None
        self.data = None
        self.Model = None
        self.res = None
        self.question_mat = None

    def read_questions(self, filename):
        df = pd.read_csv(filename)
        self.question = df.to_numpy()
        print(self.question.shape)
        return self.question

    def build_question_vector(self):
        qvec = [[] for j in range(self.question.shape[0])]
        for i in range(self.question.shape[0]):
            qvec[i] = [index_to_array(self.question[i][j])
                       for j in range(self.question.shape[1])]
        self.question_vec = np.array(qvec)
        return self.question_vec

    def read_data(self, filename_format):
        self.build_question_vector()
        data_vec_all = []
        data_index_all = []
        question_vec = []
        for i in range(4):
            df = pd.read_csv(filename_format.format(i))
            nda = df.to_numpy()
            raw_data = np.array(nda[:, 8:40], dtype=np.int)
            print(raw_data.shape)
            data_vec = [[] for j in range(raw_data.shape[0])]
            data_index = [[] for j in range(raw_data.shape[0])]
            for j in range(raw_data.shape[0]):
                question_vec.append(self.question_vec[i*32:(i+1)*32])
                for k in range(raw_data.shape[1]):
                    pic_index = self.question[i * 32 + j][raw_data[j][k] - 1]
                    data_vec[j].append(index_to_array(pic_index))
                    data_index[j].append(pic_index)
            data_vec_all.extend(data_vec)
            data_index_all.extend(data_index)
        self.data = np.array(data_index_all)
        self.ans = np.array(data_vec_all)
        self.question_mat = np.array(question_vec)
        return self.ans

    def log_likelihood(self, w):
        s = 0
        for i in range(self.ans.shape[0]):
            for j in range(self.ans.shape[1]):
                xrt = self.question_mat[i][j]
                dots = np.array([np.dot(xrt[k], w) for k in range(self.num_concepts)])
                exp_dots = np.exp(dots)
                sum_dots = np.log(exp_dots.sum())
                s += np.dot(self.ans[i][j], w) - sum_dots
        return -s

    def estimate(self):
        x0 = np.ones(self.num_total_attributes) / self.num_total_attributes
        self.res = minimize(self.log_likelihood, x0, method='Nelder-Mead')
        return self.res


if __name__ == "__main__":
    print("Conjoint Analysis")
    Model = ConjointModel()
    Model.read_questions('question.csv')
    Model.read_data('data{}.csv')
    Model.estimate()
    print(Model.res.x)
