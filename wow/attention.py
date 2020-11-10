# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 16:28:17 2020

@author: user
"""

import numpy as np
import pickle
import tensorflow as tf
from tensorflow.keras.layers import Input, Dense, Activation, Add, LayerNormalization, Dropout
from tensorflow.keras.layers import Embedding, Reshape
import tensorflow.keras.backend as K


__all__=["positional_encoding", "Attention" ]

def get_angles(position, i, d_model):
    angles = 1 / tf.pow(10000, (2 * (i // 2)) / tf.cast(d_model, tf.float32))
    return position * angles

def positional_encoding(position, d_model):
    angle_rads = get_angles(np.arange(position)[:, np.newaxis],
                            np.arange(d_model)[np.newaxis, :],
                            d_model)

    sines = tf.math.sin(angle_rads[:, 0::2])
    cosines = tf.math.cos(angle_rads[:, 1::2])

    pos_encoding = tf.concat([sines, cosines], axis=-1)
    # pos_encoding = pos_encoding[tf.newaxis, ...]

    return tf.cast(pos_encoding, tf.float32)

class Attention:
    def __init__(self,
                 num_heads=4,
                 masked=False,
                 key_dim=32,
                 model_dim=128,
                 dropout=0.2,
                 embedLayer1,
                 embedLayer2):
    assert key_dim % num_heads==0

    self.num_heads = num_heads
    self.masked = masked
    self.key_dim = key_dim
    self.model_dim = model_dim
    self.dropout = dropout
    self.embedLayer1 = embedLayer1
    self.embedLayer2 = embedLayer2
    
    def linear_projection(self, embed_Layer1, embed_Layer2):
        q = Dense(self.key_dim, use_bias=False)(embed_Layer1)
        k = Dense(self.key_dim, use_bias=False)(embed_Layer1)
        v = Dense(self.key_dim, use_bias=False)(embed_Layer2)
    
        return q, k, v
    
    def multi_head(self, q, k, v):
        q, k, v = self.linear_projection(embed_layer1, embed_layer2)
        qs, ks, vs = self.split_heads(q, k, v)
        output = self.scaled_dot_produt(qs,ks,vs)
        output = self.concat_heads(output)
        output = Dropout(self.dropout=0.2)(output)
        return output
    
    def split_heads(self,q, k, v):
        def split_last_dimension_then_transpose(tensor, num_heads):
            tensor = K.expand_dims(tensor, axis=1)
            return K.repeat_elements(tensor,rep=num_heads, axis=1)
        
        qs = split_last_dimension_then_transpose(q, self.num_heads)
        ks = split_last_dimension_then_transpose(k, self.num_heads)
        vs = split_last_dimension_then_transpose(v, self.num_heads)
    
        return qs, ks, vs
    
    def _scaled_dot_product(self,qs, ks, vs, self.key_dim):
        '''
        qs: (batch_size, num_heads, max_seq_len, dim)
        ks: (batch_size, num_heads, max_seq_len, dim)
        vs: (batch_size, num_heads, max_seq_len, dim)
        '''
        o1 = tf.matmul(qs, ks, transpose_b=True)    # Q * (K^T)
        o2 = o1 / (key_dim ** 0.5)                  # Q * (K^T) / (dk^(1/2))
    
        if self.masked:
            diag_vals = tf.ones_like(o2[0, 0, :, :])
            tril = tf.linalg.LinearOperatorLowerTriangular(diag_vals).to_dense() # 하삼각행렬: 자기 자신인 단어까지만.
            masks = tf.tile(input=tf.reshape(tril, (1, 1, tril.shape[0], tril.shape[1])), \
                            multiples=[tf.shape(o2)[0], tf.shape(o2)[1], 1, 1]) # batch size, num_heads 만큼 행렬 사이즈 늘려서 마스크 만듦.
            paddings = tf.ones_like(masks) * -1e9 # 주목하지 말아야 할 부분에 낮은 숫자.
            o2 = tf.where(tf.equal(masks, 0), paddings, o2) # mask에 0인 위치(뒤의 단어)에 패딩을 넣어 준다.
    
    
        o3 = Activation('softmax')(o2)              # softmax
        o3 = tf.matmul(o3, vs)
        
        return o3

    def _concat_heads(self,outputs):
        def transpose_then_concat_last_two_dimension(tensor):
            return tf.reshape(tensor, shape=(-1, tensor.shape[2], tensor.shape[1]*tensor.shape[3]))
        return transpose_then_concat_last_two_dimension(outputs)
    
    
    
    




















