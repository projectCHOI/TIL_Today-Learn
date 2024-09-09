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