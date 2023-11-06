#사칙연산의 실습
### 변수를 합하라.
x = 20
y = 30
print(x + y) #50
print(x * y) #600

### input을 활용해 변수를 기입하여 연산하라.
x = input("x 값을 입력해주세요 :")
y = input("y 값을 입력해주세요 :")
#x = 20
#y = 30
print(int(x) + int(y)) #50
print(int(x) * int(y)) #600
print(x + y) #2030
print(x * y) #Error

#해설 : input(값)을 해야 숫자로 인지한다.
#print(x * y)는 곱하기, Error뜬다.



#비교연산자를 활용한 실습
a = input("첫번째 정수 : ") #70
b = input("두번째 정수 : ") #60
c = input("세번째 정수 : ") #50

print(int(a) > 65)
print(int(b) > 65)
print(int(c) > 65)
# True
# False
# False
print(int(a) > 65 and int(b) > 65 and int(c) > 65)
print(True and False and False)
# False
# False
print(int(a) > 65 or int(b) > 65 or int(c) > 65)
print(True and False and False)
# True
# False


#문자열 실습
### 문제 1 - 문자를 입력받아 공백을 모두 제거하고 출력하세요
word = input("아무 문자나 입력해주세요")
#팀의 체력을 책임지고 있는 성기사입니다.
print(word)
#팀의 체력을 책임지고 있는 성기사입니다.
print(word.replace(" ", ""))
#팀의체력을책임지고있는성기사입니다.

### 문제 2 - 이름과 점수3개를 입력받아 출력하세요.
name = input("이름을 입력해주세요 : ")
score1 = int(input("나이를 입력해주세요 : "))
#이름을 입력해주세요 : 최윤석
#나이를 입력해주세요 : 29
print(name)
print(score1)
#최윤석
#29
print("저의 이름은 " + str(name) + "  저의 연령은 " + str(score1))
#저의 이름은 최윤석  저의 연령은 29



### 리스트와 튜플의 실습 
### range 함수를 이용하여 사용자가 입력한 수까지 2의 배수값을 넣은 리스트를 만들고 리스트의 맨 마지막에 사용자가 입력한 추가해 주세요.
number = int(input("숫자를 입력해주세요 : "))
lists = list(range(2, number+1, 2))
lists.append(number)
print(lists)
#숫자를 입력해주세요 : 20 #(20을 넣을 경우)
#print = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 20]



### 딕셔너리의 실습
### 실습1 이름, 나이, 연락처를 입력받아 딕셔터리를 만들어 출력해주세요
name = input("이름을 입력해주세요 : ")
age = input("나이를 입력해주세요 : ")
number = input("연락처를 입력해주세요 : ")
#print = 이름을 입력해주세요 : 최윤석
#print = 나이를 입력해주세요 : 29
#print = 연락처를 입력해주세요 : 010-2504-1234

dic1 = {"이름": name, "나이": age, "연락처": number}
print(dic1)
#print = {'이름': '최윤석', '나이': '29', '연락처': '010-2504-1234'}


### 실습2  두사람의 이름, 나이, 연락처를 입력받아 각각 딕셔너리를 만들어 리스트에 넣어주세요 
name1 = input("이름을 입력해주세요 : ")
age1 = input("나이를 입력해주세요 : ")
number1 = input("연락처를 입력해주세요 : ")
name2 = input("이름을 입력해주세요 : ")
age2 = input("나이를 입력해주세요 : ")
number2 = input("연락처를 입력해주세요 : ")
#이름을 입력해주세요 : 홍길동
#나이를 입력해주세요 : 27
#연락처를 입력해주세요 : 010-3023-1223
#이름을 입력해주세요 : 이몽룡
#나이를 입력해주세요 : 30
#연락처를 입력해주세요 : 010-3030-4434

list1 = [{"이름": name1, "나이": age1, "연락처": number1}, {"이름": name2, "나이": age2, "연락처": number2}]
print(list1)
#print = [{'이름': '홍길동', '나이': '27', '연락처': '010-3023-1223'}, {'이름': '이몽룡', '나이': '30', '연락처': '010-3030-4434'}]

list2 = [] #바구니, 값을 여기에 넣는다.
list2.append({"이름": name1, "나이": age1, "연락처": number1})
list2.append({"이름": name2, "나이": age2, "연락처": number2})
print(list2)
#print = [{'이름': '홍길동', '나이': '27', '연락처': '010-3023-1223'}, {'이름': '이몽룡', '나이': '30', '연락처': '010-3030-4434'}]





