#Deep-Learning_CNN_실습2_shopping
#다양한 의류 이미지를 예측하는 모델 만들기

#데이터 불러오기-------------------------------
import tensorflow as tf
fmnist = tf.keras.datasets.fashion_mnist
(x_train, y_train),( x_test, y_test) = fmnist.load_data()

x_train.shape, y_train.shape

#데이터 확인하기-------------------------------
x_train

import matplotlib.pyplot as plt

#이미지 데이터를 그릴 박스크기(그래프 영역) 설정
fig, axes = plt.subplots(1, 1)
fig.set_size_inches(10, 5) #크기설정

axes.imshow(x_train[0], cmap='gray') #imshow이미지 데이터 확인
axes.set_title(str(y_train[0]))

plt.show()

#전체 데이터 가져오기-------------------------------
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 5) #2 곱하기 5의 (10)의 데이터를 보겠다.
fig.set_size_inches(10, 5)

for i in range(10):
  axes[i//5, i%5].imshow(x_train[i],cmap='gray') #axes[i//5, i%5]는 그림이 나오는 자리를 의미.
  axes[i//5, i%5].set_title(str(y_train[i]))
  plt.setp( axes[i//5, i%5].get_xticklabels(), visible=False)
  plt.setp( axes[i//5, i%5].get_yticklabels(), visible=False)

plt.tight_layout() # 자동으로 여백 조정 (상황 보고 선택적 사용)
plt.show()

#DNN으로 MNIST 구현-------------------------------
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train[0]

x_train = x_train/255.0
x_test = x_test/255.0
x_train[0]
# MNIST data는 각 픽셀이 0 ~ 255사이의 정수값을 가진다.
# 이런 이미지의 경우 보통 255로 나누어 0 ~ 1사이 값으로 정규화를 한다.
# 표준화는 아니지만, 양수값으로 이루어진 이미지 전처리(scaling)에 주로 사용되는 방법이다.

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten

model = Sequential()
model.add(Flatten(input_shape = (28,28)))#28x28 사이즈 라는 뜻.
model.add(Dense(64, activation = 'relu'))
model.add(Dense(10, activation = 'softmax')) # 0 ~ 9 로 카테고리가 총 10개

model.compile(loss = 'sparse_categorical_crossentropy',
              optimizer = 'adam', metrics=['acc'])

model.fit(x_train,y_train,
          validation_data = (x_test, y_test), epochs = 5) #학습 툴

test_loss, test_acc = model.evaluate(x_test,  y_test, verbose=2)

print('\nTest loss:',test_loss)
print('\nTest accuracy:', test_acc)
#--------------------------------------------------------------
import tensorflow as tf
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train.shape, y_train.shape

x_train = x_train.reshape(60000, 28, 28, 1)
x_test = x_test.reshape(10000, 28, 28, 1)
#(데이터 갯수, 픽셀, 픽셀) cf. 채널 값 흑백은(1), 칼라는 (3)
x_train = x_train / 255.0
x_test = x_test / 255.0

x_train[0]

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, BatchNormalization #BatchNormalization는 성능개선을 위한 말, 써두 되고 안 써두됨

model = Sequential()
## 아래에 Conv2D를 쌓아보세요.

#feature extraction 부분
model.add(Conv2D (64, (3,3), input_shape = (28,28,1), activation = 'relu'))
model.add(MaxPooling2D (2,2))#MaxPooling2D 용량 줄여줌

#classification 부분
model.add(Conv2D (32, (3,3), activation='relu'))
model.add(MaxPooling2D(2,2))
model.add(Flatten()) #Flatten map 1차원으로 변형

#fully-connectied layer 부분
model.add(Dense (128, activation='relu'))
model.add(BatchNormalization())

model.add(Dense(10, activation = 'softmax')) #출력
model.compile(loss = 'sparse_categorical_crossentropy', optimizer = 'adam', metrics=['acc'])

model.fit(x_train,y_train, validation_data = (x_test, y_test), epochs = 5)

#모델 결과-------------------------------
test_loss, test_acc = model.evaluate(x_test,  y_test, verbose=2)

print('\nTest loss:',test_loss)
print('\nTest accuracy:', test_acc)
#출력 값 : 손실 loss의 값은 0.03 즉 3% 오차율을 의미
#출력 값 : 정확도 acc는 0.97 즉 97%의 정확도를 보이고 있다.
