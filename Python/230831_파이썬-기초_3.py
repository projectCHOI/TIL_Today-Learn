#for : 반복 횟수가 정해진 경우 사용
#while : 반복 횟수가 정해지지 않은 경우 사용

##### 10장 조건문 IF 
#조건문 IF 특정 조건에서 코드를 실행하는 것.
x = 10
if x == 10:
  pass
#if문 들여쓰기
x = 10
if x == 10:
    print("스페이스 4칸")
    print("탭 1칸")
#결과 값. 그대로 출력됨

#다양한 조건들[>, <, =]
#  if x > 3: [x는3보다 크다]
#  if x < 3: [x는 3보다 작다]
#  if x > 3 and x < 10: [x는 3보다 크고 10보단 작다]
#  if 5 < x < 20: [x는 5보다 크고 20보단 작다]

##### 11장 반복문 for
#반복문 for : 값이 여러개인 자료형이나 변수
for i in range(0, 10) :
  print("현재값 : " ,i)
#결과 값. 0부터 9까지의 숫자 출력

#for문과 range
for i in range(0,10):
  print(i)
#결과 값. 0부터 9까지의 숫자 출력
for i in range(10,0, -1):
  print(i)
#결과 값. 10부터 1까지의 숫자 출력

#for문과 시퀸스객체
a= {"name":  "tom", "math": 80, "english": 70}
for i in a:
  print(i,end=" ")
  print(a[i])
#결과 값.객체의 속성 불러 오기 수행

#for문으로 입력한 횟수만큼 반복하기
count = int(input("반복 횟수"))
for i in range(count):
  print('hi wolf', i)
#결과 값. 반복횟수 기입에 따른 wolf 출력

#enumerate 사용하여 index 접근
a = [1,2,3,4,5,6,7,]
for idx, val in enumerate(a):
  print(idx, val, sep=",")
  
#for문 중첩
for i in range(0, 10, 2) :
    print("*********", i)
    for i in range(0, 5):
        print("j:","j")


##### 12장 반복문 while
#반복문 while = 조건에 따라 반복하는 함수
i = 0
while i < 10:
    print("현재값 :", i)
#결과 값. i값이 0이기 때문에 무한히 반복 된다.

#while으로 입력한 횟수만큼 반복하기
count = int(input("반복횟수?"))

i = 0
while i < count:

    print("입력한 횟수만큼 반복")
    i += 1

#결과 값. 반복횟수의 입력에 따라 print의 값이 출력된다.

#특정 조건이 맞을때까지 반복하는 방법
#숫자 5를 입력할 때까지 반복
i = 0

while i != 5:
    i = int(input("5를 입력하면 반복이 중단됩니다."))

print("중단!")
#계속되는 숫자 입력 코드가 작성되며, 5를 입력하면 작업이 중단 됨

#랜덤 모듈=숫자의 무작위 출력
import random
random.randint(1,50)
#결과 값. 1-50의 숫자중에 하나의 숫자를 출력한다.


##### 13장 리스트 응용
# max : 최대값
# min : 최소값
# sum : 합산
# split : 문자를 리스트로
# join : 리스트를 문자로

#TIP
text = "Hi"
#text = 출력값 : 'Hi'
#print(text)  = 출력값 : Hi
#해설 : text를 출력할 때 print를 사용하면 ''없이 출력 된다. 

#가장 큰수 구하기 [max : 최대값]
a = [32, 45, 2, 5, 76]
print(max(a))
#결과값 : 가장 큰 수가 출력된다. 76
#가장 작은수 구하기 [min : 최소값]
a = [32, 45, 2, 5, 76]
print(min(a))
#결과값 : 가장 작은 수가 출력된다. 2

#합계 구하기 [sum : 합산]
a = [32, 45, 2, 5, 76]
b = 0
for i in a:
  b += i
print(b)
#결과값 : a함수를 합치게 된다.

#split 함수 : 문자를 리스트로
fruit = "사과, 배, 옥수수, 당근"
fruit_list = fruit.split(",")
print(fruit_list)
#결과값 : ['사과', ' 배', ' 옥수수', ' 당근']

#join 함수 : 리스트를 문자로
fruit_list = ['사과', ' 배', ' 옥수수', ' 당근']
fruit = "".join(fruit_list)
print(fruit)

#리스트 컴프리헨션 (list comprehension)
a = [ i for i in range(10)]
print(a)
#결과값 : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

a = [ i + 5 for i in range(10)]
print(a)
#결과값 : [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

a = [ i * 3 for i in range(10)]
print(a)
#결과값 : [0, 3, 6, 9, 12, 15, 18, 21, 24, 27]

a = [ 0 for i in range(10)]
print(a)
#결과값 : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


#list[식 for 변수 in 리스트]
a = [i for i in range(10) if i % 2 ==0]
print(a)
#결과값 :[0, 2, 4, 6, 8]
a = [i for i in range(10) if i % 2 ==1]
print(a)
#결과값 :[1, 3, 5, 7, 9]


#list[식 for 변수(i) in 리스트(range) for 변수(j) in 리스트(range)]
a = [i * j  for i in range(2, 10) for j in range(1,10)]
print(a)
#결과값 :[2, 4, 6, 8, 10, 12, 14, 16, 18, 3, 6, 9, 12, 15, 18, 21, 24, 27, 4, 8, 12, 16, 20, 24, 28, 32, 36, 5, 10, 15, 20, 25, 30, 35, 40, 45, 6, 12, 18, 24, 30, 36, 42, 48, 54, 7, 14, 21, 28, 35, 42, 49, 56, 63, 8, 16, 24, 32, 40, 48, 56, 64, 72, 9, 18, 27, 36, 45, 54, 63, 72, 81]


#리스트를 딕셔너리로 변경
keys = ["name", "age", "address"]
users = ["tom", 20, "inheon"]
dicdic = {keys[i] : users[i] for i in range(0,3)}
dicdic
#결과값 : {'name': 'tom', 'age': 20, 'address': 'inheon'}

#zip (리스트1, 리스트2)
for x, y in zip([1, 2, 3], ["a", "b", "c"]):
  print(x, y)
#결과값 : 각 값이 매칭 되어 출력 된다.

keys = ["name", "age", "address"]
users = ["tom", 20, "inheon"]
dic = dict(zip(keys, users))
print(dic)
#결과값 : {'name': 'tom', 'age': 20, 'address': 'inheon'}

#2차원 리스트 응용
a = [[10,20],[30,40],[50,60]]
a
#결과값 : [[10, 20], [30, 40], [50, 60]]
#일반적인 출력 값이 나온다.

a[0]. append(10)
print(a)
#결과값 : [[10, 20, 10], [30, 40], [50, 60]]

a[0]. extend([20, 30])
print(a)
#결과값 : [[10, 20, 10, 20, 30], [30, 40], [50, 60]]

#for와 range 사용
a = [[10, 20], [30, 40], [50, 60]]
for i in range(len(a)):
  for j in range(len(a[i])):
    print(a[i][j], end=" ")
  print()

#결과값 : 아래와 같이 출력 된다.
# 10 20 
# 30 40 
# 50 60 
 
#for와 enumerate 사용
a = [[10, 20], [30, 40], [50, 60]]
for idx, val in enumerate(a):
    # print(idx)
    # print(val)
    for idx2, val2 in enumerate(val):
        print(idx, idx2, val2)
#결과값 : 아래와 같이 출력 된다.
# 0 0 10
# 0 1 20
# 1 0 30
# 1 1 40
# 2 0 50
# 2 1 60

##### 14장 break와 continue [브레이크, 커티뉴]
# break : foy, while를 중단
# continue : 이번 반복 중단후 처음으로 다시 반복

#for문에서의 예제
for i in range(5):
  if(i == 3):
    break
  print(i, end=" ")
#결과값 : 0 1 2  
#4까지 출력할 때 3 전에 멈춘다는 의미

#for에서의 continue 예제
for i in range(5):
  if(i == 3):
    continue
  print(i, end=" ")
#결과값 : 0 1 2 4
#출력할때 3을 빼고 다시 돌아서 출력 그래서 4도 출력 됨

#while에서의 break 예제
i = 0
while i < 30:
  if i == 20:
    break
  print(i, end="  ")
  i +=1
#결과값 :0  1  2  3  4  5  6  7  8  9  10  11  12  13  14  15  16  17  18  19  

#while에서의 continue 예제
i = 0
while i < 30:
  i +=1
  if i % 2 == 0:
    continue
  print(i, end= " ")
#결과값 : 1 3 5 7 9 11 13 15 17 19 21 23 25 27 29 