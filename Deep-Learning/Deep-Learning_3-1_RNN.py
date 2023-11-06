#RNN 기초-------------------------------
# RNN은 가장 기본적인 인공신경망 시퀀스 모델로, 입력과 출력을 시퀀스 단위로 처리하는 모델이다.
# 시퀀스 (Sequence) : 전기회로 도면 모양을 뜻함. (녹색 판에 복잡시러운 그거)
# Sequential Model : 연속적인 입력으로부터 연속적인 출력을 생성하는 모델
# 순차데이터(sequential data) : ‘순서’를 가진 데이터로 순서가 변경될 경우 데이터의 특성을 잃어버리는 데이터를 의미함
#                             EX) 문장, 주가, 날씨, DNA 유전정보 등의 시계열 데이터(time series data)

# RNN 종류-------------------------------
# One to Many-----------
# 하나의 입력을 받아 RNN 층을 통과하면 여러개의 출력값을 내보내는 모형
# 활용 영역 : 이미지 캡셔닝 - 입력값 '이미지 데이터'를 넣으면 출력값으로 이미지를 '설명하는 문장'이 나옴
#                           EX)'이미지 데이터' --- 컴퓨터 --- '코딩을 하는 사람!'

# 아래 2개 : 문서(문장)을 토큰화하고, 토큰화된 단어는 여러개의 입력이 되어 RNN층을 통과하게 되면 긍정 혹은 부정의 확률값이 출력됨. 확률값을 보고 긍정,부정 판단 가능 기술
# Many to One-----------
# 여러개 입력을 받아 RNN층을 통과하여 하나의 출력을 내보내는 모형
# 활용 영역 : 감정분석 - 어떤 문장이나 문서에 대한 주관적 극성을 분류하는 방법
#                      EX)'오늘 데이트 코스 재미있었어!' --- 컴퓨터 --- '긍정!' 

# Many to Many-----------
# 여러개의 입력값을 받아 RNN층을 통과하여 여러개의 출력값을 내모내는 모형
# 입력과 출력의 갯수가 같은경우와, 같지않은 경우 두가지 모형이 존재
# Seq2Seq : 입력과 출력의 갯수가 같은 경우
# 활용 영역 : 개체명인식 - 단어가 입력되면, 입력된 단어가 어떤 유형(사람, 장소, 조직, 시간 등)에 속하는지 인식하는 방법
#                        EX)'저녁 동대문 데이트에 먹은 파스타는 맛있었다.' --- 컴퓨터 --- '긍정!'    

# RNN 한계점-------------------------------
# 장기의존성 문제 : 예측하는 문장의 길이가 길어지는 경우 먼저 입력된 단어의 반영도는 점차 줄어드는 문제가 발생


# RNN 기초--------------------------------------------------------------
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

train_x = [[1,2,3,4,5],
           [2,4,6,8,10],
           [1,3,5,7,9],
           [0,2,4,6,8]]
print (np.shape (train_x))
# 출력 값 : (4, 5)

#이건 train_x가 2차원 () 안에 있으니깐
train_x = np.array(train_x, dtype=np.float32)
print(train_x.shape)
# 출력 값 : (4, 5)

# RNN의 경우 2차원이 아닌 3차원 tensor로 값을 입력받기 때문에 3차원으로 변환해 준다.
# 이건 train_x가 3차원 () 안에 [] 안을 더 했으니깐
train_x = np.array([train_x], dtype=np.float32)
print(train_x.shape)
# 출력 값 : (1, 4, 5)

# 파라미터인 return_sequences와 return_state-------------------------------
# 두 파라미터의 default 값은 False이다

# return_sequence = False : 마지막 시점의 hidden state만 출력된다.
#우선 hidden_size는 임의로 3으로 정한다.
hidden_size = 3 # hidden state 차원수 3차원이라는 뜻.
cell = layers.SimpleRNNCell (units = hidden_size)
rnn = layers.RNN(cell, return_sequences=True, return_state=False)
hidden_state = rnn (train_x)

print('train_x: {} \t shape {}'.format(train_x, train_x.shape))
print('hidden_state: {} \t shape: {}'.format (hidden_state, hidden_state.shape))

# tensor (1,3)
# 마지막 시점의 hidden state이다.


# return_sequences = True : 모든 시점의 hidden state가 출력됨
cell = layers.SimpleRNNCell (units = hidden_size)
rnn = layers. RNN (cell, return_sequences=True, return_state=False)
hidden_state= rnn(train_x)

print('train_x : {} \t shape: {}'.format(train_x, train_x.shape))
print('hidden_state: {} \t shape: {}'.format(hidden_state, hidden_state.shape))

#tensor (1,4,3) 출력
#입력(x_data)의 크기는 (1,4,5)였고, 모든 시점의 hidden state 값을 출력하기 때문에 (1,4,3)가 됨 (시점을 의미하는 값 4)


# return_state = True : return_sequence의 값이 True/False인지 관계없이 마지막 시점의 은닉상태를 출력
cell = layers.SimpleRNNCell (units = hidden_size)
rnn = layers. RNN (cell, return_sequences=True, return_state=True)
hidden_state, last_state= rnn (train_x)

print('train_x: {} \t shape: {}'.format(train_x, train_x.shape))

print('hidden_state: {} \t shape : {}'.format(hidden_state, hidden_state.shape))
print('last_state: {} \t shape: {}'.format(last_state, last_state.shape))


# return_sequences=False인데 return_state = True : 마지막 시점의 hidden state가 출력됨
cell = layers.SimpleRNNCell (units = hidden_size)
rnn = layers.RNN (cell, return_sequences=False, return_state=True)
hidden_state, last_state= rnn (train_x)

print('train_x: {} \t shape: {}'.format(train_x, train_x.shape))
print('hidden_state ()\t shape: ()'.format (hidden_state, hidden_state.shape))
print('last state: {} \t shape: {}'.format(last_state, last_state.shape))








