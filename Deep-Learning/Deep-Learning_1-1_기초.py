#딥러닝 기초

#빅데이터가 있는 시점에 컴퓨터 언어(Python 등-)을 활용해 알고리즘을 설계한다.
#알고리즘을 다양한 분야에 학습 시켜서 사용하는 것이 머신러닝이다.
# EX.머신러닝 + 자동차 = 자율주행!
# EX. 버튼 A를 누르니깐 움직이네? 왜지? = 머신러닝이 학습 되어 있다.

#미래를 예측하기 위한 학습이다.
#통계학의 선형 회기분석이 밑바탕 되어 있다.

# ----------------------------------------------------
#선형회기 모델링 1
#선형회기 모델링의 구성은 아래와 같다.
import numpy as np
import matplotlib.pyplot as plt

#코랩 from tensorflow.keras.models import Sequential
#코랩 from tensorflow.keras.layers import Dense

x = np.array([2,4,6,8,10])
y = np.array([45,61,73,80,95])

#코랩 model = Sequential()

#코랩 model.add(Dense(1, input_dim=1, activation='linear'))

#코랩 model.compile(loss='mse', optimizer='sgd',metrics=['accuracy'])
#코랩 model.fit(x,y,epochs=50)

#그래프
plt.scatter(x,y)
#코랩 plt.plot(x,model.predict(x),'r')
plt.show()
# 결과 값은 선형 그래프가 뜬다.

#predict(예측값)
#코랩 model.predict([5])
#결과 55.9%
# ----------------------------------------------------
#텐서플로우 선형회기 모델링 2
#x = np.array([[2,0],[4,5],[6,3],[8,5],[10,7]])
#y = np.array([20,24,37,40,50])
#x와y의 선형회기모델을 만들고, [5,7]을 넣었을 때의 값을 예측하라.

import numpy as np
import matplotlib.pyplot as plt

#코랩 from tensorflow.keras.models import Sequential
#코랩 from tensorflow.keras.layers import Dense

x = np.array([[2,0],[4,5],[6,3],[8,5],[10,7]])
y = np.array([20,24,37,40,50])


model = Sequential()

model.add(Dense(1, input_dim=2, activation='linear'))

model.compile(loss='mse', optimizer='sgd',metrics=['accuracy'])
model.fit(x,y,epochs=50)

#predict(예측값)
model.predict([[5,7]])
#결과 26.0%
#----------------------------------------------------
#텐서플로우 로지스틱회귀 모델링
#x = np.array([2,4,6,8,10,12])
#y = np.array([0,0,0,1,1,1])
#로지스틱회귀 모델링을 만들고 [9]를 넣었을 때의 값 예측하라.
import numpy as np
import matplotlib.pyplot as plt

#코랩 from tensorflow.keras.models import Sequential
#코랩 from tensorflow.keras.layers import Dense

x = np.array([2,4,6,8,10,12])
y = np.array([0,0,0,1,1,1])


model = Sequential()

model.add(Dense(1, input_dim=1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='sgd',metrics=['accuracy'])
model.fit(x,y,epochs=50)

#predict(예측값)
print(model.predict([9]))
#결과 0.8%

