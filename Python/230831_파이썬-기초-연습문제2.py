#10장 조건문 IF 연습문제
#리스트의 모든내용을 출력해주세요. 

fruit = ['사과', '오렌지']
vegetable = ['당근', '호박']
#위와 같은 리스트 두개를 만들고 유저로부터 카테고리와 상품명을 입력받아
category = input("등록할 카테고리는? (과일, 채소): ")
thing = input("등록할 {}을 입력해: ".format(category))
#카테고리가 과일일때는 fauit 리스트에
#카테고리가 채소일때는 vegetable 리스트에 상품을 추가하고
if category == '과일':
    if thing not in fruit:
        fruit.append(thing)
    print(fruit)
elif category == "채소":
    if thing in vegetable:
        print("등록된 채소")
    else:
        print("등록된 채소 없음")
else:
    print("그런 건 없습니다")
#단, 카테고리명이 채소나 과일이 아닐경우 “ 존재하지 않는 카테고리입니다. “ 이미 등록되어있는 경우 “이미등록된 과일입니다.” or “이미 등록등록된 채소입니다" 를 출력해주세요.

#코드 실행 성공!

##### 11장 반복문 for 연습문제1
#y = {"math":70, "science": 80, "english":20}의 값의 모든 요소에 10을 더하여 저장한 뒤 출력하라.
y = {"math": 70, "science": 80, "english": 20}
for key in y:
    y[key] += 10
print(y)

#결과값 : {'math': 80, 'science': 90, 'english': 30}
#key를 출력하고 10을 더한다는 개념

##### 11장 반복문 for 연습문제2
x = int(input("몇단을 출력하겠는가: "))
for i in range(1, 10):
  print("{0} * {1} = {2}".format(x, i, x * i))

#결과값 : 몇단을 출력하겠는가 출력 되며, 숫자 기입, 기입한 숫자에 1-9의 숫자를 곱함.

##### 11장 반복문 for 연습문제3
#word = ["school", "game", "piano", "science", "hotel", "mountian"] 중 글자수가 6글자 이상인 문자를 모아 새로운 리스트를 생성하세요.
word = ["school", "game", "piano", "science", "hotel", "mountain"]
newword = []
#기존 워드를 정의하고 새로운 프레임에 넣을 준비.
for i in word:
  if len(i) >= 6:
    newword.append(i)
#정의한 워드에 len 길이 함수 6글자 이상을 if문 추가
print(newword)
#['school', 'science', 'mountain'] 6자 이상이 출력 되며 수행 끝

##### 11장 반복문 for 연습문제4
#구구단을 1단부터 9단까지 출력하세요.
for i in range(1, 10):
    for j in range(1, 10):
        print(f"{i} * {j} = {i * j}")
    print()
#결과값 i와 j의 항목이 1-9까지 출력되어 print에 곱해져서 출력 {}의 위치가 중요!

##### 11장 반복문 for 연습문제5
#[3, 6, 9, 10, -7, 5] 리스트를 sort와 같은 함수를 사용하지 말고 for문을 활용하여 오른차순으로 정렬해주세요
sort_list = [3, 6, 9, 10, -7, 5]

for i in range(len(sort_list)):
    min_index = i
    for j in range(i + 1, len(sort_list)):
        if sort_list[j] < sort_list[min_index]:
            min_index = j

    sort_list[i], sort_list[min_index] = sort_list[min_index], sort_list[i]

print(sort_list)
#결과 값    
    
##### 11장 반복문 for 연습문제6
#1-100까지 숫자 중
# 3과 5의 공배 수일 경우 "3과 5의 공배수"
# 나머지 숫자중 3의 배수일 경우 "3의 배수"
# 나머지 숫자중 5의 배수일경우 "5의 배수"
# 모두 해당하지 않을 경우 그냥 숫자를 출력하세요.
for i in range(1, 101):
    if i % 3 == 0 and i % 5 == 0:
        print("3과 5의 공배수")

    elif i % 3 == 0:
        print("3의 배수")

    elif i % 5 == 0:
        print("5의 배수")

    else:
        print(i)


#####12장 반복문 while 연습문제1
#1부터 49사이의 랜덤한 6자리 숫자를 출력하라.
import random

def generate_lotto_numbers():
    return random.sample(range(1, 50), 6)

lotto_numbers = generate_lotto_numbers()
print("복권 번호:", lotto_numbers)
#결과 값 : 복권번호 : [여기에 랜덤 숫자 표기 됨]

#####12장 반복문 while 연습문제2
#random 모듈을 사용해 가위, 바위, 보 게임을 만들어라.
user = 1
computer = 0
word = ["가위", "바위", "보"]
total = - 1
win = 0

while user in [1, 2, 3]:

    if user == 1:
        if computer == 3:
            win = win + 1
    elif user == 2:
        if computer == 1:
            win = win + 1
    elif user == 3:
        if computer == 2:
            win = win + 1

    if computer != 0:
      print("유저 : {}, 컴퓨터 : {}".format(word[user-1], word[computer-1]))

    total = total + 1

    user = int(input("가위(1), 바위(2), 보(3)를 입력 해주세요! : "))
    computer = random.randint(1, 3)

print("가위 바위 보 게임이 종료되었습니다. (전체:{}, 승:{})".format(total, win))


#####13장 리스트 응용 연습문제1
#word = ["school", "game", "piano", "science", "hotel", "mountian"] 중 리스트 컴프리핸션을 사용해 글자수가 6글자 이상인 문자를 모아 새로운 리스트를 생성하세요.
word = ["school", "game", "piano", "science", "hotel", "mountain"]
new_list = [ i for i in word if len(i) >= 6]
print(new_list)
#결과 값 : ['school', 'science', 'mountain']
#해석 : word에서 6자리를 빼낸 것, i랑 j는 항목이다. 
#해석2 : 새 리스트 = [항목 for 항목 in 워드에서 if 항목 >= 6(6과 같거나 큰)] 출력하라(워드)


#####13장 리스트 응용 연습문제2
#word = ["school", "game", "piano", "science", "hotel", "mountian"] 중 리스트 컴프리핸션을 사용해 리스트의 글자수가 들어간 새로운 리스트를 생성하세요.
word = ["school", "game", "piano", "science", "hotel", "mountain"]
lengths = [ len(i) for i in word]
print(lengths)
#결과 값 : [6, 4, 5, 7, 5, 8]
#해석 : len함수를 사용해 글자 수 작성.
#해석2 : 새 리스트 = [len(숫자 세기 함수) (항목) for (항목) in 워드에서] 출력하라(워드)

#####13장 리스트 응용 연습문제3
a = [[10, 20], [30, 40], [50, 60]]
b = [[2, 3], [4, 5], [6, 7]]
# 두 리스트를 곱해 새로운 리스트를 만드세요.

c = []

for i in range(3):
  temp = []
  for j in range(2):
    temp.append(a[i][j] * b[i][j])
  c.append(temp)

print(c)

#결과 값 : [[20, 60], [120, 200], [300, 420]]


##### 14장 break와 continue 연습문제1
#user = int(input("숫자를 입력하세요."))
# cnt = 0
# while True:
# (여기)
# 코드의 while 문을 완성하여 사용자가 입력한 숫자만큼 출력해주세요. (break 사용)
user = int(input("숫자를 입력하세요."))
cnt = 0
while True:
    print(cnt)
    cnt += 1

    if cnt == user:
        break

#결과 값 : 숫자를 입력하라는 메세지가 뜬 뒤에 입력 값만큼 리스트가 출력 되고 중단된다.

##### 14장 break와 continue 연습문제2
# user= int(input("숫자를 입력하세요."))
# for i in range(user+1):
# (여기 코드를 완성해 주세요)
# print(i)
# 코드의 for 문을 완성하여 사용하여 사용자가 입력한 숫자까지의 짝수를 출력하기. (continue 사용)
user= int(input("숫자를 입력하세요."))
for i in range(user+1):
  if i % 2 == 1:
    continue
  print(i)

#결과 값 : 숫자를 입력하라는 메세지가 뜬 뒤에 입력 값 i의  2를 나눈 값이 0 1이면 홀수로 인식한다.


##### 15장 함수 연습문제
#가변인수와 고정인수를 사용해 모든값을 더하거나 곱하는 함수 작성
def calc(operator, *numbers):           #operator는 문자열이고 numbers는 숫자의 목록.

  if operator == "+":                   #operator가 "+"일 때 다음 코드를 실행

    result = 0

    for num in numbers:
      result += num

    return result

  elif operator == "*":                #operator가 "*"일 때 다음 코드를 실행

    result = 1

    for num in numbers:
      result *= num

    return result

calc("+", 1, 2, 3, 4, 5)     #결과 값 : 15
calc("*", 1, 2, 3, 4, 5)     #결과 값 : 120

##### 15장 함수 연습문제 재귀함수
#양의정수 n을 인자로받아, 1부터 n까지 합을구하는 재귀함수 구현
def f_sum(a):
  if a == 1:
    return a                # a가 1일 때는 a를 반환.
  else:
    return a + f_sum(a-1)   #a가 1이 아닐 때는 a와 f_sum(a-1)의 합을 반환하는걸 추가

f_sum(5)                    #결과 값 : 15


##### 16장 객체와 클래스 연습문제
#Car 클래스를 만드세요
#객체 생성시 차이름, 배기량, 생산년도 입력받고 인스턴스 속성으로 만들어주세요 - 차이름, 배기량, 생산년도는 직접 변경하지 못합니다
#차이름을 확인하는 함수와 변경하는 함수를 만드세요
#배기량에 따라 
#1000CC 보다 작으면 소형
#1000CC 이상 2000CC 이하 중형
#2000CC 보다크면 대형을 출력하는 인스턴스함수를 만드세요

#객체 생성시마다 등록된 차량 갯수를 기록하는 클래스속성을 만들어주세요 - 총 등록된 차량개수를 출력하는 클래스 함수를 만드세요

class Car:                                         #Car이라는 이름의 클래스를 정의
    count = 0                                      #클래스 변수 count를 0으로 초기화

    @staticmethod
    def getCount():                                #getCount 이름의 정적 메서드를 정의
        print("총 등록된 차량개수 : ", Car.count)

    def __init__(self, name,cc,year):
        self.__name = name                  #변수 __name에 name 할당
        self.__cc = cc                      #변수 __cc에 cc 할당
        self.__year = year                  #변수 __year에 year 할당
        Car.count += 1                      #Car.count에 변수 1 증가

    def getName(self):
        print(self.__name)

    def changeName(self, name):
        self.__name = name
        print(self.__name)

    def getKind(self):
        if self.__cc < 1000:
            print("소형차")
        elif 1000 <= self.__cc <= 2000:
            print("중형차")
        else:
            print("대형차")


car1 = Car('aaa',500,1986)
car2 = Car('bbb',1500,1986)

car1.changeName('ccc') #결과 값 : ccc
car1.getKind()         #결과 값 : 소형차
car2.getKind()         #결과 값 : 중형차
Car.getCount()         #결과 값 : 총 등록된 차량개수 :  2


##### 17장 예외처리 연습문제
#매개변수로 전달받은 숫자의 구구단을 출력해주는 함수를 만드는데 매개변수로 1~9 이외의 숫자를 전달하면 NotNumberException 을 발생시켜 주세요
class NotNumberException(Exception):
    def __init__(self):
        super().__init__("잘못된 숫자입니다.")

def gugudan(num):

    if not (1 <= num <= 9):
        raise NotNumberException             #num이 1 이상 9 이하가 아니면 NotNumberException 예외를 발생

    for i in range(1, 10):                   #num과 i의 곱을 출력하는 코드.
        print("{} X {} = {}".format(num, i, num * i))

num = int(input("구구단을 출력할 숫자를 입력하세요: "))
gugudan(num)

#결과 값 : 1~9면 정상 구구단이 작동.
#결과 값 : 그외의 숫자가 입력되면 "잘못된 숫자입니다." 출력