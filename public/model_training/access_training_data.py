'''
    @author Zhenke Chen
    @date 05/10/2021

    Transfer the training data into the form which can be used by the model
'''


# import the required packages
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import pickle


class AccessTrainingData():

    def __init__( self ):
        pass

    def load_data( self ):

        '''
            Access the training data and prepare them for model training

            Keyword arguments:
            
        '''

        # get access to the data (now is for testing)
        data_x = np.array([[1, 2], [3, 4]])
        data_y = np.array([[1, 2], [3, 4]])

        return data_x, data_y