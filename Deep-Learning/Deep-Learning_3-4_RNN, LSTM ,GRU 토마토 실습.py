# RNN, LSTM ,GRU 토마토 실습-------------------------------
# '토마토를 먹자'를 축력하기 위한 코드를 만들어보자.
# input = '토토마를자먹'
# output = '토마토를먹자'

# RNN--------------------------------------------------------------
# RNN 자료 불러오기-------------------------------
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNNCell, Dense, TimeDistributed, RNN

idx2char = ['토', '마', '를', '먹', '자']

x_data = [[0, 0, 1, 2, 4, 3]] #토토마를자먹
y_data = [[0, 1, 0, 2, 3, 4]] #토마토를먹자

num_classes = 5
input_dim = 5
sequence_len = 6
learning_rate = 0.1

# RNN 데이터 변환 원-핫 인코딩-------------------------------
x_one_hot = tf.keras.utils.to_categorical (x_data, num_classes=num_classes)
y_one_hot = tf.keras.utils.to_categorical (y_data, num_classes=num_classes)

# 시퀀스수, 시퀀스길이, dim 사이즈-------------------------------
x_one_hot.shape

# RNN 모델링-------------------------------
model = Sequential() #선언을 꼭 해줘야한다.
cell = SimpleRNNCell(units=num_classes, input_shape=(sequence_len, input_dim)) # SimpleRNNCell

model.add(RNN (cell=cell,
               return_sequences=True,
               return_state=False,
               input_shape = (sequence_len, input_dim)))

model.add(TimeDistributed(Dense(units=num_classes, activation='softmax')))

model.compile(loss = 'categorical_crossentropy',
              optimizer=tf.keras.optimizers.Adam(learning_rate-learning_rate),
              metrics=['accuracy'])

model.fit(x_one_hot, y_one_hot, epochs=10)
pred = model.predict(x_one_hot)

# RNN 출력-------------------------------
# pred
for i, word in enumerate(pred):
    print(" ".join([idx2char[c] for c in np.argmax (word, axis=1)]))


# LSTM--------------------------------------------------------------
# LSTM자료 불러오기-------------------------------
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, TimeDistributed, RNN
from keras.layers import LSTM # LSTM

idx2char = ['토', '마', '를', '먹', '자']

x_data = [[0, 0, 1, 2, 4, 3]] #토토마를자먹
y_data = [[0, 1, 0, 2, 3, 4]] #토마토를먹자

num_classes = 5
input_dim = 5
sequence_len = 6
learning_rate = 0.1

# LSTM데이터 변환 원-핫 인코딩-------------------------------
x_one_hot = tf.keras.utils.to_categorical (x_data, num_classes=num_classes)
y_one_hot = tf.keras.utils.to_categorical (y_data, num_classes=num_classes)

# 시퀀스수, 시퀀스길이, dim 사이즈-------------------------------
x_one_hot.shape

# LSTM모델링-------------------------------
model = Sequential() #선언을 꼭 해줘야한다.

model.add(LSTM(units=num_classes,
                return_sequences = True,
                input_shape = (sequence_len, input_dim), activation = 'tanh'))
model.add(Dense(32, activation='relu'))
model.add(Dense(units=num_classes, activation='softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer=tf.keras.optimizers. Adam (learning_rate-learning_rate),
              metrics=['accuracy'])

model.fit(x_one_hot, y_one_hot, epochs=10)
pred = model.predict(x_one_hot)

# LSTM출력-------------------------------
# pred
for i, word in enumerate (pred):
    print(" ".join([idx2char[c] for c in np.argmax (word, axis=1)]))


# GRU--------------------------------------------------------------
# GRU자료 불러오기-------------------------------
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, TimeDistributed, RNN
from keras.layers import GRU # GRU

idx2char = ['토', '마', '를', '먹', '자']

x_data = [[0, 0, 1, 2, 4, 3]] #토토마를자먹
y_data = [[0, 1, 0, 2, 3, 4]] #토마토를먹자

num_classes = 5
input_dim = 5
sequence_len = 6
learning_rate = 0.1

# GRU데이터 변환 원-핫 인코딩-------------------------------
x_one_hot = tf.keras.utils.to_categorical (x_data, num_classes=num_classes)
y_one_hot = tf.keras.utils.to_categorical (y_data, num_classes=num_classes)

# 시퀀스수, 시퀀스길이, dim 사이즈-------------------------------
x_one_hot.shape

# GRU모델링-------------------------------
model = Sequential() #이번에도 선언을 꼭 해줘야한다.

model.add(GRU (units=num_classes,
               return_sequences=True,
               input_shape = (sequence_len, input_dim),activation = 'tanh'))
model.add(Dense (32, activation= 'relu'))
model.add(Dense (units=num_classes, activation='softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer=tf.keras.optimizers. Adam (learning_rate-learning_rate),
              metrics=['accuracy'])

model.fit(x_one_hot, y_one_hot, epochs=10)
pred = model.predict(x_one_hot)

# GRU출력-------------------------------
# pred
for i, word in enumerate (pred):
    print(" ".join([idx2char[c] for c in np.argmax (word, axis=1)]))
#