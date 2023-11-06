# GRU 기초-------------------------------
# GRU(Gated Recurrent Unit - 게이트 순환 유닛) : LSTM 모델을 간소화한 모델 (3개에서 2개로)
# LSTM 모델보다 파라미터가 적어 연산비용이 적게들고, 학습속도가 빠름

# GRU 구조-------------------------------
# Forget Gate와 Input Gate를 합쳐 Update Gate를 만들고, Reset Gate를 추가함
# Update Gate : 데이터를 얼마나 활성화 할 것인가 혹은 얼마나 업데이트 할 것인가에 대한 값을 계산
# Reset Gate : 이전 정보에서 얼마만큼을 선택하여 내보낼지에 대한 계산

# Reset gate 값을 사용하여 현재 셀의 값(A)을 계산하고, update gate를 사용하여 새로운 hidden state값을 계산
# hidden state : 메모리 셀이 출력층 방향 또는 다음 시점인 t+1의 자신에게 보내는 값

# GRU 기초--------------------------------------------------------------
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

from keras. layers import GRU

# return_sequences=False인데 return_state = True일 경우
# 우선 hidden_size는 임의로 3으로 정한다.
hidden_size = 3 # hidden state
gru= GRU (units=hidden_size, return_sequences=False, return_state=True)
hidden_state, last_state, last_cell_state = lstm(train_x)

print('train_x : {} \t shape : {}'.format(train_x, train_x.shape))
print('hidden_state : {} \t shape : {}'.format (hidden_state, hidden_state.shape))
print('last_state: {} \t shape: {}'.format(last_state, last_state.shape))
print('last_cell_state : {} \t shape{}'.format(last_cell_state, last_cell_state.shape))


# return_sequences=True일인데 return_state = True일 경우
gru= GRU (units=hidden_size, return_sequences=True, return_state=True)
hidden_state, last_state, last_cell_state = lstm(train_x)

print('train_x: {} \t shape {}'.format(train_x, train_x.shape))
print('hidden_state: {} \t shape: {}'.format(hidden_state, hidden_state.shape))
print('last_state: {} \t shape: {}'.format(last_state, last_state.shape))
print('last_cell_state {} \t shape: {}'.format(last_cell_state, last_cell_state.shape))
#
