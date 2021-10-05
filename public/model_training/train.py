'''
    @author Zhenke Chen
    @date 05/10/2021

    Construct and then train the CNN model with keras package
'''

# import the required packages
import numpy as np
import matplotlib.pyplot as plt

# import the keras package for CNN model construction
import keras
from keras import regularizers
from keras.models import Sequential

# define the CNN model hyperparameters
ACTIVATION = "relu"

#define the parameters for training
EPOCHS = 100


class TrainModel():

    def construct_model():

        '''
            Construct the CNN model based on the given model hyperparameters with the keras package
        
            Keyword arguments:
            
        '''

        # apply keras to construct the model
        model = Sequential()

        model.add()

        model.compile()

        return model


    def train_model( model, ):

        '''
            Train the CNN model based on the given training parameters with the keras package
        
            Keyword arguments:
            
        '''

        training_status = model.fit()

        return training_status
