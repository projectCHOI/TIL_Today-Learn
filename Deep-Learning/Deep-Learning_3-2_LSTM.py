# LSTM 기초-------------------------------
# LSTM(장단기 메모리) : RNN의 장기의존성문제와 Gradient 문제를 해결하기 위해 고안된 모형
# ‘Gate’를 추가하여 기억할것과 잊을것을 선택하여 중요한 정보만 기억하도록 함 - 기존 RNN 모형에비해 학습 속도가 빨라짐

# LSTM 구조-------------------------------
# Forget Gate : 전 단계에서 받은 정보를 얼마나 잊어버릴지에 대한 값을 결정
# 0과 1로 변환된 데이토를 해석한다.

# LSTM 기초--------------------------------------------------------------
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

train_x = [[1,2,3,4,5],
           [2,4,6,8,10],
           [1,3,5,7,9],
           [0,2,4,6,8]]

train_x = np.array(train_x, dtype=np.float32)
train_x = np.array([train_x], dtype=np.float32)

from keras.layers import LSTM

# return_sequences=False인데 return_state = True일 경우
# 우선 hidden_size는 임의로 3으로 정한다.
hidden_size = 3 # hidden state
lstm = LSTM(units=hidden_size, return_sequences=False, return_state=True)
hidden_state, last_state, last_cell_state = lstm(train_x)

print('train_x : {} \t shape{}'.format(train_x, train_x.shape))
print('hidden_state: {} \t shape: {}'.format (hidden_state, hidden_state.shape))
print('last_state {} \t shape: {}'.format(last_state, last_state.shape))
print('last_cell_state: {} \t shape: {}'.format(last_cell_state, last_cell_state.shape))

#return_sequence가 False일 때 마지막 hidden_state가 출력되므로 hidden_state = last_cell_state 결과값이 같다.
#RNN과 LSTM의 차이점은 LSTM의 경우 return_state = True인 경우 last_cell_state까지 출력해준다는 것이 다른다


# return_sequences=True인데 return_state = True일 경우
# 우선 hidden_size는 임의로 3으로 정한다.
hidden_size = 3 # hidden state
lstm = LSTM(units=hidden_size, return_sequences=True, return_state=True)
hidden_state, last_state, last_cell_state = lstm(train_x)

print('train_x: {} \t shape : {}'. format(train_x, train_x.shape))
print('hidden_state: {} \t shape: ()'.format(hidden_state, hidden_state.shape))
print('last state: {} \t shape: {}'.format(last_state, last_state.shape))
print('last_cell_state : {} \t shape : {}'.format(last_cell_state, last_cell_state.shape))
#return_sequence가 True인 경우 모든 hidden_state값이 출력되므로 4개 값에대한 hidden_state가 모두 출력되었다.
#