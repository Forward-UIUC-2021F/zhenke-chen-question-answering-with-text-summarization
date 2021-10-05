'''
    @author Zhenke Chen
    @date 05/10/2021

    Construct and then train the CNN model with keras package
'''

# import the necessary fucntions from other files
from access_training_data import AccessTrainingData

# import the required packages
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf


# import the keras package for CNN model construction
from tensorflow import keras
from keras.models import Sequential
from keras import optimizers
from keras import losses
from keras import metrics
from keras.layers import Dense, Activation
from keras import regularizers, losses


# define the CNN model hyperparameters
ACTIVATION = "relu"
OPTIMIZOR = optimizers.Adadelta
LOSS_FUNCTION = losses.binary_crossentropy
METRICES = metrics.mae
LOSS_WEIGHTS = None
SAMPLE_WEIGHT_MODE = None
WEIGHTED_METRICS = None
TARGET_TENSORS = None


# define the hyperparameters for training
EPOCHS = 100
BATCH_SIZE = 128


class TrainModel():

    def __init__( self ):
        pass

    def construct_model():

        '''
            Construct the CNN model based on the given model hyperparameters with the keras package
        
            Keyword arguments:
            
        '''

        # apply keras to construct the model
        model = Sequential()

        model.add()

        model.add()

        model.add()

        model.compile(
            optimizer = OPTIMIZOR,          # define the optimizer
            loss = LOSS_FUNCTION,           # define the loss function
            metrices = METRICES,            # define the performance metrices
            loss_weights = LOSS_WEIGHTS,    

        )

        return model


    def train_model( model, ):

        '''
            Train the CNN model based on the given training hyperparameters with the keras package
        
            Keyword arguments:
            
        '''

        training_status = model.fit()

        return training_status


def main():

    return 0