#iris 꽃의 데이터를 내려 받아 곷의 속성을 base line 모델을 만들어 성능(acc) 90% 이상 모델을 만들자.

#petal_length = 꽃받침 길이
#sepal_width = 꽃받침 넓이
#petal_length = 꽃잎 길이
#petal_width = 꽃잎 너비
#species = 꽃의 종류

#데이터 불러오기-------------------------------
import seaborn as pd
import seaborn as sns

#sns 데이터셋에 내장된 데이터 확인
sns.get_dataset_names()

#데이터 확인하기-------------------------------
df = sns.load_dataset("iris")
df.head()

print(type(df['petal_length'][0]), #꽃받침 길이
      type(df['sepal_width'][0]),  #꽃받침 넓이
      type(df['petal_length'][0]), #꽃잎 길이
      type(df['petal_width'][0]),  #꽃잎 너비
      type(df['species'][0]))      #꽃의 종류

df.info()
df.describe()#print의 통계정보 확인

#출력 데이터 그래프로 확인---------------------------
import missingno as mino
mino.matrix(df)
#출력 값 : 그래프 출력!

#boxplot(박스 플롯) 그래프-------------------------------
df.head()
data = df.iloc[:, :-1]
data.boxplot()
#sepal_with의 경우 outlier가 발견된다.
#위 평균값과 비교했을 때 범위가 크게 벗어나지 않아 넘어가기로 함.
#출력 값 : 그래프 출력!

#산점도-------------------------------
sns.pairplot(df, hue='species')
#출력 값 : 그래프 출력!

#데이터 전처리-------------------------------
df.head()
#데이터 플레임 안에 할당 
#x는 df안에서 열0 ~ 열3에 할당
#y는 df안에서 열 마지막에 할당
x = df.iloc[:,0:4] # sepal_length, sepal_width, petal_length, petal_width
y = df.iloc[:, -1] # species

#x = df [['sepal_length', 'sepal_width', 'petal_length', 'petal_width']]
#y=df['species']

from sklearn.preprocessing import LabelEncoder

#LabelEncoder인코딩 한다. encoding(열)의 데이터를
encoding = LabelEncoder() # 선언
y_encoding = encoding.fit_transform(y)
y_encoding
#출력 값 : 데이터 인코딩 값 출력

#데이터 모델링-------------------------------
from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x, y_encoding, test_size=0.2, random_state=2)
# train_test_split이 함수에서
# x는 독립변수 
# y_encoding는 종속변수
# test_size=0.2는 테스트 셋트의 비율이 0.2(20%)라는 뜻

print('훈련 : ', len(x_train), len(y_train))
print('테스트 : ', len (x_test), len(y_test))
#출력 값 :훈련 :  120 120
#출력 값 :테스트 :  30 30

#Sequential눈 순차적 신경망 모델이다.
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

model = Sequential()

model.add(Dense (8, input_dim= 4, activation = 'relu'))
model.add(Dense (3, activation = 'softmax'))

model.compile(loss = 'sparse_categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])
test_loss, test_acc = model.evaluate(x_test,y_test, verbose=2)

print('test_loss', test_loss)
print('test_acc', test_acc)
#출력 값 : 손실 loss의 값은 5.6 오차율을 의미
#출력 값 : 정확도 acc는 0.26 즉 26%의 정확도를 보이고 있다.

#모델 성능 향상-------------------------------
import pandas as pd
import numpy as np
import seaborn as sns

from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization

df = sns.load_dataset('iris')

X = df.iloc[:, 0:4] # sepal_length, sepal_width, petal_length, petal_width
y= df.iloc[:, -1] # species

encoding= OneHotEncoder (sparse = False)
y_encoding = encoding.fit_transform(np.array(y).reshape(-1,1))
# encoding = LabelEncoder()
# y_encoding encoding.fit_transform(y)

x_train, x_test, y_train, y_test = train_test_split (x, y_encoding, test_size = 0.2,
                                                     random_state=2) # test_size: default = 0.25 22
#모델 Sequential 생성
model = Sequential( )
model.add(Dense (1024, input_dim = 4, activation = 'relu'))
model.add(Dropout (0.5))
model.add(Dense (512, activation = 'relu'))
model.add(Dense (128, activation = 'relu'))
model.add(Dense (32, activation = 'relu'))
model.add(Dense (3, activation = 'softmax'))

model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

#epochs 1000번의 학습 / batch_size 배치크기 10
model.fit(x_train, y_train, epochs = 1000, batch_size = 10)

test_loss, test_acc = model.evaluate(x_test,y_test, verbose=2)

print('test_loss', test_loss)
print('test_acc',test_acc)
#출력 값 : #손실 loss의 값은 0.03 오차율을 의미
#출력 값 : #정확도 acc는 1 즉 100%의 정확도를 보이고 있다.

# 추가 원핫 인코딩 사용의 경우-------------------------------
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

x = df.iloc[:, 0:4]
y = df.iloc[:, -1]

encoding = OneHotEncoder (sparse = False)
y_encoding = encoding.fit_transform (np.array(y).reshape(-1,1))
# 원핫 인코딩을 사용하려면 범주형 변수는 배열이 반드시 2차원 배열이어야 하기 때문에 reshape 진행
x_train, x_test, y_train, y_test = train_test_split (X, y_encoding)

model = Sequential()

model.add(Dense (1024, input_dim= 4, activation = 'relu'))
model.add(Dense (512,  activation = 'relu'))
model.add(Dense (128, activation = 'relu'))
model.add(Dense (32, activation = 'relu'))
model.add(Dense (3, activation = 'softmax'))

model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

model.fit(x_train, y_train, epochs = 10, batch_size = 10)

test_loss, test_acc = model.evaluate(x_test,y_test, verbose=2)

print('test_loss', test_loss)
print('test_acc',test_acc)
#손실 loss의 값은 0.04 오차율을 의미
#정확도 acc는 1 즉 100%의 정확도를 보이고 있다.
