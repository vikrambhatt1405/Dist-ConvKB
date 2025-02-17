import tensorflow as tf
import numpy as np
import math
class ConvKB(object):

    """
    A CNN for text classification.
    Uses an embedding layer, followed by a convolutional, max-pooling and softmax layer.
    """

    def __init__(self, sequence_length, num_classes, embedding_size, filter_sizes, num_filters, vocab_size,
                 pre_trained=[], l2_reg_lambda=0.001, batch_size=256, is_trainable=True, useConstantInit=False):
        # Placeholders for input, output and dropout
        self.input_x = tf.placeholder(tf.int32, [batch_size, sequence_length], name="input_x")
        self.input_y = tf.placeholder(tf.float32, [batch_size, num_classes], name="input_y")
        self.dropout_keep_prob = tf.placeholder(tf.float32, name="dropout_keep_prob")

        # Keeping track of l2 regularization loss (optional)
        l2_loss = tf.constant(0.0)

        # Embedding layer
        with tf.name_scope("embedding"):
            if pre_trained == []:
                self.W = tf.Variable(tf.random_uniform([vocab_size, embedding_size], -math.sqrt(1.0/embedding_size), math.sqrt(1.0/embedding_size), seed=1234), name="W",collections=[tf.GraphKeys.LOCAL_VARIABLES])
            else:
                self.W = tf.get_variable(name="W2", initializer=pre_trained) #trainable=is_trainable)

            self.embedded_chars = tf.nn.embedding_lookup(self.W, self.input_x)
            self.embedded_chars_expanded = tf.expand_dims(self.embedded_chars, -1)
        """
        sequence_length=3 because triples.
        self.embedded_chars_expanded is of shape [batch_size,sequence_length,embedding_size,1]
        """
        """
                W is of shape [sequence_length,filter_size,1,num_filters]
                conv is of shape = [batch_size,output_height,output_width,num_filters]
                output_height=(embedding_size-sequence_length)/(1) + 1
        """
        # Create a convolution + maxpool layer for each filter size
        pooled_outputs = []
        for i, filter_size in enumerate(filter_sizes):
            with tf.name_scope("conv-maxpool-%s" % filter_size):
                if useConstantInit == False:
                    filter_shape = [sequence_length, filter_size, 1, num_filters]
                    W = tf.Variable(tf.truncated_normal(filter_shape, stddev=0.1, seed=1234), name="W",collections=[tf.GraphKeys.LOCAL_VARIABLES])
                else:
                    init1 = tf.constant([[[[0.1]]], [[[0.1]]], [[[-0.1]]]])
                    weight_init = tf.tile(init1, [1, filter_size, 1, num_filters])
                    W1 = tf.get_variable(name="W3", initializer=weight_init)
                    W2 = tf.get_variable(name="W4",initializer=weight_init)
                    

                b = tf.Variable(tf.constant(0.0, shape=[num_filters]), name="b",collections=[tf.GraphKeys.LOCAL_VARIABLES])
                conv_1 = tf.nn.conv2d(
                    self.embedded_chars_expanded,
                    W1,
                    strides=[1, 1, 1, 1],
                    padding="VALID",
                    name="conv_1")
                conv_2 =  tf.nn.conv2d(
                    conv_1,
                    W2,
                    strides=[1, 1, 1, 1],
                    padding="VALID",
                    name="conv_2")
                # Apply nonlinearity
                h = tf.nn.relu(tf.nn.bias_add(conv_2, b), name="relu")

                pooled_outputs.append(h)

        # Combine all the pooled features
        self.h_pool = tf.concat(pooled_outputs, 2)
        total_dims = (embedding_size * len(filter_sizes) - sum(filter_sizes) + len(filter_sizes)) * num_filters
        self.h_pool_flat = tf.reshape(self.h_pool, [-1, total_dims])

        # Add dropout
        with tf.name_scope("dropout"):
            self.h_drop = tf.nn.dropout(self.h_pool_flat, self.dropout_keep_prob) #need drop out?

        # Final (unnormalized) scores and predictions
        with tf.name_scope("output"):
            W = tf.get_variable(
                "W",
                shape=[total_dims, num_classes],
                initializer=tf.contrib.layers.xavier_initializer(seed=1234))
            b = tf.Variable(tf.constant(0.0, shape=[num_classes]), name="b",collections=[tf.GraphKeys.LOCAL_VARIABLES])
            l2_loss += tf.nn.l2_loss(W)
            l2_loss += tf.nn.l2_loss(b)
            self.scores = tf.nn.xw_plus_b(self.h_drop, W, b, name="scores")
            self.predictions = tf.nn.sigmoid(self.scores)
        # Calculate mean cross-entropy loss
        with tf.name_scope("loss"):
            losses = tf.nn.softplus(self.scores * self.input_y)
            self.loss = tf.reduce_mean(losses) + l2_reg_lambda * l2_loss
        with tf.name_scope("summary"):
            self.loss_summary=tf.summary.scalar("Soft_Loss",self.loss)

        self.saver = tf.train.Saver(tf.local_variables(), max_to_keep=500)
