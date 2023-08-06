from tensorflow.python import keras
from keras.models import Sequential, Model
from keras.layers import Dense, Input, Flatten, Dropout, Activation
from keras.layers import concatenate, Convolution1D, MaxPooling1D, GlobalMaxPooling1D, Embedding, Dropout
from keras.layers import Flatten, Dense, Dropout, AlphaDropout, ThresholdedReLU, Convolution1D, ZeroPadding1D, Activation, MaxPooling1D, SpatialDropout1D, Input
from keras.layers import GlobalMaxPooling1D, concatenate, LSTM, Bidirectional,BatchNormalization

from keras import regularizers

import numpy as np


def cnn_model(nb_classes, drop_out=0, model_name=None, input_dims=config.NB_WORDS, output_dims=config.EMBEDDING_DIM, input_len=config.MAX_LEN, filters=64, kernel_size=3, dense_layer_size=100):
    model = Sequential()


    model.add(Embedding(
                input_dim=input_dims,
                output_dim=output_dims,
                input_length=input_len))

    model.add(Convolution1D(
                filters=filters,
                kernel_size=kernel_size,
                padding='same',
                activation='relu'))

    model.add(MaxPooling1D())
    model.add(Flatten())
    if drop_out>0:
        model.add(Dropout(0.2))
    model.add(Dense(
                dense_layer_size,
                activation='relu'))
    model.add(Dense(
                nb_classes,
                kernel_regularizer=regularizers.l2(0.001),
                activation='softmax'))
    model.name = 'BaseCNN'
    if model_name:
        model.name=model_name

    print(model.summary())
    return model


def multilayer_multifilter_conv(nb_class, model_name=None, input_dims=config.NB_WORDS, output_dims=config.EMBEDDING_DIM, input_len=config.MAX_LEN, filters=64, dense_layer_size=100):

    model = Sequential()

    model.add(Embedding(input_dims, output_dim=output_dims, input_length=input_len))

    graph_in = Input(shape=(config.NB_WORDS, 100))

    convolutions = []
    for filter_size in range(3, 6):
        x = Convolution1D(
            filters,
            filter_size,
            padding='same',
            activation='relu')(graph_in)
        convolutions.append(x)

    graph_out = concatenate(convolutions, axis=1)
    graph_out = GlobalMaxPooling1D()(graph_out)
    graph = Model(graph_in, graph_out)

    model.add(graph)
    model.add(Dense(dense_layer_size, activation='relu'))
    model.add( Dense(  nb_class, activation='softmax'))

    model.name = 'MultiLayerMultiFilterCNN'
    if model_name:
        model.name=model_name

    print(model.summary())
    return model


def multilayer_multifilter_embeddings_cnn(nb_class,emb_matrix, trainable=False, model_name=None, input_dims=config.NB_WORDS, output_dims=config.EMBEDDING_DIM, input_len=config.MAX_LEN, filters=64, dense_layer_size=100):
    graph_in = Input(shape=(input_dims + 1, 100))

    convs = []
    for filter_size in range(2, 5):
        x = Convolution1D(
            filters,
            filter_size,
            padding='same',
            activation='relu')(graph_in)
        convs.append(x)

    graph_out = concatenate(convs, axis=1)
    graph_out = GlobalMaxPooling1D()(graph_out)
    graph = Model(graph_in, graph_out)

    model = Sequential([Embedding(input_dims + 1,
                                  output_dims,
                                  weights=[emb_matrix],
                                  trainable=trainable,
                                  input_length=input_len),
                        graph,
                        Dense(dense_layer_size,
                              activation='relu'),
                        Dense(nb_class,
                              activation='softmax')])
    model.name = 'MultiLayerMultiFilterStaticEmbeddingsCNN'
    if model_name:
        model.name=model_name
    print(model.summary())
    return model

def single_channel_multipooling_cnn(nb_class, emb_matrix, trainable=True, model_name=None, kernel_size=5, input_dims=config.NB_WORDS, output_dims=config.EMBEDDING_DIM, input_len=config.MAX_LEN, filters=128, dense_layer_size=100):
    text_seq_input = Input(shape=(input_len,), dtype='int32')
    text_embedding = Embedding(input_dims + 1,
                               output_dims,
                               weights=[emb_matrix],
                               trainable=trainable,
                               input_length=input_len)(text_seq_input)

    filter_sizes = [3, 4, 5]
    convs = []
    for filter_size in filter_sizes:
        l_conv = Convolution1D(
            filters=filters,
            kernel_size=filter_size,
            padding='same',
            activation='relu')(text_embedding)
        l_pool = MaxPooling1D(filter_size)(l_conv)
        convs.append(l_pool)

    merge = concatenate(convs, axis=1)
    convol = Convolution1D(filters, kernel_size, activation='relu')(merge)
    pool1 = GlobalMaxPooling1D()(convol)
    dense = Dense(dense_layer_size, activation='relu', name='Dense')(pool1)
    out = Dense(nb_class, activation='softmax')(dense)
    model = Model(
        inputs=[text_seq_input],
        outputs=out,
        name="KimSingleChannelCNN")

    if model_name:
        model.name=model_name

    print(model.summary())
    return model


def multiple_channel_multipooling_cnn(nb_class, emb_matrices, trainable=False, model_name=None, kernel_size=5, input_dims=config.NB_WORDS, input_len=config.MAX_LEN, filters=128, dense_layer_size=100):
    text_seq_input = Input(shape=(input_len,), dtype='int32')

    text_embeddings=[]
    for emb_matrix in emb_matrices:
        output_dims=emb_matrix.shape[1]
        text_embeddings.append(Embedding(
            input_dims + 1,
            output_dims,
            weights=[emb_matrix],
            input_length=input_len,
            trainable=trainable)(text_seq_input))
    filter_sizes = [3, 4, 5]
    convs = []

    for text_embedding in text_embeddings:
        for filter_size in filter_sizes:
            l_conv = Convolution1D(
                filters=filters,
                kernel_size=filter_size,
                padding='same',
                activation='relu')(text_embedding)
            l_pool = MaxPooling1D(filter_size)(l_conv)
            convs.append(l_pool)
    merge = concatenate(convs, axis=1)
    convol = Convolution1D(filters, kernel_size, activation='relu')(merge)
    pool1 = GlobalMaxPooling1D()(convol)
    dense = Dense(dense_layer_size, activation='relu', name='last_but_one')(pool1)
    out = Dense(nb_class, activation='softmax')(dense)
    model = Model(
        inputs=[text_seq_input],
        outputs=out,
        name="KimMultipleChannelCNN")
    if model_name:
        model.name=model_name

    print(model.summary())
    return model


def dynamic_k_max_pooling_cnn(nb_class, emb_matrix, trainable=False, model_name=None, kernel_size=5, input_dims=config.NB_WORDS, output_dims=config.EMBEDDING_DIM, input_len=config.MAX_LEN, filters=64):
    model = Sequential(
        [
            Embedding(
                input_dims + 1,
                output_dims,
                weights=[emb_matrix],
                input_length=input_len,
                trainable=trainable),
            ZeroPadding1D(
                (49,
                 49)),
            Convolution1D(
                filters,
                50,
                padding="same"),
            KMaxPooling(
                k=kernel_size,
                axis=1),
            Activation("relu"),
            ZeroPadding1D(
                (24,
                 24)),
            Convolution1D(
                filters,
                25,
                padding="same"),
            Folding(),
            KMaxPooling(
                k=kernel_size,
                axis=1),
            Activation("relu"),
            Flatten(),
            Dense(
            nb_class,
                activation="softmax")])
    model.name = 'KalchbrennerDynamicCNN'
    if model_name:
        model.name=model_name

    print(model.summary())
    return model


def multichannel_variable_cnn(nb_class, emb_matrices, trainable=False, model_name=None, input_dims=config.NB_WORDS, input_len=config.MAX_LEN, filters=128, dense_layer_size=100):
    text_seq_input = Input(shape=(input_len,), dtype='int32')

    text_embeddings=[]
    for emb_matrix in emb_matrices:
        output_dims=emb_matrix.shape[1]
        text_embeddings.append(Embedding(
            input_dims + 1,
            output_dims,
            weights=[emb_matrix],
            input_length=input_len,
            trainable=trainable)(text_seq_input))

    k_top = 4

    layer_1 = []
    for text_embedding in text_embeddings:
        conv_pools = []
        filter_sizes = [3, 5]
        for filter_size in filter_sizes:
            l_zero = ZeroPadding1D(
                (filter_size - 1, filter_size - 1))(text_embedding)
            l_conv = Convolution1D(
                filters=filters,
                kernel_size=filter_size,
                padding='same',
                activation='tanh')(l_zero)
            l_pool = KMaxPooling(k=28, axis=1)(l_conv)
            conv_pools.append((filter_size, l_pool))
            layer_1.append(conv_pools)

    last_layer = []
    for layer in layer_1:  # no of embeddings used
        for (filter_size, input_feature_maps) in layer:
            l_zero = ZeroPadding1D(
                (filter_size - 1, filter_size - 1))(input_feature_maps)
            l_conv = Convolution1D(
                filters=filters,
                kernel_size=filter_size,
                padding='same',
                activation='tanh')(l_zero)
            l_pool = KMaxPooling(k=k_top, axis=1)(l_conv)
            last_layer.append(l_pool)

    l_merge = concatenate(last_layer, axis=1)
    l_flat = Flatten()(l_merge)
    l_dense = Dense(dense_layer_size, activation='relu')(l_flat)
    l_out = Dense(nb_class, activation='softmax')(l_dense)
    model = Model(inputs=[text_seq_input], outputs=l_out)
    model.name = 'MultiChannelVariableCNN'
    if model_name:
        model.name=model_name

    print(model.summary())
    return model


def multigroup_normconstraint_cnn(nb_class, emb_matrices, trainable=False, model_name=None, input_dims=config.NB_WORDS, input_len=config.MAX_LEN, filters=128, dense_layer_size=100):
    text_seq_input = Input(shape=(input_len,), dtype='int32')

    text_embeddings=[]
    for emb_matrix in emb_matrices:
        output_dims=emb_matrix.shape[1]
        text_embeddings.append(Embedding(
            input_dims + 1,
            output_dims,
            weights=[emb_matrix],
            input_length=input_len,
            trainable=trainable)(text_seq_input))

    filter_sizes = [3, 5]

    conv_pools = []
    for text_embedding in text_embeddings:
        for filter_size in filter_sizes:
            l_zero = ZeroPadding1D(
                (filter_size - 1, filter_size - 1))(text_embedding)
            l_conv = Convolution1D(
                filters=16,
                kernel_size=filter_size,
                padding='same',
                activation='tanh')(l_zero)
            l_pool = GlobalMaxPooling1D()(l_conv)
            conv_pools.append(l_pool)

    l_merge = concatenate(conv_pools, axis=1)
    l_dense = Dense(
        128,
        activation='relu',
        kernel_regularizer=regularizers.l2(0.001))(l_merge)
    l_out = Dense(nb_class, activation='softmax')(l_dense)
    model = Model(inputs=[text_seq_input], outputs=l_out)
    model.name = 'MultiGroupNormConstraintCNN'

    if model_name:
        model.name=model_name

    print(model.summary())
    return model


def character_multiplefilter_cnn(nb_class, trainable=True, model_name=None, input_dims=config.NB_WORDS, input_len=config.MAX_LEN, filters=256, dense_layer_size=1024, embedding_size=128):
    # Input layer
    char_embeddings = np.random.randn(input_dims, embedding_size)

    inputs = Input(shape=(None,))
    x = Embedding(input_dims, embedding_size, weights=[char_embeddings],
                  input_length=input_len, trainable=trainable)(inputs)
    filter_sizes = [10, 7, 5, 3]
    convs = []
    for filter_size in filter_sizes:
        l_conv = Convolution1D(
            filters=filters,
            kernel_size=filter_size,
            activation='tanh')(x)
        l_pool = GlobalMaxPooling1D()(l_conv)
        convs.append(l_pool)
    x = concatenate(convs, axis=1)
    # Fully connected layers
    x = Dense(dense_layer_size, activation='selu', kernel_initializer='lecun_normal')(x)
    x = AlphaDropout(0.5)(x)
    x = Dense(dense_layer_size, activation='selu', kernel_initializer='lecun_normal')(x)
    x = Dropout(0.5)(x)
    # output layer
    predictions = Dense(nb_class, activation='softmax')(x)
    # Build and compile model
    model = Model(inputs=inputs, outputs=predictions)
    model.name = 'CharacterBasedMultipleFilterCNN'

    if model_name:
        model.name = model_name

    print(model.summary())
    return model


def character_zhang_cnn(nb_class, trainable=True, model_name=None, input_dims=1024, input_len=config.MAX_SENT_LEN, filters=256, dense_layer_size=1024, embedding_size=128):
    # Input layer
    char_embeddings = np.random.randn(input_dims, embedding_size)    # Input layer
    inputs = Input(shape=(None, ))
    x = Embedding(input_dims, embedding_size, weights=[char_embeddings],
                  input_length=input_len, trainable=trainable)(inputs)
    # convolution layers
    # layer 1
    x = Convolution1D(filters, 7)(x)
    x = ThresholdedReLU(1e-6)(x)
    x = MaxPooling1D(3)(x)
    # layer 2
    x = Convolution1D(filters, 7)(x)
    x = ThresholdedReLU(1e-6)(x)
    x = MaxPooling1D(3)(x)
    # layer 3
    x = Convolution1D(filters, 7)(x)
    x = ThresholdedReLU(1e-6)(x)
    # layer 4
    x = Convolution1D(filters, 7)(x)
    x = ThresholdedReLU(1e-6)(x)
    # layer 5
    x = Convolution1D(filters, 7)(x)
    x = ThresholdedReLU(1e-6)(x)
    # layer 6
    x = Convolution1D(filters, 3)(x)
    # layer 7
    x = ThresholdedReLU(1e-6)(x)
    x = MaxPooling1D(3)(x)
    # Flatten
    x = Flatten()(x)
    # Fully connected layers
    x = Dense(dense_layer_size)(x)
    x = ThresholdedReLU(1e-6)(x)
    x = Dropout(0.5)(x)
    x = Dense(dense_layer_size)(x)
    x = ThresholdedReLU(1e-6)(x)
    x = Dropout(0.5)(x)
    # Output layer
    predictions = Dense(nb_class, activation='softmax')(x)
    # Build and compile model
    model = Model(inputs=inputs, outputs=predictions)
    model.name = 'CharacterBasedZhangCNN'
    if model_name:
        model.name = model_name

    print(model.summary())
    return model




def very_deep_character_cnn(nb_class, trainable=True, model_name=None, input_dims=1024, input_len=config.MAX_SENT_LEN, filters=256, embedding_size=128):
    char_embeddings = np.random.randn(input_dims, embedding_size)  # Input layer

    model = Sequential([
        Embedding(input_dims, embedding_size, weights=[char_embeddings],
                  input_length=input_len, trainable=trainable),
        Convolution1D(filters, 3, padding="valid")
    ])

    # 4 pairs of convolution blocks followed by pooling
    for filter_size in [64, 128, 256]:

        # each iteration is a convolution block
        for cb_i in [0, 1]:
            model.add(Convolution1D(filter_size, 3, padding="same"))
            model.add(BatchNormalization())
            model.add(Activation("relu"))
            model.add(Convolution1D(filter_size, 3, padding="same")),
            model.add(BatchNormalization())
            model.add(Activation("relu"))

        model.add(MaxPooling1D(pool_size=2, strides=3))

    # model.add(KMaxPooling(k=2))
    model.add(Flatten())
    model.add(Dense(4096, activation="relu"))
    model.add(Dense(2048, activation="relu"))
    model.add(Dense(2048, activation="relu"))
    model.add(Dense(nb_class, activation="softmax"))
    model.name = "VeryDeepCharacterBasedCNN"
    if model_name:
        model.name = model_name

    print(model.summary())
    return model


def character_dilated_cnn(conb_class, model_name=None, input_dims=config.NB_WORDS, dilation_rates=[0, 2, 4],
                          embed_size=256):
    inp = Input(shape=(None, ))
    x = Embedding(input_dim=input_dims,
                  output_dim=embed_size)(inp)
    prefilt_x = Dropout(0.25)(x)
    out_conv = []
    # dilation rate lets us use ngrams and skip grams to process
    for dilation_rate in dilation_rates:
        x = prefilt_x
        for i in range(2):
            if dilation_rate > 0:
                x = Convolution1D(
                    16 * 2**(i),
                    kernel_size=3,
                    dilation_rate=dilation_rate,
                    activation='relu',
                    name='ngram_{}_cnn_{}'.format(
                        dilation_rate,
                        i))(x)
            else:
                x = Convolution1D(16 * 2**(i),
                                  kernel_size=1,
                                  activation='relu',
                                  name='word_fcl_{}'.format(i))(x)
        out_conv += [Dropout(0.5)(GlobalMaxPooling1D()(x))]
    x = concatenate(out_conv, axis=-1)
    x = Dense(64, activation='relu')(x)
    x = Dropout(0.1)(x)
    x = Dense(32, activation='relu')(x)
    x = Dropout(0.1)(x)
    x = Dense(conb_class, activation='sigmoid')(x)
    model = Model(inputs=inp, outputs=x)
    model.name = 'CharacterDilationCNN'
    if model_name:
        model.name = model_name

    print(model.summary())
    return model


def c_lstm(nb_class, emb_matrix, trainable=True, model_name=None, lstm_size=64, input_dims=config.NB_WORDS, output_dims=config.EMBEDDING_DIM, input_len=config.MAX_LEN, filters=128, dense_layer_size=128):
    text_seq_input = Input(shape=(input_len,), dtype='int32')
    text_embedding = Embedding(input_dims + 1,
                               output_dims,
                               weights=[emb_matrix],
                               trainable=trainable,
                               input_length=input_len)(text_seq_input)

    filter_sizes = [3, 4, 5, 6, 7]
    convs = []
    for filter_size in filter_sizes:
        l_conv = Convolution1D(
            filters=filters,
            kernel_size=filter_size,
            padding='same',
            activation='relu')(text_embedding)
        convs.append(l_conv)

    cnn_feature_maps = concatenate(convs, axis=1)
    sentence_encoder = LSTM(lstm_size, return_sequences=False)(cnn_feature_maps)
    fully_connected = Dense(dense_layer_size, activation="relu")(sentence_encoder)
    out = Dense(nb_class, activation="softmax")(fully_connected)
    model = Model(inputs=[text_seq_input], outputs=out)

    if model_name:
        model.name = model_name

    print(model.summary())
    return model


def ac_bilstm(nb_class, emb_matrix, trainable=True, model_name=None, lstm_size=64, input_dims=config.NB_WORDS, output_dims=config.EMBEDDING_DIM, input_len=config.MAX_LEN, filters=128, dense_layer_size=128):
    text_seq_input = Input(shape=(input_len,), dtype='int32')
    text_embedding = Embedding(input_dims + 1,
                               output_dims,
                               weights=[emb_matrix],
                               trainable=trainable,
                               input_length=input_len)(text_seq_input)

    filter_sizes = [3, 4, 5, 6, 7]
    convs = []
    for filter_size in filter_sizes:
        l_conv1 = Convolution1D(filters=filters, kernel_size=1, strides=1,
                                padding="same")(text_embedding)
        l_relu1 = Activation("relu")(l_conv1)
        l_conv2 = Convolution1D(filters=filters, kernel_size=filter_size, strides=1,
                                padding="same")(l_relu1)
        l_relu2 = Activation("relu")(l_conv2)
        convs.append(l_relu2)

    l_concat = concatenate(convs, axis=2)
    l_blstm = Bidirectional(
        LSTM(
            lstm_size,
            activation="relu",
            return_sequences=True))(l_concat)
    l_dropout = Dropout(0.5)(l_blstm)
    l_flatten = Flatten()(l_dropout)
    l_fc = Dense(dense_layer_size, activation='sigmoid')(l_flatten)
    out = Dense(nb_class, activation="softmax")(l_fc)
    model = Model(inputs=[text_seq_input], outputs=out)
    model.name = 'AC-BILSTM'

    if model_name:
        model.name = model_name

    print(model.summary())
    return model
