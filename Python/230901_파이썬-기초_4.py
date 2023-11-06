##### 15장 함수
#def 함수 시작전에 들어감
#def 뒤엔 사용할 함수가 들어감

def func(a, b):
  print("함수입니다.")
  return a+b

func_test = func(1, 2)
print(func_test)

#출력값 : 함수입니다.
#출력값 : 3


#인자와 반환값이 없는 함수
def func():
  print("HI FFF")
func()

#출력값 : HI FFF

#인자는 있으나 반환값이 없는 함수
def func11(name):
  print("Hello, " + name)

func11("Hello, Tom")
#출력값 : HI FFF

#인자와 반환값이 있는 함수
def func(a, b):
  return a+b
func(5, 4)
#출력값 : 9

#값을 여러개 반환
def func(a, b):
  return a+b, a-b
func(5, 4)
#출력값 : (9, 1)

#변수의 유효범위
a = 5

def func1():
  a = 1
  print(a)

func1()
print(a)
#출력값 : func1()의 값은 1가 출력 된다.
#출력값 : print(a)의 값은 5가 출력 된다.

a = 5
def func2():
  print(a)
func2()
#출력값 : func2()의 값은 5가 출력 된다.

##리스트와 찾고싶은 값을 모두 입력하면 입력한 값의 인덱스(위치) 를 리턴해주는 함수만들기
def allindex(lis, val):
  idx = []

  for i, v in enumerate(lis):
    if v == val:
      idx.append(i)

  return

idxlis = [1, 2, 3, 1, 4, 2, 1]
allindex(lis, 1)
#출력값 : [0, 3, 6]


##함수응용
#인자값에 리스트 사용
def func(a, b, c):
  print(a, b, c)

x = [1, 2, 3]
func(*x)
#출력값 : 1 2 3

#가변인수
def func(*args):
  for arg in args:
    print(arg, end="")
  print("")

func(1) #출력값 : 1
func() #출력값 :
func(1, 2, 3, 4, 5) #출력값 :12345


#가변인수와 고정인수 같이 사용
def func(a, *args):
  print(a, end="")
  for arg in args:
    print(arg, end="")

func(100, 1, 2, 3, 4, 5) #출력값 :10012345

#키워드 인수
def func(email, name):
    print("이메일 : ", email)
    print("이름 : ", name)

func(email="yoonsuk.choi93@gmail.com", name="choi") # 키워드 인수에 값을 넣는 방식 살펴보기
func(name="choi", email="yoonsuk.choi93@gmail.com") # 입력하는 순서가 달라도 OK!
#출력값 : 이메일 :  yoonsuk.choi93@gmail.com
#출력값 : 이름 :  choi
#출력값 : 이메일 :  yoonsuk.choi93@gmail.com
#출력값 : 이름 :  choi
#매칭 이름에 따라 분배된다.


#가변인수와 키워드 인수
def func(**kwargs): # 가변 키워드 인수를 사용하도록 함수를 정의하는 방식 살펴보기
    print("이메일 : ", kwargs["email"])
    print("이름 : ", kwargs["name"])

func(email="yoonsuk.choi93@gmail.com", name="choi")
#출력값 : 이메일 :  yoonsuk.choi93@gmail.com
#출력값 : 이름 :  choi

#매개변수 초기값
def func(email, name, age=31): # 함수를 정의할 때 매개변수의 초기값을 알려줄 수 있음
  print("이메일:", email)
  print("이름:", name)
  print("나이:", age)

func(email="yoonsuk.choi93@gmail.com", name="choi") # age 인자의 값을 입력하지 않은 경우 미리 함수에서 지정한 초기값을 사용
func(email="yoonsuk.choi93@gmail.com", name="choi", age=29)

#출력값 : 이메일: yoonsuk.choi93@gmail.com
#출력값 : 이름: choi
#출력값 : 나이: 31

#출력값 : 이메일: yoonsuk.choi93@gmail.com
#출력값 : 이름: choi
#출력값 : 나이: 29


#재귀함수
# 함수 안에서 자기자신을 호출하는 방식
# RecursionError: 재귀의 깊이가 일정길이를 초과하면 오류가 발생 (default: 1000회)

def test():
  print("재귀함수 소환!")
  test() # 자기자신을 호출
#출력값 : 재귀함수 소환!---------이 단어가 무수히 출력된다.

#재귀함수 종료조건을 넣어보자.
def test(end):
  if end == 0: # 반복이 멈추어야 하는 순간에 if문을 사용하여 재귀함수을 호출하지 못하도록 합니다
    return
  print("재귀함수 소환!", end)
  end -= 1
  test(end)

test(7)
#출력값 : 재귀함수 소환! 7 부터 1까지만 반복 되고 종료 된다.

#재귀함수로 팩토리얼 구하기 (응용)
def factorial(n):
  if n == 1:
    return 1
  return n * factorial(n-1) # n이 1보다 크면 n과 n-1의 팩토리얼을 곱한 결과를 반환한다.

factorial(5)
#출력값 : 120


##람다표현식
#람다 표현식은 익명 함수를 만드는 방법 (익명 함수: 이름이 없는 함수)
#주로 다른 함수의 인수로 함수를 넣어야 하는 경우 사용
def plus_ten(x):
  return x + 10

plus_ten(1)
#출력값 : 11

#람다표현식 바로 호출하기

##map - 반복되는 자료형의 값들을 함수를 이용하여 값을 가공
#map 함수
#람다 표현식에서는 elif를 사용할 수 없다. 대신 if와 else를 사용하여 동일한 결과를 만들 수 있다.
#filter - 반복되는 자료형의 값들을 함수를 하여 참인 것만 걸러냄

def return_a(x): #return_a는 x라는 함수를 정의
  return x + 10  #x와 10을 더한 결과

return_a(1)      #함수 호출
#출력값 : 11

#간략하게 표현!
return_a = lambda x: x+10 #: return_a는 lambda x: x+10다 정의
return_a(1)
#출력값 : 11



##### 16장 객체와 클래스
#객체    : 속성(변수)과 행동(함수)으로 구성된 대상
#클래스  : 객체를 만들기 위한 도구 (문법)
#클래스  : 코드의 규모가 커지는 경우 코드를 정리하기에 유용한 문법.
#실무에서는 규모가 있는 코드를 작성하는 경우 대부분 클래스를 사용하여 코드가 작성되기 때문에 클래스의 문법 구조와 사용 방법을 숙지해야 편하다.
#예시
class Dog: # 클래스 이름, 보통 영어 대문자로 시작.

  def __init__(self, name, color):  # 생성자 함수
    self.hungry = 0 # 인스턴스 속성, self.속성이름 양식으로 만든다. 클래스 안에서 가져와 사용할 수 있는 변수입니다.
    self.name = name
    self.color = color
    # print("생성자 함수 실행")

  def eat(self): # 인스턴스 매서드, (self는 Dog 클래스에서 생성되는 객체(인스턴스) 자신을 의미.)
    self.hungry -= 10
    print("밥먹음", self.hungry)

  def walk(self):
    self.hungry += 10
    print("산책 ", self.hungry)

choco = Dog("choco", "black") # 객체 생성 ("인스턴스 생성"), 객체 생성시 생성자 함수가 자동으로 실행된다. # 여기에 들어간 인자는 __init__(self, arg1, arg2)에 각각 들어간다.(중요)
jjong = Dog("jjong", "white")

# 메서드를 실행 
choco.eat()  #출력값 : 밥먹음 -10
choco.eat()  #출력값 : 밥먹음 -20
choco.walk() #출력값 : 산책  -10

# 속성에 접근
print(choco.hungry) #출력값 : -10
print(jjong.hungry) #출력값 : 0


#비공개 속성 (private attribute)
class Dog:

  def __init__(self, name, color):
    self.name = name
    self.color = color
    self.__hungry = 0   # 비공개 속성, 외부에서 속성에 접근하지 못하게 차단. (클래스 안에서만 사용 가능)

  def eat(self):
    if self.__hungry <= 0:
      print("배가 너무 불러요!")
    else:
      self.__hungry -= 10
      print("밥먹음", self.__hungry)

  def walk(self):
    self.__hungry += 10
    print("산책 ", self.__hungry)

  def condition(self):
    print("{} 배고픔 : {}".format(self.name, self.__hungry))

mery = Dog("mery", "black") #입력상자

mery.eat()       #출력값 : 배가 너무 불러요!
mery.walk()      #출력값 : 산책  10
mery.walk()      #출력값 : 산책  20
mery.condition() #출력값 : mery 배고픔 : 20


#클래스 속성 (class attribute)
# 모든 객체(인스턴스)가 공유하는 속성
# 객체 없이 클래스명으로 접근 가능
#예시
class Dog:

  dog_count = 0 # 클래스 속성

  def __init__(self, name, color):
    self.name = name
    self.color = color
    Dog.dog_count += 1 # 클래스 속성 접근

  def dogCount(self):
    print("총 강아지는 : ", Dog.dog_count)

hello = Dog("hello", "black")
hello.dogCount() #출력값 : 총 강아지는 :  1 
happy = Dog("happy", "black")
hello.dogCount() #출력값 : 총 강아지는 :  2

#정적 메서드 (static method, class method)
#객체를 생성하지 않아도, 클래스명으로 접근이 가능한 메서드
#인스턴스 속성 및 인스턴스 메서드는 객체를 생성하지 않으면 접근 불가
#예시
class Calc:

  @staticmethod
  def add(a,b):
    print(a+b)

  def test(self):
    print("test")

Calc.add(10, 20) #출력값 : 30


##상속
#공통되는 내용은 부모 클래스로 만들고
#클래스(자식)를 만들 때 공통되는 내용을 부모 클래스로부터 상속
#예시
class Animal:

    def __init__(self):
        self.hungry = 0

    def eat(self):
        self.hungry -= 10
        print("밥먹음 ", self.hungry)

    def walk(self):
        self.hungry += 10
        print("산책 ", self.hungry)

class Dog(Animal): # 괄호 안에 부모 클래스 이름 입력

    def __init__(self):
        super().__init__()  # __init__ 생성자 함수를 사용하는 경우 super().__init__() 추가, super()로 부모 클래스의 __init__()을 수행
        # print("dog")

    def sound(self):
        print("멍멍")

class Cat(Animal):

    def __init__(self):
        super().__init__()

    def sound(self):
        print("야옹")

#Dog()
dog.sound()  #출력값 : 멍멍
dog.walk()  #출력값 : 산책 10
dog.walk()  #출력값 : 산책 20

#Cat()
cat.sound()  #출력값 : 야옹
cat.walk()  #출력값 : 산책 10
cat.walk()  #출력값 : 산책 20

#오버라이딩 : 상위 클라스(부모)의 기능을 물려받고 일부 기능 수정
class Dog(Animal): # 괄호 안에 부모 클래스 이름 입력

    def __init__(self):
        super().__init__()  # __init__ 생성자 함수를 사용하는 경우 super().__init__() 추가, super()로 부모 클래스의 __init__()을 수행
        # pass

    def sound(self):
        print("멍멍")

    def eat(self): # 오버라이딩, 부모의 기능을 물려받고 일부 기능을 수정
      print("으르르릉")
      super().eat() # 부모 클래스에서 가져온 코드 실행
      print("왈왈왈")

dog.eat()  #출력값 : 으르르릉
           #출력값 : 밥먹음  -40
           #출력값 : 왈왈왈


##추상클래스
#미구현 추상메소드를 하나 이상 가진다.
#자식클래스에서 해당 추상 메소드를 반드시 구현하도록 강제.
#자식클래스는 추상 메소드를 구현하지 않아도 클래스 코드를 작성할 때 에러는 발생하지 않으나, 객체 생성시 에러가 발생.

from abc import *   # abc 모듈 임포트 필요!! (필요하면 앞에 ! 붇이고~)

class Animal(metaclass=ABCMeta):

    def __init__(self):
        self.hungry = 0

    def eat(self):
        self.hungry -= 10
        print("밥먹음 ", self.hungry)
    def walk(self):
        self.hungry += 10
        print("산책 ", self.hungry)

    @abstractmethod
    def sound(self):
        pass

class Dog(Animal):

    def __init__(self):
        super().__init__()

    # sound() 메서드가 없는 경우 객체 생성시 에러 발생
    def sound(self):
        print("멍멍")

#dog = Dog() #출력값 : Dog 클래스에서 sound() 메서드를 주석처리하는 경우 이 코드에서 TypeError가 발생.
dog.sound()  #출력값 : 멍 멍


##static method, class method 차이점
class Animal:

  type = "동물"

  @staticmethod
  def getType1():
    return Animal.type

  @classmethod
  def getType2(cls):
    return cls.type

  def __init__(self):
    self.hungry = 0

class Dog(Animal):

  type = "강아지"

Dog.getType1()  # staticmethod -> 부모 클래스의 클래스 속성 값으로 '고정(static; 변화 없는, 이동하지 않는)'
Dog.getType2()  # classmethod -> 자식 클래스의 클래스 속성 값으로 변경되어 들어감

Dog.getType1()  #출력값 : 동물
Dog.getType2()  #출력값 : 강아지


##### 17장 예외처리 try와 except
#코드를 실행하다가 예외를 만나면(=에러가 발생하면, 오류가 발생하면) 코드 전체가 실행을 중단합니다.
#예외가 발생하는 경우 코드가 계속 정상적으로 동작하도록 "예외 처리"가 필요합니다.
#예시
try:
  print("test1")
  print(10 / 0) # 실행할코드
  print("test2")
except:
  print("예외오류발생") # 예외발생시 코드
#출력값 : test1
#출력값 : 예외오류발생

#특정 예외만 처리
x = [1, 2, 3]
try:
  print(10/0)
  x[5]
except ZeroDivisionError as e:           # 0으로 나눗셈을 하는 경우 발생
  print("숫자를 0으로 나눌 수 없음", e)
except IndexError as e:                  # 인덱스 범위를 벗어나는 경우 발생
  print("잘못된 인덱스", e)
#출력값 : 숫자를 0으로 나눌 수 없음 division by zero

#else와 finally
# else : 오류가 발생하지 않았을 때만 동작
# finally : 오류 발생 여부 상관 없이 무조건 동작

#예외 발생시키기 raise
#예시1
try:
  print(10 / 0)
  # print()
except:
  print("예외오류발생")
else:
  print("오류발생하지 않음")
finally:                    # 무조건 동작 = except로 처리되지 않은 에러가 발생해도 무조건 실행한다는 의미
  print("무조건 실행")

#출력값 : 예외오류발생
#출력값 : 무조건 실행

#예시2
try:
  raise Exception("예외강제발생")
except Exception as e:
  print("예외 발생", e)

class MyError(Exception):
  def __init__(self):
    super().__init__("나의오류")

try:
  raise MyError
except Exception as e:
  print("예외발생", e)
#출력값 : 예외 발생 예외강제발생
#출력값 : 예외발생 나의오류


##### 18장 모듈과 패키지
#모듈과 패키지 : 변수, 함수, 클래스 등을 모아놓은 스크립트 파일

# 현재 경로(=디렉터리, 폴더)
#pwd
# 현재 경로에 존재하는 파일 및 폴더 목록
#ls
# calc.py
# 모듈 calc.py 를 파일명으로 해서 현재 경로에 저장

name = "calc"

def add(a,b):
  return a+b

def sub(a,b):
  return a-b
# main.py

from calc import add, sub

print(add(5, 6))
print(sub(5, 6))

##시작점 확인 __name__
#파이썬은 어떤 모듈에서든 실행 가능
#해당 모듈이 시작점일 경우 __name__ 의 값은 "__main__"
#시작점이 아닐 경우 __name__는 해당 모듈의 모듈명(파일명)
calc.py # 모듈 calc.py 를 파일명으로 해서 현재 경로에 저장

name = "calc"

def add(a,b):
   return a+b

def sub(a,b):
   return a-b

if __name__ == '__main__':
  print("시작점")

##패키지 : 여러가지 모듈을 모아놓은 것
# pkcalc/calc.py
# 현재 위치에 pkcalc 폴더를 만들고 그 안에 calc.py 를 저장

def add(a, b):
  return a+b

def sub(a, b):
  return a-b

#패키지명으로 import (__init__.py)
# main.py

from pkcalc.calc import name, add

print(name)
print(add(5, 6))

#모듈과 패키지를 찾는 경로
import sys
print(sys.path)

# sys.path.append("path")
실습1


##### 19장 데코레이터
##데코레이터
#일급함수 (일급객체, first class function)
#함수가 변수처럼 다루어지는 경우, 이를 일급함수라고 합니다.

#<일급함수의 조건>
#함수를 변수에 담을 수 있고,
#함수를 매개변수로 전달할 수 있고,
#함수를 리턴값(반환값)으로 사용할 수 있어야 합니다.
#파이썬에서는 함수가 일급함수 조건을 만족합니다.

##클로저
#내부 함수를 결과로 반환할 때, 그 내부 함수를 클로저라고 합니다.

#파일 입출력
# 파일 쓰기

file = open("file.txt", "w")  # 파일을 쓰기 모드("w")로 엽니다.
file.write("First File")      # 문자열을 파일에 저장합니다.
file.close()                  # 파일을 닫습니다. (닫지 않는 경우 계속 메모리의 공간을 차지합니다.)

#예시문
#cat file.txt

# 파일 읽기

file = open("file.txt", "r")  # 파일을 읽기모드("r")로 엽니다.
text = file.read()            # 파일에서 내용을 읽습니다.
print(text)
file.close()                  # 파일을 닫습니다.

#with를 사용해 자동으로 파일 객체 닫기
with open("file.txt", "r") as file:
  text = file.read()
  print(text)
print()

#pickle 모듈을 이용한 리스트 파일에 저장하기
import pickle

text = ["First File", "Second Line"]

with open("data.p", "wb") as file:  # data 파일을 바이너리 쓰기 모드로 열기
  pickle.dump(text, file)

import pickle

with open("data.p", "rb") as file:  # data 파일을 바이너리 읽기 모드로 열기, 바이너리 파일의 읽는 속도가 더 빠릅니다. 데이터 양이 많은 경우 유용합니다.
  data = pickle.load(file)
  print(data)


#pickle 모듈을 이용한 다양한 자료형 저장하기
import pickle

name = "tom"
age = 24
address = "서울시 마포구"
scores = {"python": 90, "deeplearning": 95, "database": 85}

with open("data2.p", "wb") as file:
  pickle.dump(name, file)
  pickle.dump(age, file)
  pickle.dump(address, file)
  pickle.dump(scores, file)


#pickle 모듈을 이용한 다양한 자료형 불러오기
import pickle

with open("data2.p", "rb") as file:
  name2 = pickle.load(file)
  age2 = pickle.load(file)
  address2 = pickle.load(file)
  scores2 = pickle.load(file)

print(name, age, address, scores)
