##### 7장 리스트와 튜플
#리스트
a = [1, 2, 3, 4, 5, 6, 7]
print(a)
#print = [1, 2, 3, 4, 5, 6, 7]
#리스트는 일반적인 출력이 된다.

a = [1, "apple", 3.14, False]
print(a)
print(type(a))
#print = [1, 'apple', 3.14, False]
#print = <class 'list'>


#튜플
b = (1, 2, 3, 4, 5, 6, 7)
print(b)
#print = (1, 2, 3, 4, 5, 6, 7)

b = (1, "apple", 3.14, False)
print(b)
print(type(b))
#print = (1, 'apple', 3.14, False)
#print = <class 'tuple'>


#Range 함수사용
#파이썬의 숫자는 0부터 시작한다.
a = list(range(10))
b = tuple(range(10))
print(a)
print(b)
#print = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
#print = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

#리스트, 튜플의 변환
##print에 입력을 바꾸어 준다.
a = [1, 2, 3, 4, 5]
print(tuple(a))
#print = (1, 2, 3, 4, 5)

a = [1, 2, 3, 4, 5]
print(list(a))
#print = [1, 2, 3, 4, 5]

#인덱스 접근
a = [1, 2, 3, 4, 5]

print(a[2])
#print = 3
#리스트에 3번 값이란 의미
print(a[-1])
#print = 5
#리스트에서 -1번째
a[3] = 8
print(a)
#print = [1, 2, 3, 8, 5]
#리스트의 3번은 8이다. 라는뜻, 그래서 출력 값에서 3번이 바뀐다.

#슬라이스
a = [1, 2, 3, 4, 5]

print(a[0:4])
#print = [1, 2, 3, 4]
#0번째부터 4번째
print(a[1:-2])
#print = [2, 3]

#슬라이스 증가폭 변경
a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

print(a[2:8:2])
#print = [3, 5, 7]

#끝 인덱스까지 가져오기
print(a[:3])
print(a[3:])
print(a[:-3])
print(a[-3:])
#[1, 2, 3]
#[4, 5, 6, 7, 8, 9, 10]
#[1, 2, 3, 4, 5, 6, 7]
#[8, 9, 10]

#슬라이스 요소할당 [""] 이걸 사용
a = [1, 2, 3, 4, 5]

a[1:4] = ["a", "b", "c"]
print(a)
#print = [1, 'a', 'b', 'c', 5]

a[1:4] = ["d", "e"]
print(a)
#print = [1, 'd', 'e', 5]

#슬라이스 삭제 del를 사용
a = [1, 2, 3, 4, 5]

del a[1:4]
print(a)
#print = [1, 5]

a = [1, 2, 3, 4, 5]
del a[1]
print(a)
#print = [1, 3, 4, 5]

#리스트와 튜플의 기능들
#1. 특정값이 있는지 확인 (in)사용
a = [1, 2, 3, 4, 5]
print(1 in a)
print(6 in a)
#print = True
#print = False

#2. 연결하기 (+)사용
a = [1, 2, 3, 4, 5]
b = [6, 7, 8, 9]
print(a + b)
#print = [1, 2, 3, 4, 5, 6, 7, 8, 9]

#3. 반복하기 (*)사용
a = [1, 2, 3]
print(a * 3) # 반복횟수
#print = [1, 2, 3, 1, 2, 3, 1, 2, 3]

#4. 요소갯수 구하기 len() 사용
a = [1, 2, 3]
print(len(a))
#print = 3

#5. 요소 추가하기 append(값)
a = [1, 2, 3, 4, 5]
a.append(6)
print(a)
#print = [1, 2, 3, 4, 5, 6]

#6. 요소 추가하기 extend(값)
a = [1, 2, 3, 4, 5]
a.extend([7, 8])
print(a)
#print = [1, 2, 3, 4, 5, 6, 7, 8]

#7. 특정 인덱스에 요소 추가하기 insert(인덱스,값)
a = [1, 2, 3]
a.insert(2, 100)
print(a)
#print = [1, 2, 100, 3]

#8. 리스트 요소 삭제 pop(인덱스)
a = [1, 2, 3]
a.pop(0)
print(a)
#print = [2, 3]

#9. 리스트 특정값을 찾아 삭제 remove(값)
a = [100, 200, 300]
a.remove(200)
print(a)
#print = [100, 300]

#10. 순서 뒤집기 reverse()
a = [1, 2, 3]
a.reverse()
print(a)
#print = [3, 2, 1]

#11. 정렬하기 오름차순 a.sort()
a = [3, 2, 1, 4]
a.sort()
print(a)
#print = [1, 2, 3, 4]

#12. 정렬하기 내림차순 a.sort(reverse=True)
a = [3, 2, 1, 4]
a.sort(reverse=True)
print(a)
#print = [4, 3, 2, 1]

#리스트 할당과 복사
a = [1, 2, 3, 4, 5]
b = a
# b는 a랑 같다.
a is b
#print = True
#알았다는 뜻,

b[0] = 10
print(a)
print(b)
#print = [10, 2, 3, 4, 5]
#print = [10, 2, 3, 4, 5]
#값 확인한 것,

#다차원 리스트와 튜플
a = [[1, 2], [3, 4], [5, 6]]
print(a[0][1])
#print = 2
#리스트 전체에서 0번째 항목의 1번째 요소.
#파이썬의 숫자는 0부터 쓴다. 착각하지 말라고~



##### 8장 딕셔너리
score = {"name": "tom", "math": 80, "english": 70}
print(score["name"])
#print = tom
#자료를 가져오는 것

#키가 있는지 확인
score = {"name": "tom", "math": 80, "english": 70}
print("math" in score)
#print = True

score = {"name": "tom", "math": 80, "english": 70}
print("age" in score)
#print = False

#키의 갯수
score = {"name": "tom", "math": 80, "english": 70}
len(score)
#print = 3

#키-값 쌍 추가하기
score = {"name": "tom", "math": 80, "english": 70}
score.setdefault("age", 20)
print(score)
#print = {'name': 'tom', 'math': 80, 'english': 70, 'age': 20}

#키-값 수정하기
score = {"name": "tom", "math": 80, "english": 70}
score.update({"math": 90})
print(score)
#print = {'name': 'tom', 'math': 90, 'english': 70, 'age': 20, 'test': 100}

#키로 딕셔너리 항목삭제 pop
score = {"name": "tom", "math": 80, "english": 70}
score.pop("name")
print(score)
#print = {'math': 80, 'english': 70}

#모든 값 삭제
score = {"name": "tom", "math": 80, "english": 70}
score.clear()
print(score)
#print = {} # 아무것도 나오지 않음.

#모든 키, 값 가져오기
score = {"name": "tom", "math": 80, "english": 70}
print(score.keys())
#print = dict_keys(['name', 'math', 'english'])

#딕셔너리의 할당 a.copy()
a = {"a": 0, "b": 1}
b = a.copy()
b["a"] = 2
print(a)
print(b)
#print(a) = {'a': 0, 'b': 1} 
#print(b) = {'a': 2, 'b': 1}

#딕셔너리의 복사  copy.deepcopy
import copy
a = {"a": {"c": 0, "d": 0}, "b": {"e": 0, "f": 0}}
b = copy.deepcopy(a)
print(b)
#print = {'a': {'c': 0, 'd': 0}, 'b': {'e': 0, 'f': 0}}



##### 9장 세트 animal
animal = {"dog", "cat", "monkey", "horse"}
print(animal)
#print = {'horse', 'cat', 'monkey', 'dog'}
#print = 

#세트에 특정값 확인
animal = {"dog", "cat", "monkey", "horse"}
print("cat" in animal)
print("bird" in animal)
#print = True
#print = False

a = set("animal")
print(a)
#print = {'i', 'm', 'n', 'a', 'l'}

a = list("animal")
print(a)
#print = ['a', 'n', 'i', 'm', 'a', 'l']

#집합연산 - 합집합
a = {1, 2, 3}
b = {3, 4, 5}
print(a | b)                                           # | = shift + \ 사용
print(set.union(a, b))                                 # set.union 사용
#print = {1, 2, 3, 4, 5}
#print = {1, 2, 3, 4, 5}

#집합연산 - 교집합
a = {1, 2, 3}
b = {3, 4, 5}
print(a&b)                                             # &연산자 사용
print(set.intersection(a,b))                           # set.intersection 사용
#print = 3
#print = 3

#집합연산 - 차집합
a = {1, 2, 3}
b = {3, 4, 5}
print(a-b)                                             # -연산자 사용
print(set.difference(a,b))                             # set.difference 사용
#print = {1, 2}
#print = {1, 2}

#집합연산 - 대칭차집합
a = {1, 2, 3}
b = {3, 4, 5}
print(a^b)                                              # ^연산자 사용
print(set.symmetric_difference(a,b))                    # set.symmetric_difference 사용
#print = {1, 2, 4, 5}
#print = {1, 2, 4, 5}

#집합연산 - 부분집합
a = {1, 2, 3, 4}
b = {1, 2, 3, 4, 5}
print(a <= b)                                           # <= 연산자 사용
print(a.issubset(b))                                    # a.issubset 사용
#print = True
#print = True

#집합연산 - 상위집합
a = {1, 2, 3, 4}
b = {1, 2, 3, 4, 5}
print(a >= b)                                           # >=연산자 사용
print(a.issuperset(b))                                  # a.issuperset
#print = False
#print = False

#겹치는 요소 확인 a.isdisjoint
a = {1, 2, 3, 4}
b = {1, 2, 3, 4, 5}
print(a.isdisjoint(b))
#print = False

#세트 조작하기 [a.add]
a = {1, 2, 3, 4}
a.add(5) #5를 추가하라.
print(a)
#print = {1, 2, 3, 4, 5}

#세트 조작하기 [a.remove] #지워라 뜻
a = {1, 2, 3, 4}
a.remove(2)#지워라 2의 배수
print(a)
#print = {1, 3, 4}
