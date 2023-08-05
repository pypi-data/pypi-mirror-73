

from keras.backend import sigmoid 
from keras.utils.generic_utils import get_custom_objects 
from keras.layers import Activation

from keras.layers import Dense

from keras.models import Sequential


def swish(x, beta = 1): 
    get_custom_objects().update({'swish': Activation(swish)})
    return (x * sigmoid(beta * x))

