#타이타닉 생존자 데이터를 기반으로 [base line]모델을 만들고 성능(acc) 90% 향상모델 만들기.
#전처리를 잘하는게 포인트!!

#데이터 불러오기-------------------------------
import warnings # 경고메세지 끄기
warnings.filterwarnings (action='ignore')
# 참고) 다시 출력하게 하기

import pandas as pd
import seaborn as sns
titanic = sns.load_dataset('titanic')
#titanic.head() 확인용

#데이터 확인오기-------------------------------
titanic.info()
#항목 참고
# survived : 1-생존, 0-사망
# pclass : 객실 등급
# sex : 성별
# age : 나이
# sibsp : 함께 탑승한 형제자매, 아내, 남편 수 
# parch : 함께 탐승한 부모, 자식 수
# fare : 티켓 요금
# embarked : 배에 탑승한 항구 이름 (C = Cherbourn, Q = Queenstown, S = Southampton)
# class : 객실 등급 숫자
# who : 성별
# adult_male : 성인 남성
# deck : 배에 탑승한 항구 이름 (C = Cherbourn, Q = Queenstown, S = Southampton)
# embark_town: 배에 탑승한 항구 이름 (c = Cherbourn, Q = Queenstown, S = Southampton)
# alive : yes 생존, no 사망
# alone : 동반 탑승 유무

#boxplot(박스 플롯) 그래프-------------------------------
# missing data가 있는지 다시한번 그래프를 그려서 확인
import missingno as mino
mino.matrix(titanic)
# nan값이 있는 데이터 : age, embarked, deck 는 확인 필요

#데이터 전처리-------------------------------
titanic = sns.load_dataset('titanic')

#중복 된 컬럼은 우선 제외하고 진행 -> 추후에는 중복된 컬럼을 사용하여 nan 값을 보완해보는 것도 방법이다. 
titanic = titanic[['survived', 'pclass', 'sex', 'age', 'sibsp', 'parch', 'fare', 'embarked', 'adult_male', 'alone']]
print('초기 데이터 : ',len (data))
#출력 값 : 891

#boxplot에서 500이상인 요금은 이상치로 생각하여 제외
titanic [titanic['fare' ]>500]

data = titanic.drop([258,679,737])

# 잘 삭제 되었는지 확인
data.iloc[:,1:].boxplot()

# nan 값 확인
# data[data.isna().any (axis=1)]
data[data.age.isna ()]

data[data.embarked.isna()]

# nan 데이터 삭제
data.dropna (inplace=True)
print('nan 삭제 후 데이터 : ',len (data))

# 범주형 변수(str -> float)
from sklearn.preprocessing import LabelEncoder

# sex, adult male, alone
# LabelEncoder 사용
encoding = LabelEncoder()
data['sex'] = encoding. fit_transform(data['sex']) # male = 1, female = 0
data['adult_male'] = encoding.fit_transform(data['adult_male']) # True = 1, False = 0
data['alone'] = encoding.fit_transform(data['alone']) # True = 1, False = 0

# embarked
# apply 48, replace 48
data['embarked'] = data['embarked'].apply(lambda x : x.replace('C', '0').replace('Q', '1').replace('S', '2')) # C = 0, Q = 1, S = 2

data = data.astype('float') # Tensor 94 int x, Floats
y_encoding = encoding.fit_transform(data['survived'])

#데이터 모델링-------------------------------
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

x = data.iloc[:, 1:]
y = data.iloc[:, 0] # survived

x_train, x_test, y_train, y_test = train_test_split (x, y_encoding, random_state=42) # test_size : default = 0.25 =

model = Sequential()

model.add(Dense (8, input_dim= 9, activation = 'relu'))
model.add(Dense (1, activation = 'sigmoid'))

model.compile(loss = 'binary_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

model.fit(x_train, y_train, epochs = 10, batch_size = 10)

test_loss, test_acc = model.evaluate(x_test,y_test, verbose=2)

print('test_loss', test_loss)
print('test_acc', test_acc)
#출력 값 : 손실 loss의 값은 6.6 오차율을 의미
#출력 값 : 정확도 acc는 0.63 즉 63%의 정확도를 보이고 있다.

#모델 성능 향상-------------------------------
import seaborn as sns

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

titanic = sns.load_dataset ('titanic')
titanic = titanic[['survived', 'pclass', 'sex', 'age', 'sibsp', 'parch', 'fare','embarked', 'adult_male', 'alone']]
data = titanic.drop([258,679,737])

data.dropna (inplace=True)

encoding = LabelEncoder()
data['sex'] = encoding. fit_transform (data['sex']) # male = 1, female = 0
data['adult_male'] = encoding.fit_transform (data['adult_male']) # True = 1, False = 0
data['alone'] = encoding.fit_transform(data['alone']) # True 1, False = 0
data['embarked'] = data['embarked'].apply(lambda x : x.replace('C', '0').replace('Q', '1').replace('S', '2')) # C = 0, Q = 1, S = 2 19

data = data.astype('float')
y_encoding = encoding.fit_transform(data['survived'])

x = data.iloc[:, 1:]
y = data.iloc[:, 0]

x_train, x_test, y_train, y_test = train_test_split (x, y_encoding, random_state=42)

model = Sequential( )

model.add(Dense (512, input_dim= 9, activation = 'relu'))
model.add(Dense (128, activation = 'relu'))
model.add(Dense (64, activation = 'relu')) 
model.add (Dense (64 , activation = 'relu'))
model.add(Dense (32, activation = 'relu'))
model.add(Dense (1, activation = 'sigmoid'))

model.compile(loss = 'binary_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

model.fit(x_train, y_train, epochs = 100, batch_size = 12)

#모델 결과-------------------------------
train_loss, train_acc = model.evaluate(x_train, y_train, verbose=2)
print('train_loss', train_loss)
print('train_acc', train_acc)
#출력 값 : 손실 loss의 값은 0.29 즉 29% 오차율을 의미
#출력 값 : 정확도 acc는 0.87 즉 87%의 정확도를 보이고 있다.

