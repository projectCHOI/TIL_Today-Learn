# 기본 문자열 문제

## 1. 주어진 문자를 입력하면 문자열의 길이를 알 수 있는 코드
def string_length(input_string):
    return len(input_string)

# 사용 예시
input_string = "Hello, World!"
print(f"문자열의 길이: {string_length(input_string)}")

## 2. 입력된 문자열을 뒤집는 코드
def reverse_string(input_string):
    return input_string[::-1]

# 사용 예시
input_string = "Hello, World!"
print(f"뒤집힌 문자열: {reverse_string(input_string)}")

## 3. 주어진 문자열을 대문자로 변환하거나 소문자로 변환하는 코드
def to_uppercase(input_string):
    return input_string.upper()

def to_lowercase(input_string):
    return input_string.lower()

# 사용 예시
input_string = "Hello, World!"
print(f"대문자로 변환: {to_uppercase(input_string)}")
print(f"소문자로 변환: {to_lowercase(input_string)}")

## 4. 주어진 문자에서 특정 단어를 입력하면 특정 단어의 등장 횟수를 카운팅 하는 코드
def count_word_occurrences(input_string, word):
    return input_string.count(word)

# 사용 예시
input_string = "Hello, World! Hello again!"
word = "Hello"
print(f"'{word}'의 등장 횟수: {count_word_occurrences(input_string, word)}")