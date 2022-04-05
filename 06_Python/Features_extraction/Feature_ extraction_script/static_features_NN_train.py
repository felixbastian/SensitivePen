import torch
from torch import nn
from torch.utils.data import DataLoader
from sklearn.datasets import load_boston
from sklearn.preprocessing import StandardScaler
import numpy as np

from keras.layers import Conv1D, Dense, Dropout, Input, Concatenate, GlobalMaxPooling1D
from keras.models import Model
import tensorflow.keras.backend as K

#this base model is one branch of the main model
#it takes a time series as an input, performs 1-D convolution, and returns it as an output ready for concatenation

def get_base_model(input_len, fsize):
    #the input is a time series of length n and width 19
    input_seq = Input(shape=(input_len, 19))
    #choose the number of convolution filters
    nb_filters = 10
    #1-D convolution and global max-pooling
    convolved = Conv1D(nb_filters, fsize, padding="same", activation="tanh")(input_seq)
    processed = GlobalMaxPooling1D()(convolved)
    #dense layer with dropout regularization
    compressed = Dense(50, activation="tanh")(processed)
    compressed = Dropout(0.3)(compressed)
    model = Model(inputs=input_seq, outputs=compressed)
    return model

#this is the main model
#it takes the original time series and its down-sampled versions as an input,
# and returns the result of classification as an output
#def main_model(inputs_lens = [512, 1024, 3480], fsizes = [8,16,24]):
# def main_model(inputs, fsizes=[8, 16, 24]):
#     #the inputs to the branches are the original time series, and its down-sampled versions
#     # input_smallseq = Input(shape=(inputs_lens[0], 19))
#     # input_medseq = Input(shape=(inputs_lens[1] , 19))
#     input_origseq = K.constant(inputs)
#     #the more down-sampled the time series, the shorter the corresponding filter
#     # base_net_small = get_base_model(inputs_lens[0], fsizes[0])
#     # base_net_med = get_base_model(inputs_lens[1], fsizes[1])
#     base_net_original = get_base_model(inputs_lens[2], fsizes[2])
#     # embedding_small = base_net_small(input_smallseq)
#     # embedding_med = base_net_med(input_medseq)
#     embedding_original = base_net_original(input_origseq)
#     #concatenate all the outputs
#
#     merged = Concatenate()([embedding_original])
#     #merged = Concatenate()([embedding_small, embedding_med, embedding_original])
#     out = Dense(1, activation='sigmoid')(merged)
#     model = Model(inputs=[input_origseq], outputs=out)
#     #model = Model(inputs=[input_smallseq, input_medseq, input_origseq], outputs=out)
#     return model

def main_model(inputs, fsizes=[8, 16, 24]):
    #the inputs to the branches are the original time series, and its down-sampled versions

    input_origseq = K.constant(inputs)
    print(input_origseq)
    #
    # base_net_original = get_base_model(inputs_lens[2], fsizes[2])
    #
    # embedding_original = base_net_original(input_origseq)
    # #concatenate all the outputs
    #
    # merged = Concatenate()([embedding_original])
    # #merged = Concatenate()([embedding_small, embedding_med, embedding_original])
    # out = Dense(1, activation='sigmoid')(merged)
    # model = Model(inputs=[input_origseq], outputs=out)
    # #model = Model(inputs=[input_smallseq, input_medseq, input_origseq], outputs=out)
    # model=0
    return model





def pipeline(data):

    # Set fixed random number seed
    torch.manual_seed(42)

    # Load Boston dataset
    X,y = data.loc[:,1], data.loc[:,2]
    X = np.array(X)
    y = np.array(y)

    #main_model(X)

    #scale data
    # X = StandardScaler().fit_transform(X)
    #
    # x = torch.from_numpy(X)
    # y= torch.from_numpy(y)
    #X, y = load_boston(return_X_y=True)

    print(X)
    print(y.shape)

    print(X[0].shape)

