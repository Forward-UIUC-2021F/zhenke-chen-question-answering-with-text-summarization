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
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Dense, Flatten, Dropout
from keras import regularizers, losses
from keras.utils import plot_model


# define the CNN model hyperparameters
ACTIVATION_1 = "relu"
ACTIVATION_2 = "softmax"
L_2 = 0.01
FILTERS_NUM = 400
WINDOW_SIZE = (3, 300)
STRIDE_LEN = 1
PADDING = "valid"
DATA_FORMAT = "channels_first"
POOL_SIZE = (FILTERS_NUM, 1)
DROP_OUT_RATE = 0.5
OPTIMIZOR = optimizers.Adadelta
LOSS_FUNCTION = losses.binary_crossentropy
METRICES = metrics.mae
LOSS_WEIGHTS = None
SAMPLE_WEIGHT_MODE = None
WEIGHTED_METRICS = None
TARGET_TENSORS = None


# define the hyperparameters for training
EPOCHS = 1000
BATCH_SIZE = 128
VERBOSE = 1
VALID_SPLIT = 0.2
SHUFFLE = False

class TrainModel():

    def __init__( self ):
        pass

    def construct_model( self, shape ):

        '''
            Construct the CNN model based on the given model hyperparameters with the keras package
        
            Keyword arguments:
            shape -- the shape of input training data

            p.s. all other hyperparameters for CNN model are defined above
        '''

        # apply keras to construct the model
        model = Sequential()

        # add a 2-D convolutional layer
        model.add(Conv2D(
            filters = FILTERS_NUM,                   # define the dimension of output space
            input_shape = shape,                     # define the size of the input
            activation = ACTIVATION_1,               # define the activation function
            kernal_size = WINDOW_SIZE,               # define the size of convolutional window
            strides = STRIDE_LEN,                    # define the stride length    
            padding = PADDING,                       # define the type of padding
            data_format = DATA_FORMAT                # define the order of input dimensions
        ))

        # add a max-pooling layer
        model.add(MaxPooling2D(
            pool_size = POOL_SIZE                    # define the size of max pooling
        ))

        # flatten the input
        model.add(Flatten(
            data_format = None                       # define the order of input dimensions
        ))

        # randomly set the input to 0 to prevent overfitting
        model.add(Dropout(
            rate = DROP_OUT_RATE                     # define the drop out rate
        ))

        # apply the l_2 norm regularizer
        model.add(Dense(
            activation = ACTIVATION_2,               # define the activation function
            kernel_regularizer = regularizers.l2(L_2)# define the regularizer
        ))

        # construct the model with the added layer above
        model.compile(
            optimizer = OPTIMIZOR,                   # define the optimizer
            loss = LOSS_FUNCTION,                    # define the loss function
            metrices = METRICES,                     # define the performance metrices
            loss_weights = LOSS_WEIGHTS,             # define the weights of losses from different models
            sample_weight_mode = SAMPLE_WEIGHT_MODE, # define as "temporal" if 2-D weights needed
            weighted_metrics = WEIGHTED_METRICS,     # the metrics with sample weights
            target_tensors = TARGET_TENSORS          # define the own target tensors if needed
        )

        return model


    def train_model( model, training_data, target_data ):

        '''
            Train the CNN model based on the given training hyperparameters with the keras package
        
            Keyword arguments:
            model -- the pre-set model based on the output from function construct_model()
            training_data -- the training data
            target_data -- the target data

            p.s. all other hyperparameters for training are defined above
        '''

        # train the model
        training_status = model.fit(
            x = training_data,                       # define the training data with numpy array
            y = target_data,                         # define the target data with numpy array
            batch_size = BATCH_SIZE,                 # define the batch size
            epochs = EPOCHS,                         # define the number of training epochs
            verbose = VERBOSE,                       # define the training log display mode
            validation_split = VALID_SPLIT,          # define the ratio of dataset as validation set
            shuffle = SHUFFLE                        # define if shuffling the data inside a batch
        )

        return training_status


def main():

    '''
        There are three steps for the model training process:
        1. Construct the CNN model with pre-set hyperparameters
        2. Train the model with pre-set training hyperparameters
        3. Visualize the training process and result

        Keyword arguments:
        None

        P.S. The hyperparameters for CNN model training are set above. And the training data is from the file access_training_data
    '''

    # access the training data and target data from access_training_data
    access_data = AccessTrainingData()
    x_data, y_data = access_data.load_data()
    data_size = (
        1,
        x_data.shape[2],
        x_data.shape[3]
    )

    model_training = TrainModel()

    # construct the CNN model with pre-set hyperparameters
    CNN_model = model_training.construct_model( data_size )

    # train the CNN model with pre-set training hyperparameters
    training_status = model_training.train_model( CNN_model, x_data, y_data )

    # save the model
    CNN_model.model.save('./models/CNN_model.h5')

    # show the figure of the model
    plot_model(
        model = CNN_model,
        show_shapes = True,
        show_layer_names = True,
        expand_dim = False,
        dpi = 300,
        to_file = "./figures/model.png"
    )

    # plot the model accuracy
    plt.plot(training_status.history['acc'])
    plt.plot(training_status.history['val_acc'])
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.savefig("./figures/model_accuracy.png", dpi = 300)
    plt.show()

    # plot the model loss
    plt.plot(training_status.history['loss'])
    plt.plot(training_status.history['val_loss'])
    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.savefig("./figures/model_loss.png", dpi = 300)
    plt.show()

    # plot the model mean absolute error
    plt.plot(training_status.history['mean_absolute_error'])
    plt.plot(training_status.history['val_mean_absolute_error'])
    plt.title('Model mean absolute error')
    plt.ylabel('MAE')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.savefig("./figures/model_mae", dpi = 300)
    plt.show()

    return

if __name__ == "__main__":
    main()