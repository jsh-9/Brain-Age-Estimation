from keras.models import  Sequential
from keras.layers import *


def model_2D(Dense_128_name="layer_128", Dense_last_name="last_layer"):
    model = Sequential()
    model.add(Conv2D(16, kernel_size=(3, 3), input_shape=(80, 80, 80)))
    model.add(LeakyReLU())
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(32, kernel_size=(3, 3)))
    model.add(LeakyReLU())
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(64, kernel_size=(3, 3)))
    model.add(LeakyReLU())
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(128, kernel_size=(3, 3)))
    model.add(LeakyReLU())
    model.add(Conv2D(256, kernel_size=(3, 3)))
    model.add(LeakyReLU())
    model.add(Conv2D(512, kernel_size=(3, 3)))
    model.add(LeakyReLU())
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(128, name=Dense_128_name))
    model.add(LeakyReLU())
    model.add(Dense(1, name=Dense_last_name))
    model.add(LeakyReLU())
    return model

def model_3D(Dense_128_name="layer_128", Dense_last_name="last_layer"):
    model = Sequential()
    model.add(Conv3D(16, kernel_size=(3, 3, 3), input_shape=(80, 80, 80, 1)))
    model.add(LeakyReLU())
    model.add(MaxPooling3D(pool_size=(2, 2, 2)))
    model.add(Conv3D(32, kernel_size=(3, 3, 3)))
    model.add(LeakyReLU())
    model.add(MaxPooling3D(pool_size=(2, 2, 2)))
    model.add(Conv3D(64, kernel_size=(3, 3, 3)))
    model.add(LeakyReLU())
    model.add(MaxPooling3D(pool_size=(2, 2, 2)))
    model.add(Conv3D(128, kernel_size=(3, 3, 3)))
    model.add(LeakyReLU())
    model.add(Conv3D(256, kernel_size=(3, 3, 3)))
    model.add(LeakyReLU())
    model.add(Conv3D(512, kernel_size=(3, 3, 3)))
    model.add(LeakyReLU())
    model.add(MaxPooling3D(pool_size=(2, 2, 2)))
    model.add(Flatten())
    model.add(Dense(128, name=Dense_128_name))
    model.add(LeakyReLU())
    model.add(Dense(1 , name=Dense_last_name))
    model.add(LeakyReLU())
    return model