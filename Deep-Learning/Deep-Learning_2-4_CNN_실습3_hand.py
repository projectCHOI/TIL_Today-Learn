# Deep-Learning_CNN_실습3_hand
# 가위, 바위, 보 손동작 제스처 이미지를 구분하는 모델 만들기

#데이터 불러오기-------------------------------
import tensorflow as tf
# import keras_preprocessing
# from keras_preprocessing import image

import urllib.request
import os
import zipfile

url1=  'https://storage.googleapis.com/download.tensorflow.org/data/rps.zip '
urllib.request.urlretrieve(url1, 'rps.zip')
url2 =  'https://storage.googleapis.com/download.tensorflow.org/data/rps-test-set.zip '
urllib.request.urlretrieve(url2, 'rps-test-set.zip')

local_zip = 'rps.zip'
zip_ref = zipfile.ZipFile(local_zip, 'r')
zip_ref.extractall('tmp/')
zip_ref.close()

local_zip = 'rps-test-set.zip'
zip_ref = zipfile.ZipFile(local_zip, 'r')
zip_ref.extractall('tmp/')
zip_ref.close()

# 2. Data Preprocessing
rock_dir = os.path.join('./tmp/rps/rock')
paper_dir = os.path.join('./tmp/rps/paper')
scissors_dir = os.path.join('./tmp/rps/scissors')

print('total training rock images:', len(os.listdir(rock_dir)))
print('total training paper images:', len(os.listdir(paper_dir)))
print('total training scissors images:', len(os.listdir(scissors_dir)))

rock_files = os.listdir(rock_dir)
paper_files = os.listdir(paper_dir)
scissors_files = os.listdir(scissors_dir)

#데이터 확인하기-------------------------------
# 필요하면 설치 matplotlib inline

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

pic_index = 2

next_rock = [os.path.join(rock_dir, fname)
                for fname in rock_files[pic_index-2:pic_index]]
next_paper = [os.path.join(paper_dir, fname)
                for fname in paper_files[pic_index-2:pic_index]]
next_scissors = [os.path.join(scissors_dir, fname)
                for fname in scissors_files[pic_index-2:pic_index]]

for i, img_path in enumerate(next_rock+next_paper+next_scissors):
  #print(img_path)
  img = mpimg.imread(img_path)
  plt.imshow(img)
  plt.axis('Off')
  plt.show()

# keras_preprocessing에 ImageDataGenerator를 사용#-------------------------------
#pip install keras_preprocessing #필요하면 사용

# ImageDataGenerator를 사용해서 tmp/rps/ 와 tmp/rps-test-set/에 있는 데이터를 불러오기
# 학습데이터 형태로 변경
import keras_preprocessing
from keras_preprocessing.image import ImageDataGenerator

TRAINING_DIR = "tmp/rps/"
TEST_DIR= "tmp/rps-test-set/"

training_datagen = ImageDataGenerator (rescale = 1./255)
train_generator = training_datagen.flow_from_directory (TRAINING_DIR,
                                                        target_size=(150,150),class_mode='categorical')

test_datagen = ImageDataGenerator (rescale=1./255)
test_generator = training_datagen.flow_from_directory (TEST_DIR,
                                                       target_size=(150,150),class_mode='categorical')

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, BatchNormalization

model = Sequential()

model.add(Conv2D(64, (3,3), input_shape = (150,150,3), activation = 'relu')) # filter, kernel size, strides, activation
model.add(MaxPooling2D (2,2))
model.add(Flatten())
model.add(Dense (128, activation='relu'))
model.add(BatchNormalization())

model.add(Dense(3, activation = 'softmax'))

model.compile(loss = 'categorical_crossentropy', optimizer = 'rmsprop', metrics=['acc'])

model.fit(train_generator, epochs = 5)

test_loss, test_acc = model.evaluate(test_generator, verbose=2)

print('\nTest loss:', test_loss)
print('\nTest accuracy:', test_acc)
#출력 값 : 손실 loss의 값은 3.98 
#출력 값 : 정확도 acc는 0.46 즉 46%의 정확도를 보이고 있다.

#모델 성능 개선-------------------------------
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, BatchNormalization, Dropout

model = Sequential()

model.add(Conv2D (64, (3,3), input_shape = (150,150,3), activation = 'relu')) # filter, kernel size, strides, activation
model.add(MaxPooling2D(2,2))
model.add(Conv2D (64, (3,3), activation = 'relu'))
model.add(MaxPooling2D (2,2))
model.add(Conv2D (64, (3,3), activation = 'relu'))
model.add(MaxPooling2D (2,2))
model.add(Flatten())
model.add(Dropout (0.5))
model.add(Dense (128, activation='relu'))
model.add(BatchNormalization())
model.add(Dense (3, activation = 'softmax'))

model.compile(loss = 'categorical_crossentropy', optimizer = 'rmsprop', metrics=['acc'])
model.fit(train_generator, epochs = 5)

#모델 결과-------------------------------
test_loss, test_acc = model.evaluate(test_generator, verbose=2)

print('\nTest loss:',test_loss)
print('\nTest accuracy:', test_acc)
#출력 값 : 손실 loss의 값은 0.52 
#출력 값 : 정확도 acc는 0.87 즉 87%의 정확도를 보이고 있다.

