##### 1장 파이썬 시작
print("Hello world")
print("난 최윤석")

# 이것은 주석, 코드가 인식이 안된다. 코드의 메모 쓰기 좋다.

# 한줄주석
#print("주석처리")
#ctrl + / 하면 동시에 처리가능!


##### 2장 입력과 출력
x = input("입력하자 :")
print(x)


##### 3장 산술연산
#덧셈뺄셈
print("1-2")
print(1-2)
#곱하기
print("5 * 2")
print(5 * 2)
#나누기
print("5 / 2")
print(5 / 2)
#나누기 목
print("5 // 2")
print(5//2)
#나누기 나머지
print("9 % 2")
print(9 % 2)
#거듭제곱
print("2 ** 3")
print(2 ** 3)
#여러번 계산
print("(2 + 3) * 2")
print((2 + 3) * 2)


##### 4장 변수
x = 10
print(x)

print(x)
x = 20
print(x)

test1, 가, z = 10, 20, 30
print(test1, 가, z)

#비어있는 변수
x = None
print(x)

type(x)



##### 5장 Boolean과 비교, 논리연산자
print("Boolean형")
print("True 참")
print("False 거짓")

##비교연산자
print(3 > 1) #True
#<, > 비교, =같다
print(10 != 10) #False
#걑지 않다.
print(10 == 10) #True
#같다.

#논리연산자 (and)
print(True and True)
#그리고

#논리연산자 (or)
print(True or False)
#이거나

#논리연산자 (not) 논리값 뒤집기
print(not True) #False
print(not False) #True



##### 6장 문자형
first = "Hello, World"
print(first)
#일반적으로 출력 된다.

multi = """
Hello, World
Hello, Python
"""
print(multi)
#""" 안에 있는게 출력 된다.

#문자형의 함수
#문자의 길이
word = "apple banana"
print(len(word))
#print 값 : 12

#문자열 바꾸기
word = word.replace("apple", "orange")
print(word)
#print 값 : orange banana

#소문자로 변경
print(word.lower())
#대문자로 변경
print(word.upper())

#서식지정자
# + 연산을 이용
name = "Tom"
print("I am " + name + "!")
#print 값 : I am Tom!

# 서식지정자 사용
print("I am %s!" % name)
#print 값 : I am Tom!

# 공백추가
print("I am %10s!" % name)
print("I am %-10s!" % name)
#print 값 : I am        Tom!
#print 값 : I am Tom       !

# 여러개의 추가문자
f1, f2 = "apple", "banana"
print("I like %s %s " % (f1, f2))
#print 값 : I like apple banana 

# 숫자형
n1, n2 = 3, 3.2323
print("n1 = %d, n2 = %f" % (n1, n2))
#print 값 : n1 = 3, n2 = 3.232300

# 소수점 이하 자리수
print("n2 = %.2f" % n2)
#print 값 : n2 = 3.23

# 숫자갯수 맞추기
print("n2 = %07.2f" % n2)
#print 값 : n2 = 0003.23

#Format 함수
print("I like {0}, {1} !!".format("apple", "banana"))
#print 값 : I like apple, banana !!

f1, f2 = "apple", "banana"
print("I like {0} {1} !!".format(f1, f2))
#print 값 :  I like apple banana !!