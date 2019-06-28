# -*- coding: utf-8 -*-
"""Script.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xniQ6PrxNUgcDBUUFpazn9UcrJssObhf
"""

import keras.utils
import numpy as np
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from keras.layers import Dense, Embedding, Flatten, Dropout
from sklearn.utils import shuffle
import ast

f = open('Dataset/pos/train.csv','r')
training_pos = []
for line in f.readlines():
    training_pos.append(ast.literal_eval(line))
training_pos_label = [1] * len(training_pos)


f2 = open('Dataset/neg/train.csv','r')
training_neg = []
for line in f2.readlines():
    training_neg.append(ast.literal_eval(line)) 
training_neg_label = [0] * len(training_neg)


f3 = open('Dataset/pos/val.csv','r')
val_pos = []
for line in f3.readlines():
    val_pos.append(ast.literal_eval(line)) 
val_pos_label = [1] * len(val_pos)


f4 = open('Dataset/neg/val.csv','r')
val_neg = []
for line in f4.readlines():
    val_neg.append(ast.literal_eval(line)) 
val_neg_label = [0] * len(val_neg)


f5 = open('Dataset/pos/test.csv','r')
test_pos = []
for line in f5.readlines():
    test_pos.append(ast.literal_eval(line)) 
test_pos_label = [1] * len(test_pos)


f6 = open('Dataset/neg/test.csv','r')
test_neg = []
for line in f6.readlines():
    test_neg.append(ast.literal_eval(line)) 
test_neg_label = [0] * len(test_neg)

text = training_pos + training_neg + val_pos + val_neg + test_pos + test_neg
label = training_pos_label + training_neg_label + val_pos_label + val_neg_label + test_pos_label + test_neg_label

len(text)

label = keras.utils.to_categorical(np.asarray(label))

maxlength = max([len(s) for s in text])
maxlength

tokenizer = Tokenizer()
tokenizer.fit_on_texts(text)
seq = tokenizer.texts_to_sequences(text)
word_index_values = tokenizer.word_index

data = pad_sequences(seq, maxlen = maxlength)

embeddingIndex = {}
f = open("Dataset/Word2Vec_embeddings.txt", "r")
for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    embeddingIndex[word] = coefs
f.close()

EMBEDDING_DIM = 300

embedding_matrix = np.zeros((len(word_index_values) + 1, EMBEDDING_DIM))
for word, i in word_index_values.items():
    embedding_vector = embeddingIndex.get(word)
    if embedding_vector is not None:
        embedding_matrix[i] = embedding_vector

embedding_layer = Embedding(len(word_index_values) + 1, EMBEDDING_DIM, weights = [embedding_matrix], input_length = maxlength, trainable = False)

model = Sequential()

model.add(embedding_layer)
model.add(Dense(64, activation='sigmoid', kernel_regularizer= keras.regularizers.l2(0.001)))
model.add(Flatten())
model.add(Dropout(0.4))
model.add(Dense(2, activation = 'softmax', kernel_regularizer= keras.regularizers.l2(0.001)))

model.compile(loss = 'binary_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

train_X = training_pos + training_neg 
train_Y = training_pos_label + training_neg_label
train_Y = keras.utils.to_categorical(np.asarray(train_Y))


val_X = val_pos + val_neg
val_Y = val_pos_label + val_neg_label
val_Y = keras.utils.to_categorical(np.asarray(val_Y))


test_X = test_pos + test_neg
test_Y = test_pos_label + test_neg_label
test_Y = keras.utils.to_categorical(np.asarray(test_Y))


train_X, train_Y = shuffle(train_X, train_Y)
val_X, val_Y = shuffle(val_X, val_Y)
test_X, test_Y = shuffle(test_X, test_Y)

X_train_tokens = tokenizer.texts_to_sequences(train_X)
X_val_tokens = tokenizer.texts_to_sequences(val_X)
X_train_pad = pad_sequences(X_train_tokens, maxlen = maxlength, padding = 'post')
X_val_pad = pad_sequences(X_val_tokens, maxlen = maxlength, padding = 'post')

X_test_tokens = tokenizer.texts_to_sequences(test_X)
X_test_pad = pad_sequences(X_test_tokens, maxlen = maxlength, padding = 'post')

model.fit(X_train_pad, train_Y, batch_size = 300, epochs = 5, validation_data = (X_val_pad, val_Y))

print('\n# Evaluating results on the test data')
results = model.evaluate(X_test_pad, test_Y, batch_size=128)
print('Test loss, Test acc:', results)	


