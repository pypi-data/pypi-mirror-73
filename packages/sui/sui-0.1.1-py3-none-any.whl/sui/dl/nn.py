"""Module including some useful implementations apropos neural networks.
"""
__author__ = ['Li Tang']
__copyright__ = 'Li Tang'
__credits__ = ['Li Tang']
__license__ = 'GPL'
__version__ = '1.0.1'
__maintainer__ = ['Li Tang']
__email__ = 'litang1025@gmail.com'
__status__ = 'Production'

import tensorflow as tf
from tensorflow.keras.layers import Dense

from sui import dataset


class PNN(tf.keras.Model):
    """Product-based Neural Networks
    https://arxiv.org/pdf/1611.00144.pdf
    """

    def __init__(self, features_dim: int, fields_dim: int, hidden_layer_sizes: list, dropout_params: list,
                 product_layer_dim=10, lasso=0.01, ridge=1e-5, embedding_dim=10, product_type='ipnn', model=None):
        super(PNN, self).__init__()
        self.features_dim = features_dim  # number of different features after one-hot, denoted by F
        self.fields_dim = fields_dim  # number of different original features
        self.dropout_params = dropout_params
        self.hidden_layer_sizes = hidden_layer_sizes  # number of hidden layers
        self.product_layer_dim = product_layer_dim
        self.lasso = lasso
        self.ridge = ridge
        self.embedding_dim = embedding_dim  # dimension of vectors after embedding, denoted by M
        self.product_type = product_type  # 'ipnn' for inner product while 'opnn' for outer product

        self.model = model
        # if there is no pre-trained model to use
        if self.model is None:
            # embedding layer
            self.embedding_layer = self.__init_embedding_layer()

            # product layer
            self.product_layer = self.__init_product_layer()

            # hidden layers
            for layer_index in range(len(self.hidden_layer_sizes)):
                setattr(self, 'dense_' + str(layer_index), tf.keras.layers.Dense(self.hidden_layer_sizes[layer_index]))
                setattr(self, 'batch_norm_' + str(layer_index), tf.keras.layers.BatchNormalization())
                setattr(self, 'activation_' + str(layer_index), tf.keras.layers.Activation('relu'))
                setattr(self, 'dropout_' + str(layer_index), tf.keras.layers.Dropout(dropout_params[layer_index]))

    def __init_embedding_layer(self):
        # the size of embedding layer is F * M
        return tf.keras.layers.Embedding(self.features_dim, self.embedding_dim, embeddings_initializer='uniform')

    def __init_product_layer(self):
        # linear signals l_z
        self.__linear_weights = self.__init_linear_signals()
        # embedding_feature = tf.einsum('bnm,bn->bnm', self.embedding_layer(input_feature_index), input_feature_value)
        # l_z = tf.einsum('bnm,dnm->bd', embedding_feature, self.__linear_weights)
        l_z = self.embedding_layer

        # # quadratic signals l_p
        self.__quadratic_signals_variable = self.__init_quadratic_signals()
        # l_p = tf.einsum('bdnm,bdnm->bd', self.__quadratic_signals_variable,
        #                 self.__quadratic_signals_variable)  # Batch * D1
        l_p = self.embedding_layer
        # return tf.concat((l_z, l_p), axis=1)
        return tf.keras.layers.Dense(self.hidden_layer_sizes[0])

    def __init_linear_signals(self, initializer=tf.initializers.GlorotUniform()):
        return tf.Variable(initializer(shape=(self.product_layer_dim, self.fields_dim, self.embedding_dim)))

    def __init_quadratic_signals(self, initializer=tf.initializers.GlorotUniform()):
        assert self.product_type in ['ipnn', 'opnn'], "'product_type' should be either 'ipnn' or 'opnn'."
        if self.product_type == 'ipnn':
            # matrix decomposition based on the assumption: W_p^n = \theta ^n * {\theta^n}^T
            return tf.Variable(initializer(shape=(self.product_layer_dim, self.fields_dim)))
        elif self.product_type == 'opnn':
            pass
        else:
            raise Exception('Arcane exception...')

    @staticmethod
    def loss_function(labels, logits, name=None):
        return tf.nn.sigmoid_cross_entropy_with_logits(labels=labels, logits=logits, name=name)

    def __create_model(self, training=False):
        model = tf.keras.Sequential()

        # embedding layer
        model.add(self.embedding_layer)

        # product layer
        model.add(self.product_layer)

        # fc layers
        for layer_index in range(len(self.hidden_layer_sizes)):
            model.add(getattr(self, 'dense_' + str(layer_index)))
            model.add(getattr(self, 'batch_norm_' + str(layer_index)))
            model.add(getattr(self, 'activation_' + str(layer_index)))
            if training:
                model.add(getattr(pnn, 'dropout_' + str(layer_index)))

        # output layer
        model.add(Dense(2, activation='sigmoid', kernel_initializer='he_normal', name='output'))

        # compile
        model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        self.model = model

    def train(self, data, labels, batch_size=None, epochs=1, verbose=1):
        if self.model is None:
            self.__create_model(training=True)
        self.model.fit(x=data, y=labels, batch_size=batch_size, epochs=epochs, verbose=verbose)

    def predict(self, data, batch_size=None, verbose=0, steps=None, callbacks=None, max_queue_size=10, workers=1,
                use_multiprocessing=False):
        return self.model.predict(x=data, batch_size=batch_size, verbose=verbose, steps=steps, callbacks=callbacks,
                                  max_queue_size=max_queue_size, workers=workers,
                                  use_multiprocessing=use_multiprocessing)

    # TODO dump
    def dump(self):
        pass

    def restore(self):
        pass
